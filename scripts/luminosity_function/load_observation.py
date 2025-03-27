import numpy as np
import os
import matplotlib.pyplot as plt
from typing import Literal


OBS_DICT_HINT = Literal["Bouwens+21","Oesch+18","Donnan+24","Whitler+25"]

OBS_DATA_DIR = "/mnt/home/student/cranit/RANIT/Repo/galspy/obs/uvlf"
def load_to_axis(ax:plt.Axes,redshift,obs_key_list:OBS_DICT_HINT=[],label_suffix=""):
    ax.annotate(f"z={redshift:.01f}",(0,1),(8,-8),"axes fraction","offset pixels",ha="left",va="top",fontsize=14)
    for key in obs_key_list:
        filepath = OBS_DATA_DIR + os.sep + key +".txt"
        data = np.loadtxt(filepath)
        z,*_ = data.T
        mask = z==redshift
        z,MAB,Phi,MAB_n,MAB_p,Phi_n,Phi_p = data[mask].T
        ax.errorbar(MAB,Phi,yerr=[Phi_n,Phi_p],xerr=[MAB_n,MAB_p],
                    label=f"{key} {label_suffix}"
                    ,ls=' ',marker='.',capsize=3,ms=8)

