import argparse, os
from galspy.utility.termutil import get_available_sim
from galspy.FileTypes.ConfigFile import ReadAsDictionary

def completion(env:dict):
    snap = {"PART":None,"PIG":None,"RSG":None}
    return {
        "-s":None,
        "--sim":None,
        "-n":snap,
        "--snap":snap,
        "-l":None,
        "--halo":None
    }


def main(env:dict):
    ap = argparse.ArgumentParser()
    
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument('-s','--sim', action='store_true')
    group.add_argument('-n','--snap', action='store_true')
    group.add_argument('-l','--halo', action='store_true')
    ap.add_argument("filters",type=str,nargs='*',help="Filter for matching results.")
    args = ap.parse_args()

    if args.sim:
        found_sims = get_available_sim(env["PATH"],args.filters)
        [print(sim) for sim in found_sims]
    elif args.snap:
        if "SIM" not in env.keys():
            print(f'No target "SIM" environment set.')
            return
        
        simfile = ReadAsDictionary(env["SIMFILE"])
        
        SDIR = simfile["MPGADGET_SNAPSHOT_OUTPUT"]
        child_sdir = os.listdir(SDIR)
        child_sdir = [dir for dir in child_sdir if os.path.isdir(os.path.join(SDIR,dir)) and str(dir).startswith(("PART","PIG"))]
        
        if "PART" in args.filters or args.filters==[]:
            [print(dir,end="   ") for dir in child_sdir if str(dir).startswith("PART")]
        
        if "PIG" in args.filters or args.filters==[]:
            [print(dir,end="   ") for dir in child_sdir if str(dir).startswith("PIG")]

        if "RSG" in args.filters or args.filters==[]:
            RDIR = simfile["ROCKSTAR_GALAXIES_OUTBASE"]
            child_rdir = os.listdir(RDIR)
            child_rdir = [dir for dir in child_rdir if os.path.isdir(os.path.join(RDIR,dir)) and str(dir).startswith("RSG")]
            
            [print(dir,end="   ") for dir in child_rdir]
        
        print()

    elif args.halo:
        pass




