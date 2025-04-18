# %%
import pickle
import numpy as np
import galspy as gs
import matplotlib.pyplot as plt

import galspy as gs
from matplotlib.gridspec import GridSpec

from galspy.Spectra.Dust import DustExtinction
de = DustExtinction()


SIM = gs.NavigationRoot(gs.NINJA.L250N2040)
PIG = SIM.PIG(z=7)


st_mass = PIG.FOFGroups.MassByType().T[4]


# Light

PATH_DIR_LG = "/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/light_generation/data/"
PATH_DIR_CD = "/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/column_density/data/"
def DoForFile(filepath_cd:str,filepath_lg:str,label):
    data = np.loadtxt(PATH_DIR_LG+filepath_lg,usecols=(1,5,6))
    tgid,MAB,uvbeta = data.T
    tgid = np.int64(tgid)

    with open(PATH_DIR_CD+filepath_cd,"rb") as fp:
        clm_data:dict = pickle.load(fp)

    avail_tgid = clm_data.keys()
    avail_mask = [tg in avail_tgid for tg in tgid] 

    mtgid = tgid[avail_mask]
    mMAB = MAB[avail_mask]
    muvbeta = uvbeta[avail_mask]
    AVs = np.array([clm_data[tg][1] for tg in mtgid])
    mst_mass = st_mass[mtgid-1]*1e10/0.6736

    # plt.figure()
    # plt.plot(mst_mass,AVs,'.',ms=2)
    # plt.xscale("log")
    # plt.yscale("log")
    # plt.xlabel("Stellar Mass")
    # plt.ylabel("AV")

    # plt.figure()
    # plt.plot(mMAB,AVs,'.',ms=2)
    # plt.yscale("log")
    # plt.xlabel("MAB")
    # plt.ylabel("AV")

    # plt.figure()
    # dbeta = factor * AV
    factor=1.1
    delta_beta = factor*AVs
    beta = muvbeta + delta_beta

    # print(np.median(beta))


    plt.plot(mst_mass,AVs,'.',ms=5,alpha=0.3,label=label)
    # plt.hexbin(mst_mass,beta,gridsize=100,cmap="Oranges",xscale='log',bins='log')



DoForFile("L250N2040_z7p00.dict","out_L250N2040_z7p0_stnb_chabrier300_bin.csv","L250N2040")
# DoForFile("L150N2040_z7p0_Av_a1p0.dict","out_L150N2040_z7p0_stnb_chabrier300_bin.csv","L150N2040")

plt.xscale("log")
plt.yscale("log")
plt.xlabel("Stellar Mass")
plt.ylabel("$A_V$")
# plt.ylim(-3,1)
plt.xlim(1e8,1e11)
# plt.gca().set_aspect('equal',adjustable='box') # box, datalim

plt.legend()


plt.show()

# %%
