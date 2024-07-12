import os

SIM_EXTENSON = ".sim"
def get_available_sim(serach_paths:list[str],filters:list[str]=None):
    # Validate
    if filters==None:filters=[]


    found_simfiles ={}
    
    # Find sim-files
    for path in serach_paths:
        childs      = [c for c in os.listdir(path)]
        subfiles    = [f for f in childs if os.path.isfile(os.path.join(path, f))]

        for file in subfiles:
            if not file.endswith(SIM_EXTENSON): continue 
            if file.startswith("_"): continue
            val = os.path.join(path, file)
            key = file.split(SIM_EXTENSON)[0]
            found_simfiles[key]=val

    # Filter for matching string

    if len(filters)==0:
        return found_simfiles
    else:
        filtered_simfiles= {}
        for sim in found_simfiles.keys():
            for word in filters:
                if word in sim: filtered_simfiles[sim]=found_simfiles[sim]
        return filtered_simfiles