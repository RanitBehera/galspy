import os

def completion():
    return {
        "genic":None,
        "gadget":None,
        "rockstar":None,
    }

def help():pass

def main(env:dict,args:list[str]):
    if len(args):pass

    if args[0].lower()=="genic":_genic(os.path.join(env["PWD"],"paramfile.genic"))
    


def _genic(out_path:str):
    # with open(out_path,"w") as fh:
    pass





    

