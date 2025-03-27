import galspy as gs
import numpy as np
import matplotlib.pyplot as plt



data = np.loadtxt("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/analysis_b270325/SPM3/data/out_L150N2040_z7p0_st_chabrier300_bin.csv",
                  usecols=(1,5))
TGID,MAB = data.T
TGID = np.int64(TGID)

SIM = gs.NavigationRoot(gs.NINJA.L150N2040)
PIG = SIM.PIG(7)


MMASS = PIG.FOFGroups.GasMetalMass()[TGID-1]
GMASS = PIG.FOFGroups.MassByType().T[0][TGID-1]

AVG_Z_by_M = MMASS/GMASS

print(np.max(AVG_Z_by_M))

# plt.plot(MAB,AVG_Z_by_M,'.',ms=2)

# plt.hexbin(MAB,AVG_Z_by_M)
plt.hexbin(MAB,np.log10(AVG_Z_by_M/0.02),gridsize=30,cmap="Oranges",bins='log')

plt.axhline(0)

plt.colorbar()
# plt.yscale('log')



# -------------------------
target= TGID[0]

gas_gid = PIG.Gas.GroupID()
mask = gas_gid==target
gas_mass = PIG.Gas.Mass()[mask]
gas_met = PIG.Gas.Metallicity()[mask]
gas_pos = PIG.Gas.Position()[mask]


star_gid = PIG.Star.GroupID()
mask = star_gid==target
star_mass = PIG.Star.Mass()[mask]
star_met = PIG.Star.Metallicity()[mask]
star_pos = PIG.Star.Position()[mask]


plt.figure()
plt.hist(np.log10(gas_met[~(gas_met==0)]/0.02),bins=100)



plt.figure()
from galspy.Utility.Visualization import Cube3D

c3d = Cube3D()

mask_met = (gas_met/0.02)>0.01

c3d.add_points(gas_pos[mask_met],points_size=10,points_color='b')
c3d.add_points(gas_pos[~mask_met],points_size=10,points_color='y')
c3d.add_points(star_pos,points_size=50,points_color='r')

c3d.show(False)

plt.show()
 












