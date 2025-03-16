import numpy as np
import matplotlib.pyplot as plt
import os
import matplotlib.lines as mlines
from galspy.utility.Figure.Beautification import SetMyStyle
SetMyStyle(12)

CACHE_DIR = "/mnt/home/student/cranit/RANIT/Repo/galspy/study/hpc_proposal"
CACHE_NAME = ["sfrd_L150N2040.txt",
              "sfrd_L250N2040.txt"] 

CACHE = [CACHE_DIR + os.sep + FN for FN in CACHE_NAME]
LABELS = ["L150N2040","L250N2040"]
COLORS = ['m','c']

h=0.6736

plt.figure(figsize=(6,6))

for i,file in enumerate(CACHE):
    z,sfrd,sfrd03 = np.loadtxt(file).T
    sfrd = sfrd*(h**3)
    sfrd03 = sfrd03*(h**3)
    mask = (z<18)
    z,sfrd,sfrd03=z[mask],sfrd[mask],sfrd03[mask]
    plt.plot(z,np.log10(sfrd),c=COLORS[i])
    plt.plot(z,np.log10(sfrd03),ls='--',c=COLORS[i])

# Astrid
az,asfrd = np.loadtxt("/mnt/home/student/cranit/RANIT/Repo/galspy/study/astrid/sfrd.txt",delimiter=',').T
asfrd = asfrd
# plt.plot(az,asfrd,label="Astrid",c='k',ls='-',lw=1)

az,asfrd = np.loadtxt("/mnt/home/student/cranit/RANIT/Repo/galspy/study/astrid/sfrd03.txt",delimiter=',').T
asfrd = asfrd
# plt.plot(az,asfrd,label="Astrid03",c='k',ls='--',lw=1)



# Rough Obs

def PlotObs(path,label,clr):
    obs_z,obs_sfrd,errp,errn=np.loadtxt(path).T
    plt.errorbar(obs_z,obs_sfrd,[errn,errp],label=label,fmt='o',capsize=4,color=clr)


PlotObs("/mnt/home/student/cranit/RANIT/Repo/galspy/obs/sfrd_vs_z/Bouwens_2023.txt","Bouwens et al. (2023)",(0.7,0,0))
PlotObs("/mnt/home/student/cranit/RANIT/Repo/galspy/obs/sfrd_vs_z/Harikane_2023.txt","Harikane et al. (2023)",(0,0.6,0.25))
PlotObs("/mnt/home/student/cranit/RANIT/Repo/galspy/obs/sfrd_vs_z/Oesch_2018.txt","Oesch et al. (2018, 2014)",(1,0.6,0.25))
PlotObs("/mnt/home/student/cranit/RANIT/Repo/galspy/obs/sfrd_vs_z/McLure_2018.txt","McLure et al. (2018)",(1,0.4,0.8))
PlotObs("/mnt/home/student/cranit/RANIT/Repo/galspy/obs/sfrd_vs_z/Bouwens_2016.txt","Bouwens et al. (2016)",(0.25,0.5,1.0))




# MANUAL LEGEND
clrs=['m','c']
labels=["L150N2040","L250N2040"]
line1 = mlines.Line2D([], [], color=clrs[0], marker=' ',markersize=8, label=labels[0])
line2 = mlines.Line2D([], [], color=clrs[1], marker=' ',markersize=8, label=labels[1])
boxes = [line1,line2]
leg=plt.gca().legend(handles=boxes,fontsize=12, loc='lower left',ncol=1,frameon=False,ncols=1,bbox_to_anchor=(0,0.25))
plt.gca().add_artist(leg)

line1 = mlines.Line2D([], [], color='k',ls='-', marker=' ',markersize=8, label="Global (Full Box)")
line2 = mlines.Line2D([], [], color='k',ls='--',marker=' ',markersize=8, label="SFR$_{Halo}>$ 0.3 $M_\odot$ yr$^{-1}$")
boxes = [line1,line2]
leg=plt.gca().legend(handles=boxes,fontsize=12, loc='upper right',ncol=1,frameon=False,bbox_to_anchor=(1,1))
plt.gca().add_artist(leg)





# plt.yscale('log')
plt.legend(frameon=False,loc="lower left",fontsize=10)

plt.xlabel("Redshift $(z)$",fontsize=16)
plt.ylabel("log$_{10}$(SFRD) $(M_\odot$ yr$^{-1}$ Mpc$^{-3})$",fontsize=16)
plt.xlim(4)
plt.grid(alpha=0.2)

# plt.title("!! IN PROGRESS !!")

plt.show()

