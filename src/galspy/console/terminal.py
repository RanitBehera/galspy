from __future__ import annotations
import importlib.util
import os,sys
import readline
import inspect
import traceback


from prompt_toolkit import prompt, PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.completion import WordCompleter, NestedCompleter, PathCompleter
from prompt_toolkit.completion.base import CompleteEvent
from prompt_toolkit.document import Document
from prompt_toolkit.shortcuts import CompleteStyle
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.formatted_text import ANSI as PT_ANSI
from prompt_toolkit.key_binding import KeyBindings



# =============================
# ----- ANSI ESCAPE CODE ------
# =============================
#region
class ANSI:
    def ansi(n):return f"\033[{n}m"

    RESET           = ansi(0)
    BOLD            = ansi(1)
    DIM             = ansi(2)
    ITALIC          = ansi(3)
    UNDERLINE       = ansi(4)
    REVERSE         = ansi(7)
    STRIKE          = ansi(9)
    NORMAL          = ansi(22)
    NO_ITALIC       = ansi(23)
    NO_UNDERLINE    = ansi(24)
    NO_REVERSE      = ansi(27)
    NO_STRIKE       = ansi(29)
    OVERLINE        = ansi(53)
    NO_OVERLINE     = ansi(55)
    FG_BLACK        = ansi(30)
    FG_RED          = ansi(31)
    FG_GREEN        = ansi(32)
    FG_YELLOW       = ansi(33)
    FG_BLUE         = ansi(34)
    FG_MAGENTA      = ansi(35)
    FG_CYAN         = ansi(36)
    FG_WHITE        = ansi(37)
    FG_RESET        = ansi(39)
    BG_BLACK        = ansi(40)
    BG_RED          = ansi(41)
    BG_GREEN        = ansi(42)
    BG_YELLOW       = ansi(43)
    BG_BLUE         = ansi(44)
    BG_MAGENTA      = ansi(45)
    BG_CYAN         = ansi(46)
    BG_WHITE        = ansi(47)
    BG_RESET        = ansi(49)

    def fg_256(n):return f"\033[38;5;{n}m"
    def bg_256(n):return f"\033[48;5;{n}m"
    def fg_rgb(r,g,b):return f"\033[38;2;{r};{g};{b}m"
    def bg_rgb(r,g,b):return f"\033[48;2;{r};{g};{b}m"

#endregion




# ==========================
# ----- PROMPT TOOLKIT -----
# ==========================
_kb = KeyBindings()

@_kb.add('"')
def _(event):
    buffer = event.current_buffer
    buffer.insert_text('"')
    buffer.insert_text('"',move_cursor=False)

@_kb.add('(')
def _(event):
    buffer = event.current_buffer
    buffer.insert_text('(')
    buffer.insert_text(')',move_cursor=False)

@_kb.add('{')
def _(event):
    buffer = event.current_buffer
    buffer.insert_text('{')
    buffer.insert_text('}',move_cursor=False)



class _CommandCompleter(Completer):
    def __init__(self,env:dict) -> None:
        self.env = env
        self.path_completer = PathCompleter()
        self.nest_completer = NestedCompleter.from_nested_dict(self.get_nest_dict())

    def get_nest_dict(self):
        completion_dict = {}

        # Auto-Detect Internal Commands
        for name,obj in inspect.getmembers(sys.modules[__name__]):
            if not (inspect.isfunction(obj) and obj.__module__ == __name__): continue
            completion_dict[name]=None
 
        # Auto-Detect External Commands 
        for path in self.env["PATH"]:
            childs      = [c for c in os.listdir(path)]
            subfiles    = [f for f in childs if os.path.isfile(os.path.join(path, f))]
            pyfiles     = [p.split(".py")[0] for p in subfiles if p.endswith(".py") and not p.startswith("_")]
            for pyfile in pyfiles:
                sys.path.insert(0,path)
                target=importlib.import_module(pyfile)
                if hasattr(target,"main") and hasattr(target,"completion"):
                    completion_dict.update({pyfile:target.completion()})
                sys.path.pop(0)
        return completion_dict 
    
    def get_completions(self, document: Document, complete_event: CompleteEvent) -> os.Iterable[Completion]:
        if document.text.startswith("cd "):
            yield from (
                Completion(c.text,c.start_position,display=c.display)
                for c in self.path_completer.get_completions(Document(document.text[3:]),complete_event)
            )
        elif document.text.startswith("env "):
            word_bc = document.get_word_before_cursor(True)
            yield from (
                Completion(key,-len(word_bc))
                for key in self.env.keys() if key.startswith(word_bc)
            )
        else:
            yield from (
                Completion(comp.text,comp.start_position,display=comp.display)
                for comp in self.nest_completer.get_completions(Document(document.text),complete_event)
            )
        




