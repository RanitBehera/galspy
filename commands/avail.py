import os

def main(env:dict,args:list[str]):
    if args[0]=="sim":
        avail_sim(env["PATH"])
    elif args[0]=="snap":
        pass
    else:
        print('Possible arguments for "avail" are "sim" and "snap"')

SIM_EXTENSON = ".sim"
def avail_sim(serach_paths:list[str]):
    for path in serach_paths:
        childs      = [c for c in os.listdir(path)]
        subfiles    = [f for f in childs if os.path.isfile(os.path.join(path, f))]
        simfiles    = [s.split(SIM_EXTENSON)[0] for s in subfiles if s.endswith(SIM_EXTENSON) and not s.startswith("_")]

    [print(sim,end="\t") for sim in simfiles]
    print("")