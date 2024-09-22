import galspy
import matplotlib.pyplot as plt
import numpy as np

PATH        =  "/mnt/home/student/cranit/NINJA/simulations/L150N2040/SNAPS"
SNAP_NUM    = 43


# READ FIELDS
root = galspy.NavigationRoot(PATH)
SNAP = root.PIG(SNAP_NUM)
MASS_UNIT   = 1e10
# Seed Props - TODO: Auto get
MIN_FOF_MASS_FOR_SEED       = 0.5 * MASS_UNIT
MIN_STELLAR_MASS_FOR_SEED   = 0.001 * MASS_UNIT
BH_SEED_MASS_MIN            = 3.0e-6 * MASS_UNIT
BH_SEED_MASS_MAX            = 3.0e-5 * MASS_UNIT
BH_SEED_INDEX               = -2


# seed line
# sd_mass = 

bh_mass = SNAP.BlackHole.BlackholeMass() * MASS_UNIT
bh_seed_mass = SNAP.BlackHole.BlackholeMseed() * MASS_UNIT
bh_gid  = SNAP.BlackHole.GroupID()


# print(bh_mass[2]+bh_mass[3])
# print(SNAP.FOFGroups.BlackholeMass()[2]*MASS_UNIT)

print(len(bh_mass[bh_mass>5e6]))
print(max(bh_mass/1e6))


plt.plot(bh_seed_mass,bh_mass,'.',ms=5)

plt.yscale('log')
plt.xscale('log')
plt.axis("equal")


plt.show()





