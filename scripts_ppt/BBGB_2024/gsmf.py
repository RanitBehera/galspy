import galspy
import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from galspy.utility.Figure.Beautification import SetMyStyle
from galspy.utility.MassFunction import MassFunction
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

# =====================================
# Initialize with Blank Frames
# =====================================
SetMyStyle()
fig=plt.figure(figsize=np.array((NCLMS,NROWS))*4)
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
        filename = f"{simname}_gsmf_z{str(np.round(z,2))}.txt"
        filepath = os.path.join(CURVE_CACHE_DIR,filename)

        # Cache curves if file doesn't exist or recache is true
        if not os.path.exists(filepath) or RECACHE:
            snap_root = galspy.NavigationRoot(snapdir)
            snap_num  = snap_root.SnapNumFromZ(z)
            
            if not snap_num > -1:
                raise ValueError(f"Snapshot for redshift z={z} not found in directory:\n{snapdir}")

            pig = snap_root.PIG(snap_num)
            sm_mass = (pig.FOFGroups.MassByType().T)[4] * 1e10

            box_size = pig.Header.BoxSize()/1000    #Mpc/h
            M,phi,err = MassFunction(sm_mass,box_size) 

            np.savetxt(filepath,np.column_stack((M,phi,err)),header=f"Mass phi err; Munit=Mo/h; Lunit=Mpc/h; boxsize={box_size}Mpc/h")
        

        # Box Mass Function
        M,phi,err = np.loadtxt(filepath).T
        grad = np.gradient(phi)
        mask1 = grad<0
        mask2 = phi>1e-7
        mask = mask1&mask2
        M,phi,err = M[mask],phi[mask],err[mask]
        hndl=ax.plot(M,phi,lw=2,c=clr,label=simname)
        box_hands.append(hndl[0])

        # ax.fill_between(M,phi-0.9*err,phi+0.9*err,color=clr,alpha=0.2)

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
    ax.set_xlim(10**(5),10**(12))
    xticks = np.array([6,7,8,9,10,11])     # In log10 scale
    ax.set_xticks(10**xticks,[])
    if int(i/NCLMS)==(NROWS-1):
        ax.set_xticks(10**xticks,[f"$10^{{{xt}}}$" for xt in xticks],fontsize=14)
        ax.set_xlabel("Stellar Mass $(M_\odot/$h$)$",fontsize=16)

    # set yticks only for first column
    ax.set_ylim(1e-8,1.5e1)
    yticks = np.array([-7,-5,-3,-1,1])     # In log10 scale
    ax.set_yticks(10.0**yticks,[])
    if int(i%NCLMS)==0:
        ax.set_yticks(10.0**yticks,[f"$10^{{{yt}}}$" for yt in yticks],fontsize=14)
        ax.set_ylabel(" $\phi$ (Mpc/h)$^{-1}$",fontsize=16)

    ax.xaxis.set_tick_params(which="major",direction="in",top=True,pad=4)
    ax.yaxis.set_tick_params(which="major",direction="in",right=True,pad=4)
    ax.xaxis.set_tick_params(which="minor",direction="in",bottom=False,pad=4)
    ax.yaxis.set_tick_params(which="minor",direction="in",bottom=False,pad=4)

    ax.grid(alpha=0.2)
    ax.annotate(f"$z$={z}",xy=(0,1),xytext=(12,-12),xycoords="axes fraction",textcoords="offset pixels",ha="left",va="top",fontsize=16)
    if i==1:
        leg=ax.legend(handles=box_hands,fontsize=14, loc='upper right',ncol=1,frameon=False,bbox_to_anchor=(1,1),markerfirst=False)



# =====================================
# Add Observations
# =====================================
z10 = axs[0]
z9 = axs[1]
z8 = axs[2]
z7 = axs[3]
z6 = axs[4]
z5 = axs[5]

z10_hands=[]
z9_hands=[]
z8_hands=[]
z7_hands=[]
z6_hands=[]
z5_hands=[]

h=0.6736

# https://arxiv.org/pdf/1507.05636
CLR = (0.7,0,0)
M=10**np.arange(7.25,11.30,0.5)*h


p7=10**np.array([-1.63,-2.07,-2.49,-2.96,-3.47,-4.11,-4.61,-5.24])
p7p=p7*(10**np.array([0.54,0.45,0.38,0.32,0.32,0.41,0.72,0.90])-1)
p7n=p7*(1-1/10**np.array([0.54,0.41,0.32,0.30,0.35,0.57,0.82,0.57]))
song2016=z7.errorbar(M[:len(p7)],p7,[p7n,p7p],fmt='o',capsize=4,color=CLR,ms=5,label="Song et al. (2016)")
z7_hands.append(song2016)

p8=10**np.array([-1.73,-2.28,-2.88,-3.45,-4.21,-5.31])
p8p=p8*(10**np.array([1.01,0.84,0.75,0.57,0.63,1.01])-1)
p8n=p8*(1-1/10**np.array([0.84,0.64,0.57,0.60,0.78,1.64]))
z8.errorbar(M[:len(p8)],p8,[p8n,p8p],fmt='o',capsize=4,color=CLR,ms=4)
z8_hands.append(song2016)









