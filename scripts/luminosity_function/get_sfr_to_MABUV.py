import galspy
import numpy,os

MPGADGET_OUTPUT_DIR = "/mnt/home/student/cranit/NINJA/simulations/L250N2040/SNAPS"

Z=10
root = galspy.NavigationRoot(MPGADGET_OUTPUT_DIR)
PIG = root.PIG(root.SnapNumFromZ(Z))

SFR = PIG.FOFGroups.StarFormationRate()
SFR*=(1e10/3.08568e+16) * 365 * 24 * 3600 # M_sun /year
SFR=SFR[SFR!=0]
SFR=SFR.astype(numpy.float128)
K_UV = 1.15e-28
L_UV = SFR/K_UV


# 
area = 4 * numpy.pi * (10 * 3.086e18)**2
f_nu = L_UV/area
Jy = 1e-23
M_AB = -2.5*numpy.log10(f_nu/3631/Jy)

print(M_AB)

numpy.savetxt(f"/mnt/home/student/cranit/RANIT/Repo/galspy/study/LuvAB/MUVAB_SFR_L250N2050_z{Z}.txt",M_AB)


