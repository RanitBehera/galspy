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


SetMyStyle()
NROWS,NCLMS = 1,2
fig=plt.figure(figsize=np.array((NCLMS,NROWS))*4)
gs = GridSpec(NROWS,NCLMS)
axs = [plt.subplot(gs[i, j]) for i in range(NROWS) for j in range(NCLMS)]
fig.subplots_adjust(hspace=0.05,wspace=0.05)
# fig.tight_layout()


TABLE_PATH = "/mnt/home/student/cranit/RANIT/Repo/galspy/scripts_2/galaxy_statistics/data"



# Redshifts
def Plot(i,BOX,Z,boxsize_mpc):
    ax:plt.Axes=axs[i]
    GID,GMDM,GMST,GMBH,NST,NBH,bh_acc,Mdot_edd,L_edd = np.loadtxt(TABLE_PATH +os.sep+f"table1_{BOX}_{Z}.txt").T
    GID_p,MAB_ST_p,MAB_ST_RED_p,MAB_TOT_p,MAB_TOT_RED_p,beta_ST_p,beta_ST_RED_p,beta_TOT_p,beta_TOT_RED_p = np.loadtxt(TABLE_PATH +os.sep+f"table2_primordial_{BOX}_{Z}.txt").T
    MAB_ks = np.loadtxt(f"/mnt/home/student/cranit/RANIT/Repo/galspy/study/LuvAB/MUVAB_SFR_{BOX}_z{Z}.txt")
    # ==============

    h=0.6736
    boxsize_mpc=boxsize_mpc/h
    # M,phi,err = LuminosityFunction(MAB_ks,(boxsize_mpc)**3,0.5)
    # mask=(M< -18)&(M> -27)&(phi>1e-6)
    # M,phi,err=M[mask],phi[mask],err[mask]
    # ax.plot(M,phi,label="Scaling",c='k')
    # ==============
    M,phi,err = LuminosityFunction(MAB_ST_p,(boxsize_mpc)**3,0.5)
    mask=(M< -18)&(M> -23)&(phi>1e-7)
    M,phi,err=M[mask],phi[mask],err[mask]
    # M,phi=M[:-skip1],phi[:-skip1]
    ax.plot(M,phi,label="Stellar Only",c='deepskyblue')

    M,phi,err = LuminosityFunction(MAB_TOT_p,(boxsize_mpc)**3,0.5)
    mask=(M< -18)&(M> -23)&(phi>1e-7)
    M,phi,err=M[mask],phi[mask],err[mask]
    # M,phi=M[:-skip2],phi[:-skip2]
    ax.plot(M,phi,label="+ Nebular (Primorial)",c="orange")



    # ==============
    ax.set_yscale("log")
    ax.xaxis.set_major_formatter(ticker.ScalarFormatter())
    ax.xaxis.set_minor_formatter(ticker.NullFormatter())
    ax.yaxis.set_major_formatter(ticker.ScalarFormatter())
    ax.yaxis.set_minor_formatter(ticker.NullFormatter())

    ax.xaxis.set_tick_params(which="major",direction="in",top=True,pad=4)
    ax.yaxis.set_tick_params(which="major",direction="in",right=True,pad=4)
    ax.xaxis.set_tick_params(which="minor",direction="in",bottom=False,pad=4)
    ax.yaxis.set_tick_params(which="minor",direction="in",bottom=False,pad=4)
    
    ax.set_ylim(0.8e-8,2e-2)
    yticks = np.array([-7,-6,-5,-4,-3,-2])     # In log10 scale
    ax.set_yticks(10.0**yticks,[])
    if int(i%NCLMS)==0:
        ax.set_yticks(10.0**yticks,[f"$10^{{{yt}}}$" for yt in yticks],fontsize=14)
        ax.set_ylabel("$\Phi$ (mag$^{-1}$ Mpc$^{-3}$)",fontsize=16)

    ax.set_xlim(-24,-18)
    xticks = np.array([-23,-22,-21,-20,-19])     # In log10 scale
    ax.set_xticks(xticks,[])
    if int(i/NCLMS)==(NROWS-1):
        ax.set_xticks(xticks,[str(xt) for xt in xticks],fontsize=14)
        ax.set_xlabel("$M_{{{UV}}}$",fontsize=16)
    ax.invert_xaxis()

    ax.annotate(f"z={Z}",xy=(0,1),xytext=(8,-8),xycoords="axes fraction",textcoords="offset pixels",va="top",ha="left",fontsize=14)
    return


Plot(0,"L150N2040",8,150)
Plot(1,"L150N2040",9,150)
# Plot(2,"L150N2040",10,150)
# Plot(0,"L250N2040",8,250)
# Plot(1,"L250N2040",9,250)
# Plot(2,"L250N2040",10,250)


