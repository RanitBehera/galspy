import matplotlib.pyplot as plt
import numpy as np
import galspy as gs
from matplotlib.gridspec import GridSpec
from typing import Literal

# Initialise Figure
gs.SetPlotStyle()
fig = plt.figure(figsize=(12,8))
gs = GridSpec(2,2,figure=fig)
ax00 = fig.add_subplot(gs[0,0])
ax01 = fig.add_subplot(gs[0,1])
ax10 = fig.add_subplot(gs[1,0])
ax11 = fig.add_subplot(gs[1,1])

OBS_DATA_DIR = "/mnt/home/student/cranit/RANIT/Repo/galspy/obs/uvlf"
OBS_DICT_HINT = Literal["Bouwens+21","Oesch+18"]
OBS_DICT = {
    "Bouwens+21" : f"{OBS_DATA_DIR}/Bouwens+21.txt",
    "Oesch+18" : f"{OBS_DATA_DIR}/Oesch+18.txt"
}


def InitAxis(ax:plt.Axes,redshift,obs_key_list:OBS_DICT_HINT=[]):
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

        ax.errorbar(MAB,Phi,label=key,yerr=[Phi_n,Phi_p],ls=' ',marker='.',capsize=3,ms=8)


InitAxis(ax00,10,["Oesch+18"])
InitAxis(ax01,9,["Bouwens+21"])
InitAxis(ax10,8,["Bouwens+21"])
InitAxis(ax11,7,["Bouwens+21"])

for ax in [ax00,ax01,ax10,ax11]:
    ax.legend()
    ax.set_yscale("log")























plt.show()
