from __future__ import annotations
import importlib.util
import os,sys, readchar
from typing import Callable, Union

    
# ====================
# ----- TERMINAL -----
# ====================

class Terminal:
    def __init__(self,initmsg:str="",hist_len:int=32) -> None:
        self.env = {}                   
        self.history = []
        
        # Validation
        if hist_len<5:hist_len=5

        # Initialise Environment
        self.env["INITMSG"] = initmsg
        self.env["PS"] = "$"
        self.env["PATH"] = []
        self.env["HIST_LEN"] = hist_len
        self.env["PWD"] = os.getcwd()

    def AddPath(self,path:str):
        if path in self.env["PATH"]:return
        self.env["PATH"].append(path)

    def Start(self):
        # Clear screen at start
        clear()

        # Show welcome message
        print(self.env["INITMSG"],"\n")

        # Run main loop
        while True:
            # --- GET COMMAND
            print(self.env["PS"],end=" ",flush=True)
            command=input()
            # command=self._ut.get_command()

            if command.lower() in ["quit","exit"]:
                # self._ut.save_history(self.history)
                break

            # --- UPDATE HISTORY
            # Remove old duplicates
            if command in self.history:self.history.remove(command)
            # Insert current command
            if not command.strip()=="":self.history.insert(0,command)
            # Cap length
            hlen = self.env["HIST_LEN"]
            if len(self.history)>hlen:self.history = self.history[:hlen]


            # --- EXECUTE COMMAND
            try:
                cmd_chunks  = command.split(" ")
                cmd_exec    = cmd_chunks[0].strip()
                cmd_args    = [cnk for cnk in cmd_chunks[1:] if cnk.strip()!=""]

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

def pwd(env:dict):
    print(env["PWD"])

def env(env:dict,args:list[str]):
    keys        = env.keys()
    if len(args)!=0: keys = [a for a in args if a in keys]
    if len(keys)==0: return
    max_len     = max([len(k) for k in keys])
    if max_len > 32 : max_len = 32
    for key in keys:
        print(str(key).rjust(max_len),"=",env[key])
    
def echo(env:dict,args:list[str]):
    keys = env.keys()
    for i,a in enumerate(args):
        if a.startswith("$") and a[1:] in keys: args[i]=env[a[1:]]
    print(" ".join(args))
         
    
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






