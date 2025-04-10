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


# Light
data = np.loadtxt("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/light_generation/data/out_L150N2040_z7p0_stnb_chabrier300_bin.csv",usecols=(1,5))
tgid,MAB = data.T
tgid = np.int64(tgid)

PATH_DIR = "/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/column_density/data/"
def DoForFile(filepath:str):
    with open(PATH_DIR+filepath,"rb") as fp:
        clm_data:dict = pickle.load(fp)

    avail_tgid = clm_data.keys()
    avail_mask = [tg in avail_tgid for tg in tgid] 

    mtgid = tgid[avail_mask]
    mMAB = MAB[avail_mask]

    AVs = np.array([clm_data[tg][1] for tg in mtgid])
    AUV = [de.get_extinction([1500],"Calzetti",Av)[0] for Av in AVs]

    for i,(mg,mA) in enumerate(zip(mtgid,AVs)):
        print(mg,mA)
        if i>20:break

    mMAB_AV = mMAB + AUV
    mMAB_AV = mMAB_AV[mMAB_AV<-16]

    load_obs_to_axis(plt.gca(),7,["Bouwens+21","Donnan+24","Whitler+25","Oesch+18","Finkelstein+15"])

    h=0.6736
    bin_AB,bin_phi,error=gs.Utility.LumimosityFunction(mMAB,150/h,20)
    plt.gca().plot(bin_AB,bin_phi,'.-',label=f"ST+NB")
    bin_AB,bin_phi,error=gs.Utility.LumimosityFunction(mMAB_AV,150/h,15)
    plt.gca().plot(bin_AB,bin_phi,'.-',label=f"ST+NB+DE")


    plt.xlim(-26,-15)
    plt.yscale("log")
    plt.xlabel("M_UV")
    plt.ylabel("$\phi$")
    plt.legend()
    plt.title("z=7 (with (1+z); kappa=3e22 ; Av=Av)")
    plt.show()





DoForFile("L150N2040_z7p0_Av_a1p0_with_z.dict")

# %%
