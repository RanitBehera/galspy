import argparse
from deprecated.termutil import get_available_sim


def completion(env:dict):
    sim_dict = {}
    for sim in get_available_sim(env["PATH"]).keys():
        sim_dict[sim]=None

    return {
        "-s":sim_dict,
        "--sim":sim_dict,
        "-n":None,
        "--snap":None,
        "-l":None,
        "--halo":None
    }


def main(env:dict):
    ap = argparse.ArgumentParser()
    ap.add_argument('-s','--sim', type=str)
    ap.add_argument('-n','--snap', type=int)
    ap.add_argument('-l','--halo', type=int)
    args = ap.parse_args()

    if not args.sim == None:
        available_sim = get_available_sim(env["PATH"])
        if args.sim in available_sim.keys():
            env["SIM"] = args.sim
            env["SIMFILE"] = available_sim[args.sim]
    
    if not args.snap == None and args.snap>=0:
        env["SNAP"] = args.snap
    
    if not args.halo == None and args.halo>=0:
        env["HALO"] = args.halo



