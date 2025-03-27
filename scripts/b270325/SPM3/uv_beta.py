import numpy as np
import matplotlib.pyplot as plt
import galspy as gs

FILE="/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/SPM3/data/out_L150N2040_z7p0_st_chabrier300_bin.csv"
MAB,beta = np.loadtxt(FILE,usecols=(5,6)).T
plt.plot(MAB,beta,'.',ms=2,label="L150N2040 (ST)")
MAB,beta = np.loadtxt(FILE.replace("_st_","_stnb_"),usecols=(5,6)).T
plt.plot(MAB,beta,'.',ms=2,label="L150N2040 (ST+NB)")
MAB,beta = np.loadtxt(FILE.replace("_st_","_stnbde_"),usecols=(5,6)).T
plt.plot(MAB,beta,'.',ms=2,label="L150N2040 (ST+NB+DE)")

plt.axhline(-2.4,color='k',ls='--',lw=1)
plt.legend()
plt.xlabel("$M_{UV}$")
plt.ylabel("$\\beta_{UV}$")
plt.show()

