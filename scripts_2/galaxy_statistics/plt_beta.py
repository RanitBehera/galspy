import galspy
import numpy as np
import os
import matplotlib.pyplot as plt
from galspy.utility.Figure.Beautification import SetMyStyle
from matplotlib import ticker
import matplotlib.lines as mlines



SetMyStyle()


TABLE_PATH = "/mnt/home/student/cranit/RANIT/Repo/galspy/scripts_2/galaxy_statistics/data"

GID,GMDM,GMST,GMBH,NST,NBH,bh_acc,Mdot_edd,L_edd = np.loadtxt(TABLE_PATH +os.sep+f"table1_L150N2040_8.txt").T
GID_p,MAB_ST_p,MAB_ST_RED_p,MAB_TOT_p,MAB_TOT_RED_p,beta_ST_p,beta_ST_RED_p,beta_TOT_p,beta_TOT_RED_p = np.loadtxt(TABLE_PATH +os.sep+f"table2_primordial_L150N2040_8.txt").T

sort = np.argsort(GID_p)

M1,b1s,b1t = GMST,beta_ST_p[sort],beta_TOT_p[sort]
b1s=b1s[:50000]
b1t=b1t[:50000]
maskM=M1>1e8
masks=(b1s<-1)&maskM
maskt=(b1t<-1)&maskM

# GID,GMDM,GMST,GMBH,NST,NBH,bh_acc,Mdot_edd,L_edd = np.loadtxt(TABLE_PATH +os.sep+f"table1_L250N2040_8.txt").T
# GID_p,MAB_ST_p,MAB_ST_RED_p,MAB_TOT_p,MAB_TOT_RED_p,beta_ST_p,beta_ST_RED_p,beta_TOT_p,beta_TOT_RED_p = np.loadtxt(TABLE_PATH +os.sep+f"table2_primordial_{BOX}_{Z}.txt").T

# M2,b2s,b2t = GMST,beta_ST_p,beta_TOT_p


plt.plot(M1[masks],b1s[masks],'.',label="Stellar")
plt.plot(M1[maskt],b1t[maskt],'.',label="Stellar + Nebular")

plt.axhline(-2.4,color='k',ls='--',lw=1)
plt.xlim(left=1e8)
plt.xscale("log")
plt.xlabel("$M/M_\odot$",fontsize=14)
plt.ylabel("$\\beta_{UV}$",fontsize=14)
plt.legend()
plt.show()