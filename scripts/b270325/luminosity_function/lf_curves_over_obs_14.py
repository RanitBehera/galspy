import matplotlib.pyplot as plt
import numpy as np
import galspy as gs
from matplotlib.gridspec import GridSpec
from typing import Literal


h=0.7



# Initialise Figure
# gs.SetPlotStyle()
fig = plt.figure(figsize=(12,8))
gsp = GridSpec(1,1,figure=fig)
# ax00 = fig.add_subplot(gsp[0,0])
# ax01 = fig.add_subplot(gsp[0,1])
# ax10 = fig.add_subplot(gsp[1,0])
ax11 = fig.add_subplot(gsp[0,0])

OBS_DATA_DIR = "/mnt/home/student/cranit/RANIT/Repo/galspy/obs/uvlf"
OBS_DICT_HINT = Literal["Bouwens+21","Oesch+18","Whitler+25","Donnan+24"]
OBS_DICT = {
    "Bouwens+21" : f"{OBS_DATA_DIR}/Bouwens+21.txt",
    "Oesch+18" : f"{OBS_DATA_DIR}/Oesch+18.txt",
    "Whitler+25" : f"{OBS_DATA_DIR}/Whitler+25.txt",
    "Donnan+24" : f"{OBS_DATA_DIR}/Donnan+24.txt",
}


def InitAxis(ax:plt.Axes,redshift,obs_key_list:OBS_DICT_HINT=[],label=""):
    ax.annotate(f"z={redshift:.01f}",(0,1),(8,-8),"axes fraction","offset pixels",ha="left",va="top",fontsize=14)
    ax.set_xlabel("$M_{AB}$")
    ax.set_ylabel("$\Phi$")
    # --------
    for key in obs_key_list:
        filepath = OBS_DICT[key]
        data = np.loadtxt(filepath)
        z,MAB,Phi,MAB_n,MAB_p,Phi_n,Phi_p = data.T
        mask = z==redshift
        z,MAB,Phi,MAB_n,MAB_p,Phi_n,Phi_p = z[mask],MAB[mask],Phi[mask],MAB_n[mask],MAB_p[mask],Phi_n[mask],Phi_p[mask]

        ax.errorbar(MAB,Phi,label=key + f" {label}",yerr=[Phi_n,Phi_p],xerr=[MAB_n,MAB_p],ls=' ',marker='.',capsize=3,ms=8)


# InitAxis(ax00,10,["Oesch+18"])
# InitAxis(ax01,9,["Bouwens+21"])
# InitAxis(ax10,8,["Bouwens+21"])
InitAxis(ax11,10,["Oesch+18","Whitler+25","Donnan+24"])
# InitAxis(ax11,9,["Donnan+24","Bouwens+21"])


# -------------------------
# NINJA
def DoforFile(filepath,label,boxsize_MPC,ax):

    table = np.loadtxt(filepath)
    M_AB = table.T[5]
    
    [print(mab) for mab in M_AB]
    
    bin_AB,bin_phi,error=gs.Utility.LumimosityFunction(M_AB,boxsize_MPC/h,10)
    XLF = log_L
    # YLF = np.log10(dn_dlogL)
    YLF = dn_dlogL
    ax.plot(XLF,YLF,'.-',label=label)
    plt.fill_between(XLF,YLF+error,YLF-error,color='k',alpha=0.2,ec=None)




for ax in [ax11]:
    ax.legend()
    ax.set_yscale("log")


DATA_DIR="/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/SPM3/data_26mar/"

# DoforFile(DATA_DIR + "out_L150N2040_z14p0_st_chabrier300_bin.csv","L150N2040 (ST)",150,ax11)
# DoforFile(DATA_DIR + "out_L150N2040_WIND_WEAK_z14p0_stnb_chabrier300_bin.csv","L150N2040_WW (ST+NB)",150,ax11)
DoforFile(DATA_DIR + "out_L150N2040_z10p0_stnb_chabrier300_bin.csv","L150N2040 (ST+NB)",150,ax11)
DoforFile(DATA_DIR + "out_L150N2040_WIND_WEAK_z10p0_stnb_chabrier300_bin.csv","L150N2040_WW (ST+NB)",150,ax11)

# DoforFile("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/SPM3/data_1/out_L150N2040_z9p0_stnb_chabrier300_bin.csv","150",150,ax11)
# DoforFile("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/SPM3/data_1/out_L250N2040_z9p0_stnb_chabrier300_bin.csv","250",250,ax11)
# DoforFile("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/SPM3/data_26mar/out_L150N2040_WIND_WEAK_z9p0_stnb_chabrier300_bin.csv","150WW",150,ax11)



plt.axvline(-19,color='k',ls='--',lw=1)
plt.legend()


plt.show()
