import galspy
import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from galspy.utility.Figure.Beautification import SetMyStyle
from galspy.utility.MassFunction import MassFunction,MassFunctionLiterature, LMF_OPTIONS
from matplotlib import ticker
import pickle
import matplotlib.lines as mlines


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
RECACHE = False

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


# =====================================
# Add plots
# =====================================
for i,z in enumerate(REDSHIFTS):
    # Select axis
    ax:plt.Axes = axs[i]
    box_hands=[]
    for simname,snapdir,clr in BOXES:
        
        # Get filepath
        filename = f"{simname}_hmf_z{str(np.round(z,2))}.txt"
        filepath = os.path.join(CURVE_CACHE_DIR,filename)

        # Cache curves if file doesn't exist or recache is true
        if not os.path.exists(filepath) or RECACHE:
            print("Caching",simname,"z=",z)
            snap_root = galspy.NavigationRoot(snapdir)
            snap_num  = snap_root.SnapNumFromZ(z)
            
            if not snap_num > -1:
                raise ValueError(f"Snapshot for redshift z={z} not found in directory:\n{snapdir}")

            pig = snap_root.PIG(snap_num)
            dm_mass = (pig.FOFGroups.MassByType().T)[1] * 1e10  #M_solar/h

            box_size = pig.Header.BoxSize()/1000    #Mpc/h
            M,phi,err = MassFunction(dm_mass,box_size) 

            np.savetxt(filepath,np.column_stack((M,phi,err)),header=f"Mass phi err; Munit=Mo/h; Lunit=Mpc/h; boxsize={box_size}Mpc/h")
        
        COSMOLOGY = {'flat': True,'H0': 67.36,'Om0': 0.3153,'Ob0': 0.0493,'sigma8': 0.811,'ns': 0.9649}

        # Box Mass Function
        M,phi,err = np.loadtxt(filepath).T
        # grad = np.gradient(phi)
        # mask1 = (grad<0)
        # M_ps,phi_ps = MassFunctionLiterature("Press-Schechter",COSMOLOGY,z,M,'dn/dlnM')
        # mask2 = phi>phi_ps
        # mask = mask1 & mask2
        if simname=="L150N2040":
            maskM=M>(32*1e10*0.00293499)
        if simname=="L250N2040":
            maskM=M>(32*1e10*0.0135179)
        maskP=phi>1e-7
        mask=maskM&maskP

        M,phi,err = M[mask],phi[mask],err[mask]
        hndl=ax.plot(M,phi,lw=2,c=clr,label=simname)
        box_hands.append(hndl[0])

        ax.fill_between(M,phi-0.9*err,phi+0.9*err,color=clr,alpha=0.2)



    # Literature Mass Function
    mass_hr     = np.logspace(MASS_RANGE[0],MASS_RANGE[-1],100)
    M,dn_dlogM = MassFunctionLiterature("Seith-Tormen",COSMOLOGY,z,mass_hr,'dn/dlnM')
    ax.plot(M,dn_dlogM,ls='--',c='k',lw=1,alpha=0.5)
    M,dn_dlogM = MassFunctionLiterature("Press-Schechter",COSMOLOGY,z,mass_hr,'dn/dlnM')
    ax.plot(M,dn_dlogM,ls=':',c='k',lw=1,alpha=0.5)


    # =====================================
    # Beautification
    # =====================================
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.xaxis.set_major_formatter(ticker.ScalarFormatter())
    ax.xaxis.set_minor_formatter(ticker.NullFormatter())
    ax.yaxis.set_major_formatter(ticker.ScalarFormatter())
    ax.yaxis.set_minor_formatter(ticker.NullFormatter())
    
    # set xticks only for last row
    ax.set_xlim(10**(7.5),10**(14.5))
    xticks = np.array([8,10,12,14])     # In log10 scale
    ax.set_xticks(10**xticks,[])
    if int(i/NCLMS)==(NROWS-1):
        ax.set_xticks(10**xticks,[f"$10^{{{xt}}}$" for xt in xticks],fontsize=14)
        ax.set_xlabel("Halo Mass $(M_\odot/$h$)$",fontsize=16)

    # set yticks only for first column
    ax.set_ylim(1e-8,1e4)
    yticks = np.array([-7,-5,-3,-1,1,3])     # In log10 scale
    ax.set_yticks(10.0**yticks,[])
    if int(i%NCLMS)==0:
        ax.set_yticks(10.0**yticks,[f"$10^{{{yt}}}$" for yt in yticks],fontsize=14)
        ax.set_ylabel(" $\phi$ (Mpc/h)$^{-3}$",fontsize=16)

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


