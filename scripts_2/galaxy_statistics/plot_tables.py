import galspy
import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from galspy.utility.Figure.Beautification import SetMyStyle
from matplotlib import ticker
import pickle
import matplotlib.lines as mlines
from astropy.cosmology import FlatLambdaCDM
from galspec.Utility import LuminosityFunction


# =====================================
# PARAMETERS
# =====================================
# Axis numbers in the figure
NROWS,NCLMS = 1,3
# 
BOXES = [
    ["L150N2040","deepskyblue"],
    ["L250N2040","deeppink"]
]

CACHE_DIR = "/mnt/home/student/cranit/RANIT/Repo/galspy/scripts_2/galaxy_statistics/data"

# Redshifts in axes, will be filled row wise first
REDSHIFTS = [10,9,8]

# =====================================
# Initialize with Blank Frames
# =====================================
SetMyStyle()
fig=plt.figure(figsize=np.array((NCLMS,NROWS))*3)
gs = GridSpec(NROWS,NCLMS)
axs = [plt.subplot(gs[i, j]) for i in range(NROWS) for j in range(NCLMS)]
fig.subplots_adjust(hspace=0.05,wspace=0.05)
# fig.tight_layout()






# ======================/mnt/home/student/cranit/RANIT/Repo/galspy/scripts_2/galaxy_statistics/data===============
# Add plots
# =====================================
for i,z in enumerate(REDSHIFTS):
    # Select axis
    ax:plt.Axes = axs[i]

    # Get filepath
    filename = f"table2_primordial_L150N2040_{z}.txt"
    filepath = os.path.join(CACHE_DIR,filename)

    # Cache curves if file doesn't exist or recache is true
    
    GID,GMDM,GMST,GMBH,NST,NBH,bh_acc,Mdot_edd,L_edd = np.loadtxt("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts_2/galaxy_statistics/data_old"+os.sep+"table1.txt").T
    GID_p,MAB_ST_p,MAB_ST_RED_p,MAB_TOT_p,MAB_TOT_RED_p,beta_ST_p,beta_ST_RED_p,beta_TOT_p,beta_TOT_RED_p = np.loadtxt(filepath).T

    MAB_ks = np.loadtxt("/mnt/home/student/cranit/RANIT/Repo/galspy/study/LuvAB/MUVAB_SFR.txt")

        
    h=0.6736
    M,phi,err = LuminosityFunction(MAB_ks,(150/h)**3,0.5)
    mask=(M< -18)&(M> -27)&(phi>1e-9)
    M,phi,err=M[mask],phi[mask],err[mask]
    plt.plot(M,phi,label="MD")

    M,phi,err = LuminosityFunction(MAB_TOT_p,(150/h)**3,0.5)
    mask=(M< -18)&(M> -27)&(phi>1e-9)
    M,phi,err=M[mask],phi[mask],err[mask]
    plt.plot(M,phi,label="+ Nebular (primorial)")


    # =====================================
    # Beautification
    # =====================================
    # ax.set_xscale("log")
    ax.set_yscale("log")
    ax.xaxis.set_major_formatter(ticker.ScalarFormatter())
    ax.xaxis.set_minor_formatter(ticker.NullFormatter())
    ax.yaxis.set_major_formatter(ticker.ScalarFormatter())
    ax.yaxis.set_minor_formatter(ticker.NullFormatter())
    continue
    # set xticks only for last row
    ax.set_xlim(10**(7.5),10**(14.5))
    xticks = np.array([8,10,12,14])     # In log10 scale
    ax.set_xticks(10**xticks,[])
    if int(i/NCLMS)==(NROWS-1):
        ax.set_xticks(10**xticks,[f"$10^{{{xt}}}$" for xt in xticks],fontsize=14)
        ax.set_xlabel("Stellar Mass $(M_\odot/$h$)$",fontsize=16)

    # set yticks only for first column
    ax.set_ylim(1e-8,1e4)
    yticks = np.array([-7,-5,-3,-1,1,3])     # In log10 scale
    ax.set_yticks(10.0**yticks,[])
    if int(i%NCLMS)==0:
        ax.set_yticks(10.0**yticks,[f"$10^{{{yt}}}$" for yt in yticks],fontsize=14)
        ax.set_ylabel("SFR",fontsize=16)

    ax.xaxis.set_tick_params(which="major",direction="in",top=True,pad=4)
    ax.yaxis.set_tick_params(which="major",direction="in",right=True,pad=4)
    ax.xaxis.set_tick_params(which="minor",direction="in",bottom=False,pad=4)
    ax.yaxis.set_tick_params(which="minor",direction="in",bottom=False,pad=4)



    ax.grid(alpha=0.2)
    ax.annotate(f"$z$={z}",xy=(0,1),xytext=(12,-12),xycoords="axes fraction",textcoords="offset pixels",ha="left",va="top",fontsize=16)
    if i==1:
        leg=ax.legend(handles=box_hands,fontsize=12, loc='upper right',ncol=1,frameon=False,bbox_to_anchor=(1,1),markerfirst=False)
    if i==1:
        linest = mlines.Line2D([], [], color='k',ls='--', marker=' ',markersize=8, label="Seith-Tormen")
        lineps = mlines.Line2D([], [], color='k',ls=':',marker=' ',markersize=8, label="Press-Schechter")
        extra_hands = [linest,lineps]
        # leg=ax.legend(handles=extra_hands,fontsize=12, loc='upper right',ncol=1,frameon=False,bbox_to_anchor=(1,0.8),markerfirst=False)
        # ax.add_artist(leg)

        ax.figure.legend(handles=extra_hands,loc='upper center',frameon=False,bbox_to_anchor=(0.5,0.95),ncols=5,fontsize=14)