# ====================
# ----- TERMINAL -----
# ====================

class Terminal:
    def __init__(self,initmsg:str="") -> None:
        self.env = {}                  
        self.env["INITMSG"] = initmsg
        self.env["PS"] = "$"
        self.env["PWD"] = os.getcwd()
        self.env["USER"] = os.environ.get("USER")
        self.env["HOSTNAME"] = os.environ.get("HOSTNAME")
        self.env["HOME"] = os.environ.get("HOME")
        self.env["PATH"] = []

        self._int_cmd = self._get_internal_commands()
        self._enable_nerd_font = True
    
    def SetTitle(self,title:str):
        print(f"\33]0;{title}\a",end="") 

    def AddPath(self,path:str,recursive:bool=False):
        def Add_If_New(new_path:str):
            if not new_path in self.env["PATH"]:
                self.env["PATH"].append(new_path)

        Add_If_New(path)
        
        if recursive:
            MAX_RECURSION_DEPTH = 2
            
            def AddSubDir(path:str,recursion_level:int=1):
                if recursion_level>MAX_RECURSION_DEPTH:return
                childs = [os.path.join(path,c) for c in os.listdir(path) if os.path.isdir(os.path.join(path,c)) and not c.startswith((".","_"))]
                for child in childs:
                    Add_If_New(child)
                    AddSubDir(child,recursion_level+1)
            
            AddSubDir(path)

    def Start(self,clear_prev = False):
        self.SetTitle("GalSpy")
        
        # Clear screen at start
        if clear_prev:clear()

        # Show welcome message
        if not self.env["INITMSG"]=="":print(self.env["INITMSG"])

        # Promot Session
        nest_completer  = _CommandCompleter(self.env)
        hist_file       = FileHistory(os.path.join(os.environ.get("HOME"),".gspy_history"))
        session         = PromptSession(completer=nest_completer,
                                complete_in_thread=True,
                                history=hist_file,
                                auto_suggest=AutoSuggestFromHistory(),
                                key_bindings=_kb
                               )
        
        # Run main loop
        while True:
            # ----- UPDATE PROMPT
            prompt  = self._get_prompt()
            rprompt = self._get_rprompt()

            # ----- GET COMMAND
            command:str = str(session.prompt(PT_ANSI(prompt),rprompt=PT_ANSI(rprompt)))
                                         
            # ----- IMMEDIATE ACTION
            if command.strip()=="": continue
            if command.lower() in ["quit","exit"]: break

            # ----- PARSE COMMAND
            # Tokenize command
            tokens      = [token.strip() for token in command.split(" ") if token.strip!=""]
            
            # Replace env-variables
            self._expand_env_tokens(tokens)

            # Extract name and args
            cmd_name, cmd_args    = tokens[0],tokens[1:] 

            # Expand combined arguments
            self._split_merged_options(cmd_args)

            # ----- EXECUTE COMMAND
            # Internal commands
            if cmd_name in self._int_cmd : 
                self._int_cmd[cmd_name](self.env,cmd_args)
                continue
            
            # External commands
            exec_path = which(self.env,[cmd_name],False)
            if len(exec_path)==0:
                print("Unknown command :",cmd_name)
                continue
            
            exec_path=exec_path[0]
            exec_dir = str(os.path.dirname(exec_path))
            try:
                sys.path.insert(0,exec_dir)
                target=importlib.import_module(cmd_name)
                target.main(self.env,cmd_args)
            except Exception as e:
                traceback.print_exc()
            else:
                pass
            finally:
                sys.path.pop(0)
                

    def _get_internal_commands(self):
        int_cmd = {}
        for name,obj in inspect.getmembers(sys.modules[__name__]):
            if not (inspect.isfunction(obj) and obj.__module__ == __name__): continue
            int_cmd[name]=obj                           
        return int_cmd

    def _get_prompt(self):    
        prompt_fragmenets = [
            (ANSI.BOLD+ANSI.fg_256(47),self.env["USER"]),
            (ANSI.BOLD,"@"),
            (ANSI.BOLD+ANSI.fg_256(184),self.env["HOSTNAME"]),
            (ANSI.BOLD," : "),
            (ANSI.BOLD+ANSI.fg_256(33),self.env["PWD"].replace(self.env["HOME"],"~")),
            (ANSI.BOLD,"$ ")
        ]
        self.env["PS"]= "".join([val for _,val in prompt_fragmenets])
        return "".join(["".join(frag)+ANSI.RESET for frag in prompt_fragmenets])
        
    def _get_rprompt(self):
        rprompt = ""
        rprompt += ANSI.FG_CYAN +"\ue0b6" + ANSI.RESET 
        rprompt += ANSI.BG_CYAN + ANSI.FG_BLACK + "GalSpy" + ANSI.RESET
        rprompt += ANSI.FG_CYAN +"\uf07b" 
        return rprompt

    def _expand_env_tokens(self,tokens:list[str]):
        env_keys    = self.env.keys()
        for i,tok in enumerate(tokens):
            if not tok.startswith("$"): continue
            tok = tok[1:]

            if not tok in env_keys: continue
            env_val = self.env[tok]

            if not type(env_val) in [str,int,float]:continue
            tokens[i] = env_val
        return tokens

    def _split_merged_options(self,cmd_args):                        
        for i,arg in enumerate(cmd_args):
            if not arg.startswith('-'): continue
            if arg.startswith("--"): continue
            if len(arg)==2:continue
            cmd_args.remove(arg)
            [cmd_args.insert(i,"-"+char) for char in arg[1:][::-1] if char.isalnum()] 


            
