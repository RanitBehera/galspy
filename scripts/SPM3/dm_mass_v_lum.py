import numpy as np
import galspy as gs
import matplotlib.pyplot as plt


table = np.loadtxt("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/SPM3/data/out_L150N2040_z7p0.csv",
                  usecols=(1,2))

tgid,rf_L_lam_UV = table.T
tgindex = (tgid-1).astype(np.int64)



REDSHIFT = 7.0
SIM = gs.NavigationRoot(gs.NINJA.L150N2040)
SN = SIM.SnapNumFromRedshift(REDSHIFT)
PIG = SIM.PIG(SN)

dm_mass = PIG.FOFGroups.MassByType().T[1]*1e10
dm_mass = dm_mass[tgindex]

# plt.plot(dm_mass,rf_L_lam_UV,'.',ms=1)
plt.plot(dm_mass,dm_mass/rf_L_lam_UV,'.',ms=1)


plt.xscale("log")
plt.yscale("log")

plt.show()


