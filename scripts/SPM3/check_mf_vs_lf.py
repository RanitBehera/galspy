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
M=M[mask]
dn_dlogM=dn_dlogM[mask]

XMF = np.log10(M+1e-300)
YMF = np.log10(dn_dlogM+1e-300)
XMF = (XMF - np.min(XMF))/ (np.max(XMF)-np.min(XMF)) 
YMF = (YMF - np.min(YMF))/ (np.max(YMF)-np.min(YMF)) 
plt.plot(XMF,YMF,'.-',label=f"MF {SIM.sim_name}; z={z:.02f}")



# # LUMINOSITY FUNCTION
table = np.loadtxt("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/SPM3/data/out_L150N2040_z7p0.csv")
M_AB = table.T[5]
log_L,dn_dlogL,error=gs.Utility.LumimosityFunction(M_AB,box_size,0.5)


log_L=log_L[1:-7]
dn_dlogL=dn_dlogL[1:-7]

XLF = np.abs(log_L)
YLF = np.log10(dn_dlogL+1e-300)


YLF = (YLF-np.min(YLF))/(np.max(YLF)-np.min(YLF))
XLF = (XLF-np.min(XLF))/(np.max(XLF)-np.min(XLF))
plt.plot(XLF,YLF,'.-',label=f"LF {SIM.sim_name}; z={z:.02f}")


plt.legend()
plt.show()

