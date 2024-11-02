import numpy as np
import matplotlib.pyplot as plt
import os
from galspy.utility.Figure.Beautification import SetMyStyle
SetMyStyle(12)

CACHE_DIR = "/mnt/home/student/cranit/RANIT/Repo/galspy/study/hpc_proposal"
CACHE_NAME = ["sfrd_L150N2040.txt",
              "sfrd_L250N2040.txt"] 

CACHE = [CACHE_DIR + os.sep + FN for FN in CACHE_NAME]
LABELS = ["L150N2040","L250N2040"]
COLOSR = ['r','g']

h=0.6736

for i,file in enumerate(CACHE):
    z,sfrd,sfrd03 = np.loadtxt(file).T
    sfrd = sfrd*(h**3)
    sfrd03 = sfrd03*(h**3)
    mask = (z<15)
    z,sfrd,sfrd03=z[mask],sfrd[mask],sfrd03[mask]
    plt.plot(z,sfrd,label=LABELS[i])
    plt.plot(z,sfrd03,label=LABELS[i],ls='--')

# Astrid
az,asfrd = np.loadtxt("study/astrid/sfrd.txt",delimiter=',').T
asfrd = 10**asfrd
plt.plot(az,asfrd,label="Astrid",c='k',ls='-',lw=1)

az,asfrd = np.loadtxt("study/astrid/sfrd03.txt",delimiter=',').T
asfrd = 10**asfrd
plt.plot(az,asfrd,label="Astrid03",c='k',ls='--',lw=1)
# Rough Obs



plt.yscale('log')
plt.legend()

plt.xlabel("Redshift $(z)$")
plt.ylabel("log(SFRD) $(M_\odot$ yr$^{-1}$ Mpc$^{-3})$")

plt.show()