from __future__ import annotations
import importlib.util
import os,sys
import readline
import inspect

from prompt_toolkit import prompt, PromptSession
from prompt_toolkit.completion import WordCompleter, NestedCompleter
from prompt_toolkit.shortcuts import CompleteStyle
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.formatted_text import ANSI as PT_ANSI



# =============================
# ----- ANSI ESCAPE CODE ------
# =============================
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

        self.ic = self.Get_Internal_Commands()

    def AddPath(self,path:str):
        if path in self.env["PATH"]:return
        self.env["PATH"].append(path)

    def Get_Internal_Commands(self):
        int_cmd = {}
        for name,obj in inspect.getmembers(sys.modules[__name__]):
            if not (inspect.isfunction(obj) and obj.__module__ == __name__): continue
            int_cmd[name]=obj                           
        return int_cmd

    def Get_Prompt(self):    
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
        


    def Get_RPrompt(self):
        rprompt = ANSI.BG_CYAN + ANSI.FG_BLACK + " GalSpy " + ANSI.RESET
        return rprompt


    def Get_Completion(self):
        completion_dict = {}

        # Auto-Detect Internal Commands 
        internal_commands = [key_name for key_name,_ in self.ic.items()]
        for ic in internal_commands:completion_dict[ic]=None

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


    def Start(self,clear_prev = False):
        # Clear screen at start
        if clear_prev:clear()

        # Show welcome message
        if not self.env["INITMSG"]=="":print(self.env["INITMSG"])

        # Promot Session
        nest_completer  = NestedCompleter.from_nested_dict(self.Get_Completion())
        hist_file       = FileHistory(os.path.join(os.environ.get("HOME"),".gspy_history"))
        session = PromptSession(completer=nest_completer,
                                complete_in_thread=True,
                                history=hist_file,
                                auto_suggest=AutoSuggestFromHistory()
                               )
        
        # Run main loop
        while True:
            # <----- UPDATE PROMPT ----->
            prompt  = self.Get_Prompt()
            rprompt = self.Get_RPrompt()

            # <----- GET COMMAND ----->
            # command=input(prompt)
            command:str = session.prompt(PT_ANSI(prompt),rprompt=PT_ANSI(rprompt))
                                         
            
            if command=="": continue
            if command.lower() in ["quit","exit"]: break


            # <----- EXECUTE COMMAND ----->
            try:
                tokens      = command.split(" ")
                
                # Replace env-variables
                env_keys    = self.env.keys()
                for i,tok in enumerate(tokens):
                    if not tok.startswith("$"): continue
                    tok = tok[1:]

                    if not tok in env_keys: continue
                    env_val = self.env[tok]

                    if not type(env_val) in [str,int,float]:continue
                    tokens[i] = env_val
                
                # Extract exec name and args
                cmd_exec    = tokens[0].strip()
                cmd_args    = [arg for arg in tokens[1:] if arg.strip()!=""]

                # Expand combined args
                for i,arg in enumerate(cmd_args):
                    if not arg.startswith('-'): continue
                    if arg.startswith("--"): continue
                    if len(arg)==2:continue
                    cmd_args.remove(arg)
                    [cmd_args.insert(i,"-"+char) for char in arg[1:][::-1] if char.isalnum()] 
                

                # Internal Command
                cmd_exec_lc = cmd_exec.lower()
                if cmd_exec_lc in self.ic : 
                    self.ic[cmd_exec_lc](self.env,cmd_args)
                else:
                    # External Command
                    exec_path = which(self.env,[cmd_exec],False)
                    if len(exec_path)==0:
                        print("Unknown command :",cmd_exec)
                        continue
                    else:
                        exec_path=exec_path[0]
                    exec_dir = str(os.path.dirname(exec_path))
                    sys.path.insert(0,exec_dir)
                    target=importlib.import_module(cmd_exec)
                    #----------
                    target.main(self.env,cmd_args)
                    #----------
                    sys.path.pop(0)
            except Exception as e:
                print(e)



            

    

    
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