# # https://arxiv.org/pdf/2111.01160
# CLR = (0,0.6,0.25)

# M=10**np.array([7.75,8.25,8.70,9.10,9.50,9.90,10.30])*h
# Merrp=M*(10**np.array([0.25,0.25,0.20,0.20,0.20,0.20,0.20])-1)
# Merrn=M*(1-1/10**np.array([0.25,0.25,0.20,0.20,0.20,0.20,0.20]))
# p7=np.array([71.7,39.4,13.2,7.70,3.18,1.68,0.104])*1e-4
# p7p=np.array([23.7,6.9,2.7,1.67,0.88,0.63,0.240])*1e-4
# p7n=np.array([18.3,6.3,2.4,1.49,0.78,0.53,0.090])*1e-4
# stefanon2021=z7.errorbar(M,p7,[p7n,p7p],[Merrn,Merrp],fmt='o',capsize=4,color=CLR,ms=4)

# M=10**np.array([7.90,8.40,8.90,9.35,9.75,10.15])*h
# Merrp=M*(10**np.array([0.25,0.25,0.25,0.20,0.20,0.20])-1)
# Merrn=M*(1-1/10**np.array([0.25,0.25,0.25,0.20,0.20,0.20]))
# p8=np.array([41.9,8.91,3.56,1.11,0.591,0.0711])*1e-4
# p8p=np.array([20.6,2.49,1.19,0.57,0.371,0.1637])*1e-4
# p8n=np.array([14.5,2.08,0.95,0.42,0.262,0.0617])*1e-4
# z8.errorbar(M,p8,[p8n,p8p],[Merrn,Merrp],fmt='o',capsize=4,color=CLR,ms=4)

# M=10**np.array([7.50,8.25,8.75,9.50])*h
# Merrp=M*(10**np.array([0.50,0.25,0.25,0.50])-1)
# Merrn=M*(1-1/10**np.array([0.50,0.25,0.25,0.50]))
# p9=np.array([29.1,3.67,0.738,0.0764])*1e-4
# p9p=np.array([23.0,2.93,0.348,0.1016])*1e-4
# p9n=np.array([13.9,1.81,0.256,0.0517])*1e-4
# z9.errorbar(M,p9,[p9n,p9p],[Merrn,Merrp],fmt='o',capsize=4,color=CLR,ms=4)


# M=10**np.array([7.65,8.25,8.75])*h
# Merrp=M*(10**np.array([0.35,0.25,0.25])-1)
# Merrn=M*(1-1/10**np.array([0.35,0.25,0.25]))
# p10=np.array([12.0,0.264,0.0872])*1e-4
# p10p=np.array([15.8,0.258,0.1997])*1e-4
# p10n=np.array([7.8,0.146,0.0729])*1e-4
# z10.errorbar(M,p10,[p10n,p10p],[Merrn,Merrp],fmt='o',capsize=4,color=CLR,ms=4)


# # https://arxiv.org/pdf/2403.08872
# CLR = (0.25,0.5,1.0)

# M=10**np.arange(8.25,11.80,0.5)*h
# p7=10**np.array([-2.40,-2.70,-3.35,-3.96,-4.35,-4.78,-5.38,-5.69])
# p7p=p7*(10**np.array([0.15,0.14,0.14,0.19,0.25,0.38,0.43,0.55])-1)
# p7n=p7*(1-1/10**np.array([0.24,0.20,0.21,0.33,0.58,np.inf,np.inf,np.inf]))
# weibel2024=z7.errorbar(M[:len(p7)],p7,[p7n,p7p],fmt='o',capsize=4,color=CLR,ms=5)

# M=10**np.arange(8.75,11.80,0.5)*h
# p8=10**np.array([-3.0,-3.64,-4.09,-4.33,-4.78,-5.54,-5.66])
# p8p=p8*(10**np.array([0.18,0.19,0.24,0.30,0.45,0.57,0.56])-1)
# p8n=p8*(1-1/10**np.array([0.28,0.33,0.55,1.39,np.inf,np.inf,np.inf]))
# z8.errorbar(M[:len(p8)],p8,[p8n,p8p],fmt='o',capsize=4,color=CLR,ms=5)

# M=10**np.arange(8.75,11.80,0.5)*h
# p9=10**np.array([-3.39,-3.81,-4.35,-4.79,-5.27,-5.61,-5.61])
# p9p=p9*(10**np.array([0.25,0.24,0.31,0.40,0.54,0.64,0.61])-1)
# p9n=p9*(1-1/10**np.array([0.64,0.52,1.54,np.inf,np.inf,np.inf,np.inf]))
# z9.errorbar(M[:len(p9)],p9,[p9n,p9p],fmt='o',capsize=4,color=CLR,ms=5)



# LEGENDS
z7.legend(handles=z7_hands)



plt.show()


