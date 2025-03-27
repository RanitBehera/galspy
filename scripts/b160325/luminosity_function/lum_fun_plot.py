import numpy as np
from galspec.Utility import LuminosityFunction
import matplotlib.pyplot as plt

gid,Mst,Mtot=np.loadtxt("/mnt/home/student/cranit/RANIT/Repo/galspy/study/LuvAB/MUVAB.txt").T
M_SFR=np.loadtxt("/mnt/home/student/cranit/RANIT/Repo/galspy/study/LuvAB/MUVAB_SFR.txt").T

M,phi,err = LuminosityFunction(Mst,(150)**3,0.5)
plt.plot(M,phi,label="Stellar")
M,phi,err = LuminosityFunction(Mtot,(150)**3,0.5)
plt.plot(M,phi,label="Stellar+Nebular")

M,phi,err = LuminosityFunction(M_SFR,(150)**3,0.5)
plt.plot(M,phi,label="SFR to LUV")


plt.yscale('log')
plt.legend()
plt.show()