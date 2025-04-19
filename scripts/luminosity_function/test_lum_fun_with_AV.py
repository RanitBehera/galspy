# %%
import pickle
import numpy as np
import galspy as gs
import matplotlib.pyplot as plt

import galspy as gs
from matplotlib.gridspec import GridSpec

from load_observation import load_obs_to_axis
from load_lum_function import load_lf_to_axis

from galspy.Spectra.Dust import DustExtinction
de = DustExtinction()

REDSHIFT=7

# Light
load_obs_to_axis(plt.gca(),REDSHIFT,["Bouwens+21","Donnan+24","Whitler+25","Oesch+18","Finkelstein+15","Harikane+23"])

PATH_DIR1 = "/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/light_generation/data/"
PATH_DIR2 = "/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/column_density/data/"
def DoForFile(filepath1:str,filepath2:str,boxsize,label:str):
    data = np.loadtxt(PATH_DIR1+filepath1,usecols=(1,5))
    tgid,MAB = data.T
    tgid = np.int64(tgid)
    
    with open(PATH_DIR2+filepath2,"rb") as fp:
        clm_data:dict = pickle.load(fp)

    avail_tgid = clm_data.keys()
    avail_mask = [tg in avail_tgid for tg in tgid] 

    mtgid = tgid[avail_mask]
    mMAB = MAB[avail_mask]

    # N = np.array([clm_data[tg][0] for tg in mtgid])
    NZ = np.array([clm_data[tg][1] for tg in mtgid])
    kappa = 2e21
    epsilon = 15
    AVs = NZ/(kappa*epsilon)
    print(NZ)
    AUV = [de.get_extinction([1500],"Calzetti",Av)[0] for Av in AVs]

    for i,(mg,mA) in enumerate(zip(mtgid,AVs)):
        # print(mg,mA)
        if i>20:break

    mMAB_AV = mMAB + AUV
    # mMAB_AV = mMAB_AV[mMAB_AV< -16]

    bins=np.arange(-25,-15,1)

    h=0.6736
    bin_AB,bin_phi,error=gs.Utility.LumimosityFunction(mMAB,boxsize/h,bins)
    plt.gca().plot(bin_AB,bin_phi,'.-',label=f"ST+NB - {label}" )
    plt.fill_between(bin_AB,bin_phi-0.9*error,bin_phi+0.9*error,color='k',alpha=0.2,ec=None)

    bin_AB,bin_phi,error=gs.Utility.LumimosityFunction(mMAB_AV,boxsize/h,bins)
    plt.gca().plot(bin_AB,bin_phi,'.-',label=f"ST+NB+DE - {label}")
    plt.fill_between(bin_AB,bin_phi-0.9*error,bin_phi+0.9*error,color='k',alpha=0.2,ec=None)


 
DoForFile(f"out_L150N2040_z{REDSHIFT}p0_stnb_chabrier300_bin.csv",f"L150N2040_z{REDSHIFT}p00.dict",150,"L150N2040")
# DoForFile(f"out_L150N2040_WIND_WEAK_z{REDSHIFT}p0_stnb_chabrier300_bin.csv",f"L150N2040_WIND_WEAK_z{REDSHIFT}p00.dict",150,"L150N2040_WIND_WEAK")

# DoForFile("out_L250N2040_z7p0_stnb_chabrier300_bin.csv","L250N2040_z7p0_Av_a1p0.dict",250,"L250N2040")
# DoForFile("out_L250N2040_z7p0_stnb_chabrier300_bin.csv","L250N2040_z7p0_Av_a1p0_FS.dict",250,"L250N2040 (FS)")



# plt.xlim(-26,-15)
plt.yscale("log")
plt.xlabel("M_UV")
plt.ylabel("$\phi$")
plt.legend()
plt.title(f"z={REDSHIFT}")
plt.show()




# %%
