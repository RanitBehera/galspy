import numpy as np
import os
from galspec.bpass import BPASSCache

specs:dict = BPASSCache("cache/bpass_chab_300M.ch").Read()

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
OUTDIR = "/mnt/home/student/cranit/RANIT/Repo/galspy/study/cloudy/bpass_sed2"
# OUTDIR = "/mnt/home/student/cranit/RANIT/Repo/galspy/study/cloudy/bpass_1Myr/Lnu"
LAM_NORM = 2 #In Angstrom
NORM = []
for i,Tkey in enumerate(Tkeys):
    if i==51:break
    # if not i%10==7: continue
    Tspec   = specs[Z][Tkey]
    WriteSEDFile(OUTDIR + os.sep + f"t{i}.sed",WL,Tspec)
    print(f"t{i}.sed")

    # Report Normalisation
    NORM += [Tspec[LAM_NORM-1]]

print("\nCLOUDY Normalisation : ",end="")
print(f"L(nu) = $__LNORM__ at {912/LAM_NORM:.04f} Ryd")
# BPASS reports Flux in L_solar / Angstrom
NORM = np.array(NORM)
# CLOUDY accespts in Watts / Hz
NORM = NORM * ((LAM_NORM**2)*(3.846e33)/(3e18))
NORM = np.round(np.log10(NORM),3)

print("[" + ",".join([str(l) for l in NORM]) + "]")