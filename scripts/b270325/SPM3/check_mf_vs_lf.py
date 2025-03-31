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



# ================ LUMINOSITY FUNCTION
table = np.loadtxt("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/SPM3/data/out_L150N2040_z7p0.csv")
M_AB = table.T[5]
bin_AB,bin_phi,error=gs.Utility.LumimosityFunction(M_AB,box_size/h,0.5)


log_L=log_L[1:-7]
dn_dlogL=dn_dlogL[1:-7]

XLF = log_L
# XLF = np.abs(XLF)
YLF = np.log10(dn_dlogL+1e-300)
# plt.plot(XLF,YLF,'.-',label=f"LF {SIM.sim_name}; z={z:.02f}")



# ================ LUMINOSITY FUNCTION OBSERVED
x = [-22.965968509217227, -22.714659508937057, -22.431937018434454, -22.094240830167536, -21.67801001759394, -21.175392736034077, -20.594240470667298, -19.97382215139801, -19.345549470947468, -18.803664697484145, -18.308900339104593, -17.735602434919073, -17.264398284081402]
y = [-7.426086369245929, -6.730434553005776, -6.026086820375284, -5.399999946925958, -4.782608591811657, -4.2347825775434975, -3.765217422456503, -3.36521760821565, -3.008695783705235, -2.739130535738666, -2.5304349112555586, -2.2434784275912847, -2.0347828031081754]
plt.plot(x,y,label="Cosmos-Web")




# =============== MASS FUNCTION
fof_dm_mass = PIG.FOFGroups.MassByType().T[1]*1e10



# ---- Light
MC = fof_dm_mass[fof_dm_mass>1e8]

print(min(MC))

print(min(MC),max(MC))

MC = MC.astype(np.float64)

xi=1e30 # erg s-1 A-1 Mo-1
L=MC*xi/1.15# erg s-1 A-1



pc = 3.086e18   # cm pc-1
f_lam = L/(4*np.pi*((10*pc)**2)) # erg s-1 A-1 cm-2


c= 3e8 * 1e10 # A Hz
f_nu = f_lam * ((1500**2)/c)


M_AB = -2.5 * np.log10(f_nu) - 48.6



# -----


M,dn_dlogM,error=gs.Utility.MassFunction(fof_dm_mass,box_size)
lower_limit = 32*PIG.Header.MassTable()[1]*1e10
mask = M>lower_limit 
M=M[mask]
dn_dlogM=dn_dlogM[mask]

XMF=np.log10(M)
YMF=np.log10(dn_dlogM)

# plt.plot(XMF,YMF,'.-',label=f"MF {SIM.sim_name}; z={z:.02f}")



# ------------------------------------------------------------

# print(fof_dm_mass)

# M=fof_dm_mass
# lower_limit = 32*PIG.Header.MassTable()[1]*1e10

# mask = M>lower_limit
# M=M[mask]

# print(len(M))

# mask2=M>0
# M=M[mask2]






bin_AB,bin_phi,error=gs.Utility.LumimosityFunction(M_AB,box_size/h,0.5)


XMF = log_L
YMF = np.log10(dn_dlogL+1e-300)

mask = YMF>-30
XMF=XMF[mask]
YMF=YMF[mask]

plt.plot(XMF[:-5],YMF[:-5],'.-',label=f"MF {SIM.sim_name}; z={z:.02f}")


plt.legend()
plt.show()


# %%
