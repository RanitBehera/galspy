
def completion():
    return {
        "sim":None,
        "snap":None
    }

def main(env:dict,args:list[str]):
    if args[0]=="sim":
        pass
    elif args[0]=="snap":
        pass
    else:
        print('Possible arguments for "avail" are "sim" and "snap"')