line_so = mlines.Line2D([], [], color='deepskyblue',ls='-', marker=' ',markersize=8, label="Stellar Only")
line_nb = mlines.Line2D([], [], color='orange',ls='-',marker=' ',markersize=8, label="Stellar + Nebular (Primordial)")
# linep_md = mlines.Line2D([], [], color='k',ls='-',marker=' ',markersize=8, label="Madau-Dickinson Scaling")
extra_hands = [line_so,line_nb]
# leg=ax.legend(handles=extra_hands,fontsize=12, loc='upper right',ncol=1,frameon=False,bbox_to_anchor=(1,0.8),markerfirst=False)
# ax.add_artist(leg)

axs[0].figure.legend(handles=extra_hands,loc='upper center',frameon=False,bbox_to_anchor=(0.5,1),ncols=5,fontsize=12)











# OBS
# z=8, 
MUV = np.array([-21.35,-20.85,-20.35,-19.85,-19.35,-18.60])
phi=np.array([2.277,9.974,13.12,28.64,54.04,69.35])*1e-5
err_phi = np.array([1.226,3.137,3.840,7.247,22.19,28.41])*(1e-5)
adams=axs[0].errorbar(MUV,phi,err_phi,fmt='.',capsize=4,label="Adams et al. (2024)")

MUV = np.array([-22.17,-21.42])
phi=np.array([0.63,3.92])*1e-6
err_phip = np.array([0.50,2.34])*(1e-6)
err_phin = np.array([0.30,1.56])*(1e-6)
donnan=axs[0].errorbar(MUV,phi,(err_phin,err_phip),fmt='.',capsize=4,label="Donnan et al. (2023)",color='darkred')

# MUV = np.array([-22.2,-21.2])
# phi = np.array([5.3e-7, 1.3e-5])
# err_phip = np.array([5.2e-7,3.1e-5])
# err_phin = np.array([2.9e-7,1.2e-5])
# harikane=axs[0].errorbar(MUV,phi,(err_phin,err_phip),fmt='.',capsize=4,label="Harikane et al. (2024)",color='darkgreen')

# z=9, 
MUV = np.array([-22.05,-21.55,-21.05,-20.55,-20.05,-19.55,-18.80])
phi=np.array([0.628,0.628,1.257,6.427,10.76,18.22,42.45])*1e-5
err_phi = np.array([0.536,0.536,0.851,2.534,5.825,9.442,20.32])*(1e-5)
axs[1].errorbar(MUV,phi,err_phi,fmt='.',capsize=4,label="Adams et al. (2024)")

MUV = np.array([-22.30,-21.30])
phi=np.array([0.17,3.02])*1e-6
err_phip = np.array([0.40,3.98])*(1e-6)
err_phin = np.array([0.14,1.95])*(1e-6)
axs[1].errorbar(MUV,phi,(err_phin,err_phip),fmt='.',capsize=4,label="Donnan et al. (2023)",color='darkred')

# MUV = np.array([-22.0,-21.0,-20.0,-19.0])
# phi = np.array([6.6,5.1,2.9,3.5])*(1e-6)
# err_phip = np.array([7.1,7.0,3.2,3.7])*(1e-6)
# err_phin = np.array([4.7,3.8,2.2,2.4])*(1e-6)
# axs[1].errorbar(MUV,phi,(err_phin,err_phip),fmt='.',capsize=4,label="Harikane et al. (2024)",color='darkgreen')


# # z=10
# MUV = np.array([-23.5,-21.6,-20.6,-19.6,-18.6,-17.6])
# phi = np.array([6.8e-8,1.0e-6,8.7e-6,2.6e-5,1.9e-4,6.3e-4])
# err_phip = np.array([0,2.3e-6,20.5e-6,2.8e-5,4.7e-4,15.8e-4])
# err_phin = np.array([0,0.9e-6,8.4e-6,1.8e-5,1.9e-4,6.3e-4])
# axs[2].errorbar(MUV,phi,(err_phin,err_phip),fmt='.',capsize=4,label="Harikane et al. (2024)",color='darkgreen')






leg=axs[0].legend(handles=[adams],fontsize=12, loc='upper right',ncol=1,frameon=False,bbox_to_anchor=(1,1),markerfirst=False)
leg=axs[1].legend(handles=[donnan],fontsize=12, loc='upper right',ncol=1,frameon=False,bbox_to_anchor=(1,1),markerfirst=False)
plt.subplots_adjust(bottom=0.2,left=0.15,right=0.98)
plt.show()


###### NOTE THE < or > signs in the phi values in the Harikane PAPER!!