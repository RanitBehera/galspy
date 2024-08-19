import galspy.IO.MPGadget as mp
import matplotlib.pyplot as plt
import numpy as np

PATH = "/mnt/home/student/cranit/Data/MP_Gadget/Nishi/L50N640"
SNAP = mp.NavigationRoot(PATH).PART(36)

dens = SNAP.Gas.Density()
temp = SNAP.Gas.InternalEnergy()

mean_dens = np.sum(SNAP.Gas.Mass())/(10000**3)

plt.plot(dens/mean_dens,temp,'.',ms=0.1)
plt.xscale('log')
plt.yscale('log')
plt.savefig("/mnt/home/student/cranit/Repo/galspy/temp/plots/rho_T.png")