import numpy as np
import os
from galspec.bpass import BPASSCache

specs:dict = BPASSCache("cache/bpass.ch").Read()

Z = "0.00001"
Zspecs  = specs[Z]
Tkeys   = specs["T_KEYS"] 
WL      = Zspecs["WL"]

def WriteSEDFile(filepath,angtrom,Flambda):
    # Flambda=np.clip(Flambda,)
    np.savetxt(filepath,np.column_stack((angtrom,Flambda)),fmt="%d %.7E")
    with open(filepath, 'r') as sed:
        lines = sed.readlines()
    lines[0] = lines[0].strip() + f" Flambda units Angstrom extrapolate" + '\n'
    with open(filepath, 'w') as sed:
        sed.writelines(lines)


# ================
OUTDIR = "/mnt/home/student/cranit/RANIT/Repo/galspy/study/cloudy/bpass_sed"
for i,Tkey in enumerate(Tkeys):
    if i==11:break
    # if not i%10==7: continue
    Tspec   = specs[Z][Tkey]
    WriteSEDFile(OUTDIR + os.sep + f"t{i}.sed",WL,Tspec)
    print(f"t{i}.sed")

    # Report Normalisation