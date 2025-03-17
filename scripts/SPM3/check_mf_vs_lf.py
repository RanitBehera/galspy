import galspy as gs
import numpy as np
import matplotlib.pyplot as plt

SIM = gs.NavigationRoot(gs.NINJA.L150N2040)

REDSHIFT=7


# MASS FUNCTION
SN=SIM.SnapNumFromRedshift(REDSHIFT)
PIG = SIM.PIG(SN)

h=PIG.Header.HubbleParam()
z=PIG.Header.Redshift()
box_size = PIG.Header.BoxSize()/1000

fof_dm_mass = PIG.FOFGroups.MassByType().T[1]*1e10
M,dn_dlogM,error=gs.Utility.MassFunction(fof_dm_mass,box_size)
lower_limit = 32*PIG.Header.MassTable()[1]*1e10
mask = M>lower_limit 
plt.plot(M[mask],dn_dlogM[mask],label=f"MF {SIM.sim_name}; z={z:.02f}")



# LUMINOSITY FUNCTION
table = np.loadtxt("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/SPM3/data/out_L150N2040_z7p0.csv")
M_AB = table.T[5]
gs.Utility.LumimosityFunction()

print(M_AB)


