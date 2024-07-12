from galspy.utility.termutil import get_available_sim

def main(env:dict,args:list[str]):
    if args[0]=="sim":
        found_sims = get_available_sim(env["PATH"],args[1:]).keys()
        [print(sim) for sim in found_sims]
    elif args[0]=="snap":
        pass
    else:
        print('Possible arguments for "avail" are "sim" and "snap"')


def completion(env:dict):
    return {
        "sim":None,
        "snap":None
    }

def help():
    pass