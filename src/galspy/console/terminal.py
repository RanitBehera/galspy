from __future__ import annotations
import importlib.util
import os,sys
import readline
import inspect

from prompt_toolkit import prompt, PromptSession
from prompt_toolkit.completion import WordCompleter, NestedCompleter
from prompt_toolkit.styles import Style
from prompt_toolkit.shortcuts import CompleteStyle
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory


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

        self.Set_Prompt_Style()


    def AddPath(self,path:str):
        if path in self.env["PATH"]:return
        self.env["PATH"].append(path)


    def Set_Prompt_Style(self):
        self.pt_style = Style.from_dict(
            {
                ""          : "#ffffff",
                "username"  : "#00ff00 bold",
                "at"        : "#ffffff bold",
                "hostname"  : "#ffff00 bold",
                "colon"     : "#ffffff bold",
                "workdir"   : "#3fa2f6 bold",
                "dollar"    : "#ffffff bold"
            }
        )


    def Get_Prompt(self):    
        prompt_fragmenets = [
            ("class:username",self.env["USER"]),
            ("class:at","@"),
            ("class:hostname",self.env["HOSTNAME"]),
            ("class:colon"," : "),
            ("class:workdir",self.env["PWD"].replace(self.env["HOME"],"~")),
            ("class:dollar","$ ")
        ]
        self.env["PS"]= "".join([val for _,val in prompt_fragmenets])
        return prompt_fragmenets


    def Get_RPrompt(self):
        rprompt = ""
        return rprompt


    def Get_Completion(self):
        completion_dict = {}
        

        internal_commands = [name for name,obj in inspect.getmembers(sys.modules[__name__]) 
                            if (inspect.isfunction(obj) and
                                # name.startswith('test') and
                                obj.__module__ == __name__)]

        print(internal_commands)
        internal_commands = ("quit","exit","clear","cls","clc","pwd","ls","env","echo","where","which")
        for ic in internal_commands:completion_dict[ic]=None

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
        session = PromptSession(style=self.pt_style,
                                completer=nest_completer,
                                complete_in_thread=True,
                                history=hist_file,
                                auto_suggest=AutoSuggestFromHistory()
                               )
        return
        # Run main loop
        while True:
            # <----- UPDATE PROMPT ----->
            prompt_fragments = self.Get_Prompt()
            rprompt = self.Get_RPrompt()

            # <----- GET COMMAND ----->
            # command=input(self.env["PS"] + " ")
            command = session.prompt(prompt_fragments,rprompt=rprompt)
            
            if command=="": continue
            if command.lower() in ["quit","exit"]:
                # self._ut.save_history(self.history)
                break


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
                if cmd_exec_lc in ["clear","cls","clc"]: clear()
                elif cmd_exec_lc in ["pwd"]: pwd(self.env)
                elif cmd_exec_lc in ["ls"]: ls(self.env,cmd_args)
                elif cmd_exec_lc in ["env"]: env(self.env,cmd_args)
                elif cmd_exec_lc in ["echo"]: echo(self.env,cmd_args)
                elif cmd_exec_lc in ["where","which"]: where(self.env,cmd_args,True)
                else:
                    # External Command
                    exec_path = where(self.env,[cmd_exec])
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

def clear():
    if os.name=="nt":os.system("cls")
    else: os.system("clear")

cls = clear

def pwd(env:dict):
    print(env["PWD"])


def echo(env:dict,args:list[str]):
    print(" ".join(args))


def env(env:dict,args:list[str]):
    keys        = env.keys()
    if len(args)!=0: keys = [a for a in args if a in keys]
    if len(keys)==0: return
    max_len     = max([len(k) for k in keys])
    if max_len > 32 : max_len = 32
    for key in keys:
        print(str(key).rjust(max_len),"=",env[key])


def where(env:dict,args:list[str],print_list:bool=False):
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


def ls(env:dict,args:list[str]):
    path = env["PWD"]
    childs = [c for c in os.listdir(path)]
    for c in childs:
        if os.path.isdir(os.path.join(path,c)):
            print("",c,end="\t")
        elif os.path.isfile(os.path.join(path,c)):
            print(c,end="\t")
    print("")






