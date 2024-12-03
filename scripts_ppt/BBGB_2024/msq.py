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


# =====================================
# PARAMETERS
# =====================================
# Axis numbers in the figure
NROWS,NCLMS = 2,3
# 
BOXES = [
    ["L150N2040","/mnt/home/student/cranit/NINJA/simulations/L150N2040/SNAPS/","deepskyblue"],
    ["L250N2040","/mnt/home/student/cranit/NINJA/simulations/L250N2040/SNAPS/","deeppink"]
]
# Curves will be cached here if not available for quick plot in future
CURVE_CACHE_DIR = "/mnt/home/student/cranit/RANIT/Repo/galspy/scripts_ppt/BBGB_2024/data"
RECACHE = True

# Redshifts in axes, will be filled row wise first
REDSHIFTS = [10,9,8,7,6,5]
MASS_RANGE = [7.5,14.5]

# =====================================
# Initialize with Blank Frames
# =====================================
SetMyStyle()
fig=plt.figure(figsize=np.array((NCLMS,NROWS))*3)
gs = GridSpec(NROWS,NCLMS)
axs = [plt.subplot(gs[i, j]) for i in range(NROWS) for j in range(NCLMS)]
fig.subplots_adjust(hspace=0.05,wspace=0.05)
# fig.tight_layout()



# ===========================================
# =========== OBSERVATIONAL FITS ============
# ===========================================
# Calabro et al. (2024)
# https://arxiv.org/abs/2402.17829v1
# Table 1 (3rd row) and Figure 4
def Calabro2024_Fit(M):
    m=0.76
    q=-6.0
    log_M = np.log10(M)
    x=log_M
    y = m*x + q
    log_SFR = y
    SFR = 10**log_SFR
    return M,SFR

# -------------------------------------------
# Schreiber et al. (2014)
# https://arxiv.org/abs/1409.5433
# Equation 9
def Schreiber2014_Fit(M,z):
    M=np.array(M)
    m = np.log10(M/1e9) 
    m0=0.5
    a0=1.5
    a1=0.3
    m1=0.36
    a2=2.5
    r=np.log10(1+z)

    def Fit(m):
        return (m - m0 + a0*r - a1*(np.max([0,m-m1-a2*r]))**2)
    
    log_SFR = np.array([Fit(mi) for mi in m])
    SFR = 10**log_SFR
    return M,SFR



# -------------------------------------------
# Speagle et al. (2014)
# https://arxiv.org/abs/1405.2041
# Abstract
def Speagle2014_Fit(M,t):
    # t in Gyr
    slope = 0.84 - 0.026*t
    offset = 6.51 - 0.11*t
    log_SFR = slope * np.log10(M) - offset
    SFR = 10**log_SFR
    return M,SFR



# =====================================
# Add plots
# =====================================
for i,z in enumerate(REDSHIFTS):
    # Select axis
    ax:plt.Axes = axs[i]
    box_hands=[]
    for simname,snapdir,clr in BOXES:
        
        # Get filepath
        filename = f"{simname}_msq_z{str(np.round(z,2))}.txt"
        filepath = os.path.join(CURVE_CACHE_DIR,filename)

        # Cache curves if file doesn't exist or recache is true
        if not os.path.exists(filepath) or RECACHE:
            print("Caching",simname,"z=",z)
            snap_root = galspy.NavigationRoot(snapdir)
            snap_num  = snap_root.SnapNumFromZ(z)
            
            if not snap_num > -1:
                raise ValueError(f"Snapshot for redshift z={z} not found in directory:\n{snapdir}")

            h=1
            pig = snap_root.PIG(snap_num)
            star_mass = (pig.FOFGroups.MassByType().T)[4] * (1e10/h)  #M_solar
            sfr = pig.FOFGroups.StarFormationRate().T
            # sfr*=(1e10/3.08568e+16) * 365 * 24 * 3600 # M_sun /year
            halo_mass       = pig.FOFGroups.Mass() * (1e10/h)

            np.savetxt(filepath,np.column_stack((star_mass,sfr,halo_mass)),header=f"M_star SFR M_halo; Munit=Mo; SFRUnit=Mo/yr;")
        

        # Box Mass Function
        Mstar,sfr,Mhalo = np.loadtxt(filepath).T
        z_to_mask = {5:3e11,6:2e11,7:1e11,8:9e10,9:8e10,10:7e10}
        mask_lim=z_to_mask[int(z)]
        mask1 = (Mhalo>mask_lim)
        mask2 = (Mstar>0)
        mask = mask1 & mask2
        Mstar = Mstar[mask]
        sfr = sfr[mask]

        ax.plot(Mstar,sfr,'.',ms=2,c=clr)

        # Observational
        M=np.logspace(6,11,100)
        M,SFR = Calabro2024_Fit(M)
        ax.plot(M,SFR)

        M,SFR = Schreiber2014_Fit(M,z)
        ax.plot(M,SFR)

        cosmo = FlatLambdaCDM(H0=67.36, Om0=0.3153)
        # atropy lookbacktime in in Gyrs
        lbt_inf = cosmo.lookback_time(999999)
        lbt_z = cosmo.lookback_time(z)
        age = (lbt_inf -lbt_z).value

        M,SFR = Speagle2014_Fit(M,age)
        ax.plot(M,SFR)



    # =====================================
    # Beautification
    # =====================================
    ax.set_xscale("log")
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


