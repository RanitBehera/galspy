from __future__ import annotations
import importlib.util
import os,sys, readchar
from typing import Callable, Union

class TerminalUtility:
    def __init__(self,terminal:Terminal) -> None:
        self.terminal=terminal
    
    def save_history(self,history):
        pass

    def execute_command(self,command:str):
        cmd_chunks  = command.split(" ")
        cmd_exec    = cmd_chunks[0]
        cmd_args    = cmd_chunks[1:]

        # Internal Command
        if cmd_exec.lower() in ["clear","cls","clc"]:
            self.clear()
        elif cmd_exec.lower() in ["pwd"]:
            self.pwd()
        elif cmd_exec.lower() in ["env"]:
            self.env(cmd_args)
        elif cmd_exec.lower() in ["echo"]:
            self.echo(cmd_args)
        elif cmd_exec.lower() in ["where","which"]:
            self.where(cmd_args,True)
        else:
            # External Command
            exec_path = self.where([cmd_exec])[0]
            exec_dir = str(os.path.dirname(exec_path))
            sys.path.insert(0,exec_dir)
            target=importlib.import_module(cmd_exec)
            #---
            target.main(cmd_args,self.terminal.env)
            #---
            sys.path.pop(0)
            
    def clear(self):
        if os.name=="nt":os.system("cls")
        else: os.system("clear")
    
    def pwd(self):
        print(self.terminal.env["PWD"])

    def env(self,args):
        env         = self.terminal.env
        keys        = env.keys()
        max_len     = max([len(k) for k in keys])   # check for empty in max
        if max_len > 32 : max_len = 32
        for key in env:print(str(key).rjust(max_len),"=",env[key])

    
    def echo(self,args):
        if len(args)==0:return
        env         = self.terminal.env
        keys        = env.keys()
        ckeys       = [a for a in args if a in keys]
        # ---
        max_len     = max([len(k) for k in ckeys])  # check for empty in max
        if max_len > 32 : max_len = 32
        for key in ckeys:print(env[key])

    def where(self,args,print_list:bool=False):
        found_path=[]
        for path in self.terminal.env["PATH"]:
            childs      = [c for c in os.listdir(path)]
            subfiles    = [f for f in childs if os.path.isfile(os.path.join(path, f))]
            pyfiles     = [p.split(".py")[0] for p in subfiles if p.endswith(".py") and not p.startswith(("_","__"))]

            for exe in args:
                if not exe in pyfiles: continue
                found_path.append(os.path.join(path,exe+".py"))

        if print_list: 
            for path in found_path:print(path)

        return found_path 


    # def get_command(self):
        # return "hi"
    

# -----------------------------------------------

class Terminal:
    def __init__(self,wlcmsg:str="",hist_len:int=32) -> None:
        self.env = {}                   
        self.history = []
        self._ut = TerminalUtility(self) 
        
        # Validation
        if wlcmsg=="":wlcmsg = "galspy terminal"
        if hist_len<5:hist_len=5

        # Initialise Environment
        self.env["WLCMSG"] = wlcmsg
        self.env["PS"] = "$"
        self.env["PATH"] = []
        self.env["HIST_LEN"] = hist_len
        self.env["PWD"] = os.getcwd()

    def AddPath(self,path:str):
        self.env["PATH"].append(path)

    def Start(self):
        # Clear screen
        self._ut.clear()

        # Show welcome message
        print(self.env["WLCMSG"],"\n")

        # Run main loop
        while True:
            # --- GET COMMAND
            print(self.env["PS"],end=" ",flush=True)
            command=input()
            # command=self._ut.get_command()

            if command.lower() in ["quit","exit"]:
                self._ut.save_history(self.history)
                break

            # --- UPDATE HISTORY
            # Remove old duplicates
            if command in self.history:
                self.history.remove(command)
            # Inser current command
            if not command.strip()=="":self.history.insert(0,command)
            # Cap length
            hlen = self.env["HIST_LEN"]
            if len(self.history)>hlen:
                self.history = self.history[:hlen]


            # --- EXECUTE COMMAND
            try:
                self._ut.execute_command(command)
            except Exception as e:
                print(e)



            

    

    
