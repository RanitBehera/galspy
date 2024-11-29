import galspy
import matplotlib.pyplot as plt

L150N2040 = "/mnt/home/student/cranit/NINJA/simulations/L150N2040/SNAPS"
ROOT = galspy.NavigationRoot(L150N2040)

BLOBS = ['000000', '00000D', '00000E', '000032', '000033', '000040', '000042', '000043', '00006A', '00006B', '000075', '000076']

print("Reading Blobs ...")
energy_per_unit_mass = ROOT.PART(43).Gas.InternalEnergy(BLOBS)
mass = ROOT.PART(43).Gas.Mass(BLOBS)
print("Read Blobs")

energy = energy_per_unit_mass*mass*1e10

# FROM CODE
# /*Get the equilibrium temperature at given internal energy.
#     density is total gas density in protons/cm^3
#     Internal energy is in ergs/g.
#     helium is a mass fraction*/





