# =============================
# ----- INTERNAL COMMANDS -----
# =============================

def clear(env:dict,args:list[str]):
    if os.name=="nt":os.system("cls")
    else: os.system("clear")


def pwd(env:dict,args:list[str]):
    print(env["PWD"])


def echo(env:dict,args:list[str]):
    print(" ".join(args))


def cd(env:dict,args:list[str]):
    todir= args[0] if len(args)>0 else env["HOME"]
    os.chdir(todir)
    env["PWD"] = os.getcwd()


def mkdir(env:dict,args:list[str]):
    for a in args:
        if a.startswith(("-","/")):continue
        os.mkdir(os.path.join(env["PWD"],a))


def ls(env:dict,args:list[str]):
    path    = env["PWD"]
    childs  = [c for c in os.listdir(path)]
    child_dirs    = []
    child_files   = []
    child_links   = []
    for c in childs:
        if os.path.isdir(os.path.join(path,c)):
            child_dirs.append(c)
        elif os.path.islink(os.path.join(path,c)):
            child_links.append(c)
        elif os.path.isfile(os.path.join(path,c)):
            child_files.append(c)

    
    # Remove Hidden Childs
    if not "-a" in args:
        child_dirs  = [d for d in child_dirs if not d.startswith(".")]
        child_files = [f for f in child_files if not f.startswith(".")]
        child_links = [l for l in child_links if not l.startswith(".")]

    # Format Printing
    END = "\n" if "-l" in args else "  "
    [print(ANSI.fg_256(33)+d+ANSI.RESET,end=END) for d in child_dirs]
    [print(ANSI.fg_256(51)+l+ANSI.RESET,os.readlink(os.path.join(path,l)) if "-l" in args else "",sep="  ->  ",end=END) for l in child_links]
    [print(f,end=END) for f in child_files]
    
    print("")


def env(env:dict,args:list[str]):
    keys        = env.keys()
    if len(args)!=0: keys = [a for a in args if a in keys]
    if len(keys)==0: return
    max_len     = max([len(k) for k in keys])
    if max_len > 32 : max_len = 32
    for key in keys:
        print(str(key).rjust(max_len),"=",env[key])


def which(env:dict,args:list[str],print_list:bool=True):
    found_path=[]
    for path in env["PATH"]:
        childs      = [c for c in os.listdir(path)]
        subfiles    = [f for f in childs if os.path.isfile(os.path.join(path, f))]
        pyfiles     = [p.split(".py")[0] for p in subfiles if p.endswith(".py") and not p.startswith("_")]
        for exe in args:
            if not exe in pyfiles: continue
            found_path.append(os.path.join(path,exe+".py"))
    if print_list: 
        for path in found_path:print(path)
    return found_path 