plt.show()





















































exit()





GID,GMDM,GMST,GMBH,NST,NBH,bh_acc,Mdot_edd,L_edd = np.loadtxt("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts_2/galaxy_statistics/data/table1.txt").T
GID_s,MAB_ST_s,MAB_ST_RED_s,MAB_TOT_s,MAB_TOT_RED_s,beta_ST_s,beta_ST_RED_s,beta_TOT_s,beta_TOT_RED_s = np.loadtxt("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts_2/galaxy_statistics/data/table2_solar.txt").T
GID_p,MAB_ST_p,MAB_ST_RED_p,MAB_TOT_p,MAB_TOT_RED_p,beta_ST_p,beta_ST_RED_p,beta_TOT_p,beta_TOT_RED_p = np.loadtxt("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts_2/galaxy_statistics/data/table2_primordial.txt").T

MAB_ks = np.loadtxt("/mnt/home/student/cranit/RANIT/Repo/galspy/study/LuvAB/MUVAB_SFR.txt")

# Luminosity functions
from galspec.Utility import LuminosityFunction
plt.figure()
#
h=0.6736
M,phi,err = LuminosityFunction(MAB_ks,(150/h)**3,0.5)
mask=(M< -18)&(M> -27)&(phi>1e-9)
M,phi,err=M[mask],phi[mask],err[mask]
plt.plot(M,phi,label="MD")
#
M,phi,err = LuminosityFunction(MAB_ST_s,(150/h)**3,0.5)
mask=(M< -18)&(M> -27)&(phi>1e-9)
M,phi,err=M[mask],phi[mask],err[mask]
plt.plot(M,phi,label="Stellar (solar)")


M,phi,err = LuminosityFunction(MAB_TOT_p,(150/h)**3,0.5)
mask=(M< -18)&(M> -27)&(phi>1e-9)
M,phi,err=M[mask],phi[mask],err[mask]
plt.plot(M,phi,label="+ Nebular (primorial)")

M,phi,err = LuminosityFunction(MAB_TOT_RED_p,(150/h)**3,0.5)
mask=(M< -18)&(M> -27)&(phi>1e-9)
M,phi,err=M[mask],phi[mask],err[mask]
plt.plot(M,phi,label="+ Reddened (primorial)")




# Observational
obs = np.genfromtxt("/mnt/home/student/cranit/RANIT/Repo/galspy/obs/uvlf/uvlf.txt",dtype=None,encoding='utf-8')
obs = np.array([list(row) for row in obs],dtype=object)

MAB = obs[:,3]
phi_exp = obs[:,9]
phi = obs[:,6] * (10.**phi_exp)
phi_p = obs[:,7] * (10.**phi_exp)
phi_n = -obs[:,8] * (10.**phi_exp)

plt.errorbar(MAB,phi,(phi_n,phi_p),fmt='.',capsize=4)


# Beta function
# plt.plot(GMST[:33179],beta_ST_p,'.',label="Stellar")
# plt.plot(GMST[:33179],beta_TOT_p,'.',label="Tottal")

# ===
# edd_rat = bh_acc / Mdot_edd
# edd_rat = edd_rat[:33179]
# mask = edd_rat>0.01

# # plt.plot(GMST,edd_rat,'.')

# plt.plot(GMST[:33179],MAB_TOT_p,'.',c='g')
# plt.plot(GMST[:33179][mask],MAB_TOT_p[mask],'.',c='r',ms=10)




# plt.axhline(-2.4)
plt.legend()
# plt.xscale("log")
plt.yscale("log")
plt.show()

