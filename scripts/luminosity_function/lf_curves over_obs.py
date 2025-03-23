import matplotlib.pyplot as plt
import numpy as np
import galspy as gs
from matplotlib.gridspec import GridSpec
from typing import Literal

# Initialise Figure
# gs.SetPlotStyle()
fig = plt.figure(figsize=(12,8))
gsp = GridSpec(2,2,figure=fig)
ax00 = fig.add_subplot(gsp[0,0])
ax01 = fig.add_subplot(gsp[0,1])
ax10 = fig.add_subplot(gsp[1,0])
ax11 = fig.add_subplot(gsp[1,1])

OBS_DATA_DIR = "/mnt/home/student/cranit/RANIT/Repo/galspy/obs/uvlf"
OBS_DICT_HINT = Literal["Bouwens+21","Oesch+18"]
OBS_DICT = {
    "Bouwens+21" : f"{OBS_DATA_DIR}/Bouwens+21.txt",
    "Oesch+18" : f"{OBS_DATA_DIR}/Oesch+18.txt"
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

        ax.errorbar(MAB,Phi,label=key + f" {label}",yerr=[Phi_n,Phi_p],ls=' ',marker='.',capsize=3,ms=8)


InitAxis(ax00,10,["Oesch+18"])
InitAxis(ax01,9,["Bouwens+21"])
InitAxis(ax10,8,["Bouwens+21"])
InitAxis(ax11,7,["Bouwens+21"])



# -------------------------
# NINJA
def DoforFile(filepath,label,boxsize_MPC,ax):
    table = np.loadtxt(filepath)
    M_AB = table.T[5]
    log_L,dn_dlogL,error=gs.Utility.LumimosityFunction(M_AB,boxsize_MPC/0.6736,0.5)
    log_L=log_L[1:-7]
    dn_dlogL=dn_dlogL[1:-7]

    XLF = log_L
    # YLF = np.log10(dn_dlogL)
    YLF = dn_dlogL
    ax.plot(XLF,YLF,'.-',label=label)



for ax in [ax00,ax01,ax10,ax11]:
    ax.legend()
    ax.set_yscale("log")


DoforFile("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/SPM3/data/out_L150N2040_z7p0_st_chabrier300_bin.csv","L150N2040 (ST)",150,ax11)
DoforFile("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/SPM3/data/out_L250N2040_z7p0_st_chabrier300_bin.csv","L250N2040 (ST)",250,ax11)

DoforFile("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/SPM3/data/out_L150N2040_z8p0_st_chabrier300_bin.csv","L150N2040 (ST)",150,ax10)
DoforFile("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/SPM3/data/out_L250N2040_z8p0_st_chabrier300_bin.csv","L250N2040 (ST)",250,ax10)

DoforFile("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/SPM3/data/out_L150N2040_z9p0_st_chabrier300_bin.csv","L150N2040 (ST)",150,ax01)
DoforFile("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/SPM3/data/out_L250N2040_z9p0_st_chabrier300_bin.csv","L250N2040 (ST)",250,ax01)

DoforFile("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/SPM3/data/out_L150N2040_z10p0_st_chabrier300_bin.csv","L150N2040 (ST)",150,ax00)
DoforFile("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/SPM3/data/out_L250N2040_z10p0_st_chabrier300_bin.csv","L250N2040 (ST)",250,ax00)






x = [-16.526785714285715, -17.1875, -18.276785714285715, -19.151785714285715, -20.1875, -21.13392857142857, -21.50892857142857, -21.803571428571427, -22.151785714285715, -22.50892857142857, -23.473214285714285, -23.848214285714285, -23.955357142857142]
y = [-2.2781954887218046, -2.5338345864661656, -2.984962406015038, -3.3533834586466167, -3.8646616541353387, -4.360902255639098, -4.571428571428571, -4.7894736842105265, -4.93984962406015, -5.180451127819548, -6.007518796992481, -6.12781954887218, -6.285714285714286]
x=np.array(x)
y=np.array(y)
ax11.plot(x,10**y,':',label="Astrid")








ax00.legend()

plt.show()
