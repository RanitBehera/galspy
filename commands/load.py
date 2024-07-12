from galspy.utility.termutil import get_available_sim



def main(env:dict,args:list[str]):
    if args[0]=="sim":
        requested_sim = args[1]
        available_sim = get_available_sim(env["PATH"])
        if requested_sim in available_sim.keys():
            env["SIM"] = requested_sim
            env["SIMFILE"] = available_sim[requested_sim]

    elif args[0]=="snap":
        pass
    else:
        print('Possible arguments for "avail" are "sim" and "snap"')


def completion():
    return {
        "sim":None,
        "snap":None,
        "halo":None
    }