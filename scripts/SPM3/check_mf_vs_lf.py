

# %%
import galspy as gs
import numpy as np
import matplotlib.pyplot as plt

SIM = gs.NavigationRoot(gs.NINJA.L150N2040)

REDSHIFT=7


SN=SIM.SnapNumFromRedshift(REDSHIFT)
PIG = SIM.PIG(SN)

h=PIG.Header.HubbleParam()
z=PIG.Header.Redshift()
box_size = PIG.Header.BoxSize()/1000


# %%

# ================ LUMINOSITY FUNCTION
table = np.loadtxt("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/SPM3/data/out_L150N2040_z7p0.csv")
M_AB = table.T[5]
log_L,dn_dlogL,error=gs.Utility.LumimosityFunction(M_AB,box_size/h,0.5)


log_L=log_L[1:-7]
dn_dlogL=dn_dlogL[1:-7]

XLF = log_L
# XLF = np.abs(XLF)
YLF = np.log10(dn_dlogL+1e-300)
# YLF = (YLF-np.min(YLF))/(np.max(YLF)-np.min(YLF))
# XLF = (XLF-np.min(XLF))/(np.max(XLF)-np.min(XLF))
plt.plot(XLF,YLF,'.-',label=f"LF {SIM.sim_name}; z={z:.02f}")



# ================ LUMINOSITY FUNCTION OBSERVED
x = [-22.965968509217227, -22.714659508937057, -22.431937018434454, -22.094240830167536, -21.67801001759394, -21.175392736034077, -20.594240470667298, -19.97382215139801, -19.345549470947468, -18.803664697484145, -18.308900339104593, -17.735602434919073, -17.264398284081402]
y = [-7.426086369245929, -6.730434553005776, -6.026086820375284, -5.399999946925958, -4.782608591811657, -4.2347825775434975, -3.765217422456503, -3.36521760821565, -3.008695783705235, -2.739130535738666, -2.5304349112555586, -2.2434784275912847, -2.0347828031081754]
# y=10**np.array(y)
# x=np.abs(x)
# x=(x-np.min(x))/(np.max(x)-np.min(x))
# y=(y-np.min(y))/(np.max(y)-np.min(y))
plt.plot(x,y,label="Cosmos-Web")



# =============== MASS FUNCTION
fof_dm_mass = PIG.FOFGroups.MassByType().T[1]*1e10
M,dn_dlogM,error=gs.Utility.MassFunction(fof_dm_mass,box_size)
lower_limit = 32*PIG.Header.MassTable()[1]*1e10
mask = M>lower_limit 
M=M[mask]
dn_dlogM=dn_dlogM[mask]

XMF = np.log10(M+1e-300)
YMF = np.log10(dn_dlogM+1e-300)
# XMF = (XMF - np.min(XMF))/ (np.max(XMF)-np.min(XMF)) 
# YMF = (YMF - np.min(YMF))/ (np.max(YMF)-np.min(YMF)) 

# XMF = -XMF
# XMF *= np.abs(np.ptp(x))
# XMF += np.max(x)

# YMF *= np.abs(np.ptp(y))
# YMF -= np.max(YMF) - np.max(y)


XMF = -XMF-10
YMF = YMF -2

plt.plot(XMF,YMF,'.-',label=f"MF {SIM.sim_name}; z={z:.02f}")






plt.legend()
plt.show()


# %%
