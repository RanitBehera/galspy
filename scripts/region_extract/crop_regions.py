import galspy
import numpy as np
import matplotlib.pyplot as plt
import os
from multiprocessing import Pool

L50N1008 = "/mnt/home/student/cranit/Data/MP_Gadget/Nishi/L50N1008z05"
SAVEDIR = "/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/region_extract/data_kanish"

root = galspy.NavigationRoot(L50N1008)


def FilterGIDs():
    st_mass = root.PIG(174).FOFGroups.MassByType().T[4]
    gid     = root.PIG(174).FOFGroups.GroupID()

    mask = np.argsort(st_mass)
    st_mass = st_mass[mask]
    gid = gid[mask]

    select_mask = (st_mass>=0.5) & (st_mass<=5)

    return gid[select_mask]

    # plt.plot(gid[select_mask],st_mass[select_mask],'.g',ms=2)
    # plt.plot(gid[~select_mask],st_mass[~select_mask],'.k',ms=1)
    # plt.xscale("log")
    # plt.yscale("log")
    # plt.axhspan(0.1,10,color='k',alpha=0.1,ec=None)
    # plt.show()

selected_gids=FilterGIDs()

SAVEDIR = SAVEDIR + os.sep + "GIDSET"
os.makedirs(SAVEDIR,exist_ok=True)

for gid in selected_gids:
    GIDDIR=SAVEDIR+os.sep+f"GID_{gid}"
    os.makedirs(GIDDIR,exist_ok=True)


    
