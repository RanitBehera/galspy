import numpy as np
import matplotlib.pyplot as plt
import galspec.Cloudy as cd
import matplotlib
import galspec.Utility as gu

from galspy.utility.Figure.Beautification import SetMyStyle
SetMyStyle(16)





PATH = "/mnt/home/student/cranit/RANIT/Repo/galspy/study/cloudy/bpass_sed"
fig,axs = plt.subplots(1,2,figsize=(10,5))


Ha=[]
Hb=[]
NII_BPT = []
OIII_BPT = []

for i in range(51):
    print(i)
    cloud = cd.CloudyOutputReader(PATH,f"t{i}")

    li = cloud.Lines
    # ================
    _Ha = li.H_alpha
    _Hb = li.H_beta
    _NII_bpt = li.NII_BPT
    _OIII_bpt = li.OIII_BPT 
    # ================
    Ha.append(_Ha)
    Hb.append(_Hb)
    NII_BPT.append(_NII_bpt)
    OIII_BPT.append(_OIII_bpt)

Ha = np.array(Ha)
Hb = np.array(Hb)
NII_BPT = np.array(NII_BPT)
OIII_BPT = np.array(OIII_BPT)

# ============================
x=6+(np.array(range(51))/10)

# Line Intensity
ax:plt.Axes=axs[0]
ax.plot(x,Hb,c='k')
ax.plot(x,Ha,c='r')
ax.plot(x,NII_BPT,c='b')
ax.plot(x,OIII_BPT,c='c')

# Beautify
ax.set_xlim(6,9.5)
ax.set_xlabel("Log Age (Year)")
ax.set_ylabel("Line Intensity\nReative to $H\\beta$")
ax.set_yscale('log')
ax.set_ylim(0.01,100)

# ax.legend()
ax.annotate("$H\\beta - 4861.32\AA$",(6,Hb[0]),(4,8),"data","offset pixels",fontsize=12)
ax.annotate("$H\\alpha - 6562.80\AA$",(6,Ha[0]),(4,8),"data","offset pixels",fontsize=12)
ax.annotate("$[OIII] - 5006.84\AA$",(6,OIII_BPT[0]),(4,8),"data","offset pixels",fontsize=12)
ax.annotate("$[NII] - 6583.45\AA$",(6,NII_BPT[0]),(4,-8),"data","offset pixels",fontsize=12,va="top")


# BPT
ax2:plt.Axes=axs[1]
ax2.plot((NII_BPT/Ha),(OIII_BPT/Hb),'.',ms=10,color='k')
ax2.set_xscale('log')
ax2.set_yscale('log')
ax2.set_xlabel("$[NII]/H\\alpha$")
ax2.set_ylabel("$[OIII]/H\\beta$")
ax2.set_xlim(1e-3,1e2)
ax2.set_ylim(1e-3,1e2)


# SDSS z~0 : https://arxiv.org/pdf/2201.03564
# x_hr = np.logspace(-3,2,100)
# y_hr = (0.61/(x_hr+0.08))+1.1
# ax2.plot(x_hr,y_hr,label="SDSS (z~0) Garg et al. (2022)")
# ax2.legend()



plt.suptitle("IMF : Chab_300M \nZ=0.00001")


plt.show()
