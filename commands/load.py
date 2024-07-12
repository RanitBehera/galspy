from galspy.utility.termutil import get_available_sim



def main(env:dict,args:list[str]):
    if "sim" in args:
        requested_sim = args[args.index("sim")+1]
        available_sim = get_available_sim(env["PATH"])
        if requested_sim in available_sim.keys():
            env["SIM"] = requested_sim
            env["SIMFILE"] = available_sim[requested_sim]

    if "snap" in args:
        pass

    else:
        print('Possible arguments for "avail" are "sim" and "snap"')


def completion(env:dict):
    sim_dict = {}
    for sim in get_available_sim(env["PATH"]).keys():
        sim_dict[sim]=None

    return {
        "sim":sim_dict,
        "snap":None,
        "halo":None
    }