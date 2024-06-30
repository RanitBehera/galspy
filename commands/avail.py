import os

def completion():
    return {
        "sim":None,
        "snap":None
    }

def help():pass

def main(env:dict,args:list[str]):
    if args[0]=="sim":
        avail_sim(env["PATH"],args[1:])
    elif args[0]=="snap":
        pass
    else:
        print('Possible arguments for "avail" are "sim" and "snap"')

SIM_EXTENSON = ".sim"
def avail_sim(serach_paths:list[str],match_list:list[str]):
    # Find sim-files
    for path in serach_paths:
        childs      = [c for c in os.listdir(path)]
        subfiles    = [f for f in childs if os.path.isfile(os.path.join(path, f))]
        simfiles    = [s.split(SIM_EXTENSON)[0] for s in subfiles if s.endswith(SIM_EXTENSON) and not s.startswith("_")]

    # Filter for matching string
    if len(match_list)==0:
        [print(sim) for sim in simfiles]
    else:
        simfiles_filtered = []
        for sim in simfiles:
            for match in match_list:
                if match in sim: simfiles_filtered.append(sim)
    
        [print(sim) for sim in simfiles_filtered]