import numpy as np
import matplotlib.pyplot as plt
import galspy

# gid,Mst,Mtot=np.loadtxt("/mnt/home/student/cranit/RANIT/Repo/galspy/study/LuvAB/MUVAB.txt").T

# plt.plot(Mst,Mtot-Mst,'.')
# plt.show()

MPGADGET_OUTPUT_DIR = "/mnt/home/student/cranit/NINJA/simulations/L150N2040/SNAPS"
SNAP_NUM = 43

root = galspy.NavigationRoot(MPGADGET_OUTPUT_DIR)
PIG = root.PIG(SNAP_NUM)


ac=PIG.BlackHole.BlackholeAccretionRate()
ac*= (1e10/3.08568e+16) * 365 * 24 * 3600 # M_sun /year
ac = ac.astype(np.float128)
# ac=ac*(2e30)/(365*24*3600) #kg/sec


mass=PIG.BlackHole.BlackholeMass()*1e10




plt.plot(mass,ac,'.')
plt.xscale("log")
plt.yscale("log")
plt.axhline(0.05,ls='--',color='k')
plt.show()

