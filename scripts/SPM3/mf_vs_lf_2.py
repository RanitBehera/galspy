import galspy as gs
import numpy as np
import matplotlib.pyplot as plt

from galspy.MPGadget import _Sim


def DoForSim(sim_path:str,redshift=7):
    SIM = gs.NavigationRoot(sim_path)
    SN=SIM.SnapNumFromRedshift(redshift)
    PIG = SIM.PIG(SN)

    h=PIG.Header.HubbleParam()
    z=PIG.Header.Redshift()
    box_size = PIG.Header.BoxSize()/1000

    # Get Mass Function to light
    fof_dm_mass = PIG.FOFGroups.MassByType().T[1]*1e10

    lower_limit = 32*PIG.Header.MassTable()[1]*1e10
    mask =fof_dm_mass>lower_limit
    MC = fof_dm_mass[mask]
    MC = MC.astype(np.float64)
    
    # To light
    xi=1e30 # erg s-1 A-1 Mo-1
    L=MC*xi/1.15# erg s-1 A-1
    pc = 3.086e18   # cm pc-1
    f_lam = L/(4*np.pi*((10*pc)**2)) # erg s-1 A-1 cm-2
    c= 3e8 * 1e10 # A Hz
    f_nu = f_lam * ((1500**2)/c)
    M_AB = -2.5 * np.log10(f_nu) - 48.6

    # Luminosity function
    log_L,dn_dlogL,error=gs.Utility.LumimosityFunction(M_AB,box_size/h,0.5)
    XMF = log_L
    YMF = np.log10(dn_dlogL+1e-300)
    if sim_path==gs.NINJA.L150N2040:
        plt.plot(XMF[:-5],YMF[:-5],'--',label=f"{SIM.sim_name}; z={z:.02f}",alpha=0.5)
    if sim_path==gs.NINJA.L250N2040:
        plt.plot(XMF[1:-5],YMF[1:-5],'--',label=f"{SIM.sim_name}; z={z:.02f}",alpha=0.5)




DoForSim(gs.NINJA.L150N2040)
DoForSim(gs.NINJA.L250N2040)

# ================ LUMINOSITY FUNCTION OBSERVED
# x = [-22.965968509217227, -22.714659508937057, -22.431937018434454, -22.094240830167536, -21.67801001759394, -21.175392736034077, -20.594240470667298, -19.97382215139801, -19.345549470947468, -18.803664697484145, -18.308900339104593, -17.735602434919073, -17.264398284081402]
# y = [-7.426086369245929, -6.730434553005776, -6.026086820375284, -5.399999946925958, -4.782608591811657, -4.2347825775434975, -3.765217422456503, -3.36521760821565, -3.008695783705235, -2.739130535738666, -2.5304349112555586, -2.2434784275912847, -2.0347828031081754]
# plt.plot(x,y,'k',label="Cosmos-Web")


#Harikane
year,z,MUV,MUV_p,MUV_n,phi,phi_p,phi_n,phi_exp = np.loadtxt("/mnt/home/student/cranit/RANIT/Repo/galspy/obs/uvlf/uvlf.txt",usecols=(1,2,3,4,5,6,7,8,9)).T

val = np.log10(phi * (10**phi_exp))
val_p = np.log10((phi + phi_p) * 10**phi_exp)
val_n = np.log10((phi + phi_n) * 10**phi_exp)

# plt.plot(MUV,val,'.',label="Harikane",ms=10,color='k')
# plt.plot(MUV,val_p,'+',ms=10,color='k')
# plt.plot(MUV,val_n,'+',ms=10,color='k')

plt.plot(MUV,val,'.',ms=10,color='k',label="Harikane+24")
for m,n,p in zip(MUV,val_n,val_p):
    plt.plot([m,m],[n,p],'_-k')


# Finkelstein
MUV=[-22.0,-21.5,-21.0,-20.5,-20.0,-19.5,-19.0,-18.5,-18.0]

phi=[0.0046,0.0187,0.0690,0.1301,0.2742,0.3848,0.5699,2.5650,3.0780]
phi_p=[0.0049,0.0085,0.0156,0.0239,0.0379,0.0633,0.2229,0.8735,1.0837]
phi_n=[-0.0028,-0.0067,-0.0144,-0.0200,-0.0329,-0.0586,-0.1817,-0.7161,-0.8845]


phi = np.array(phi)*1e-3
phi_n = phi+np.array(phi_n)*1e-3
phi_p = phi+np.array(phi_p)*1e-3

phi = np.log10(phi)
phi_p = np.log10(phi_p)
phi_n = np.log10(phi_n)

plt.plot(MUV,phi,'.',ms=10,color='r',label="Finkelstein+15")

for m,n,p in zip(MUV,phi_n,phi_p):
    plt.plot([m,m],[n,p],'_-r')





# Bouwens 21
MUV=np.array([-22.19,-21.69,-21.19,-20.69,-20.19,-19.69,-19.19,-18.69,-17.94,-16.94])
phi =np.array([0.000001,0.000041,0.000047,0.000198,0.000283,0.000589,0.001172,0.001433,0.005760,0.008320])
err=np.array([0.000002,0.000011,0.000015,0.000036,0.000066,0.000126,0.000336,0.000419,0.001440,0.002900])

phi_p=phi+err
phi_n=phi-err

phi=np.log10(phi)
phi_p=np.log10(phi_p)
phi_n=np.log10(phi_n)


plt.plot(MUV,phi,'.',ms=10,color='g',label="Bouwens+21")

for m,n,p in zip(MUV,phi_n,phi_p):
    plt.plot([m,m],[n,p],'_-g')






# ================ LUMINOSITY FUNCTION SIMS
x = [-16.526785714285715, -17.1875, -18.276785714285715, -19.151785714285715, -20.1875, -21.13392857142857, -21.50892857142857, -21.803571428571427, -22.151785714285715, -22.50892857142857, -23.473214285714285, -23.848214285714285, -23.955357142857142]
y = [-2.2781954887218046, -2.5338345864661656, -2.984962406015038, -3.3533834586466167, -3.8646616541353387, -4.360902255639098, -4.571428571428571, -4.7894736842105265, -4.93984962406015, -5.180451127819548, -6.007518796992481, -6.12781954887218, -6.285714285714286]
x=np.array(x)
plt.plot(x,y,':',label="Astrid")


# NINJA
def DoforFile(filepath,label,boxsize_MPC):
    table = np.loadtxt(filepath)
    M_AB = table.T[5]
    log_L,dn_dlogL,error=gs.Utility.LumimosityFunction(M_AB,boxsize_MPC/0.6736,0.5)
    log_L=log_L[1:-7]
    dn_dlogL=dn_dlogL[1:-7]

    XLF = log_L
    YLF = np.log10(dn_dlogL)
    plt.plot(XLF,YLF,'.-',label=label + "z=7")



DoforFile("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/SPM3/data_old/out_L150N2040_z7p0.csv","L150N2040 (ST+NB)",150)
DoforFile("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/SPM3/data_old/out_L150N2040_z7p0_stellar.csv","L150N2040 (ST)",150)
# DoforFile("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/SPM3/data/out_L250N2040_z7p0_stellar.csv","L250N2040 (ST)",250)


plt.xlabel("MUV")
plt.xlabel("Phi")

plt.legend()
plt.show()

