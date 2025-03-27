import galspy as gs
import numpy as np

SIM = gs.NavigationRoot(gs.NINJA.L150N2040)
PIG=SIM.PIG(SIM.SnapNumFromRedshift(7))
h=PIG.Header.HubbleParam()
BOXSIZE = PIG.Header.BoxSize()/1000 # Mpc

M2L_RATIO = 1e30    # erg s-1 A-1 Mo-1
PC2CM = 3.086e18
MUNIT =1e10/h
dm_mass = PIG.FOFGroups.MassByType().T[1]
lower_limit = 32*PIG.Header.MassTable()[1]
mask = dm_mass>lower_limit
dm_mass = dm_mass[mask]*MUNIT
dm_lum = M2L_RATIO * dm_mass.astype(np.float64)
f_lam = dm_lum/(4*np.pi*(10*PC2CM)**2)
c= 3e8 * 1e10 # A Hz
lam=1500 # A
f_nu = f_lam * ((lam**2)/c)
M_AB = -2.5 * np.log10(f_nu) - 48.6


M_AB,Phi,error = gs.Utility.LumimosityFunction(M_AB,BOXSIZE,20)


import matplotlib.pyplot as plt
plt.plot(M_AB,Phi)
plt.yscale("log")
plt.show()






