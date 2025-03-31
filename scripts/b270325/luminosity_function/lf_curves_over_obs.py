import matplotlib.pyplot as plt
import numpy as np
import galspy as gs
from matplotlib.gridspec import GridSpec
from typing import Literal

# Initialise Figure
# gs.SetPlotStyle()
fig = plt.figure(figsize=(12,8))
gsp = GridSpec(1,1,figure=fig)
# ax00 = fig.add_subplot(gsp[0,0])
# ax01 = fig.add_subplot(gsp[0,1])
# ax10 = fig.add_subplot(gsp[1,0])
ax11 = fig.add_subplot(gsp[0,0])

OBS_DATA_DIR = "/mnt/home/student/cranit/RANIT/Repo/galspy/obs/uvlf"
OBS_DICT_HINT = Literal["Bouwens+21","Oesch+18"]
OBS_DICT = {
    "Bouwens+21" : f"{OBS_DATA_DIR}/Bouwens+21.txt",
    "Oesch+18" : f"{OBS_DATA_DIR}/Oesch+18.txt"
}


def InitAxis(ax:plt.Axes,redshift,obs_key_list:OBS_DICT_HINT=[],label=""):
    ax.annotate(f"z={redshift:.01f}",(0,1),(8,-8),"axes fraction","offset pixels",ha="left",va="top",fontsize=14)
    ax.set_xlabel("$M_{AB}$")
    ax.set_ylabel("$\Phi$")
    # --------
    for key in obs_key_list:
        filepath = OBS_DICT[key]
        data = np.loadtxt(filepath)
        z,MAB,Phi,MAB_n,MAB_p,Phi_n,Phi_p = data.T
        mask = z==redshift
        z,MAB,Phi,MAB_n,MAB_p,Phi_n,Phi_p = z[mask],MAB[mask],Phi[mask],MAB_n[mask],MAB_p[mask],Phi_n[mask],Phi_p[mask]

        ax.errorbar(MAB,Phi,label=key + f" {label}",yerr=[Phi_n,Phi_p],ls=' ',marker='.',capsize=3,ms=8)


# InitAxis(ax00,10,["Oesch+18"])
# InitAxis(ax01,9,["Bouwens+21"])
# InitAxis(ax10,8,["Bouwens+21"])
InitAxis(ax11,7,["Bouwens+21"])


# -------------------------
# NINJA
SIM = gs.NavigationRoot(gs.NINJA.L150N2040)
PIG = SIM.PIG(SIM.SnapNumFromRedshift(7))
SMASS=PIG.FOFGroups.MassByType().T[4]*1e10/0.6736

def DoforFile(filepath,label,boxsize_MPC,ax):
    table = np.loadtxt(filepath,usecols=(1,5))
    TGID,M_AB = table.T
    TGID=TGID.astype(np.int64)
    bin_AB,bin_phi,error=gs.Utility.LumimosityFunction(M_AB,boxsize_MPC/0.6736,20)
    # log_L=log_L[1:-7]
    # dn_dlogL=dn_dlogL[1:-7]

    XLF = bin_AB
    # YLF = np.log10(dn_dlogL)
    YLF = bin_phi
    ax.plot(XLF,YLF,'-',label=label)
    plt.fill_between(XLF,YLF+error,YLF-error,color='k',alpha=0.2,ec=None)
    # plt.plot(XLF,YLF+error,color='k',alpha=0.3)
    # plt.plot(XLF,YLF-error,color='k',alpha=0.3)

    # --------------------------------
    tsmass=SMASS[TGID-1]
    def GetA(mstar,mab,m1,m2,K):
        return 10**(m1*np.log10(mstar)+m2*mab+K)

    A6=GetA(tsmass,M_AB,0.0319,-0.3083,-6.8107)
    MAB_D=M_AB+A6/10
    bin_AB,bin_phi,error=gs.Utility.LumimosityFunction(MAB_D,boxsize_MPC/0.6736,20)
    XLF = bin_AB
    YLF = bin_phi
    ax.plot(XLF,YLF,'--',label=label)





for ax in [ax11]:
    ax.legend()
    ax.set_yscale("log")


DoforFile("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/b270325/SPM3/data/out_L150N2040_z7p0_st_chabrier300_bin.csv","L150N2040 (ST)",150,ax11)
DoforFile("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/b270325/SPM3/data/out_L150N2040_z7p0_stnb_chabrier300_bin.csv","L150N2040 (ST+NB)",150,ax11)
# DoforFile("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/b270325/SPM3/data/out_L150N2040_z7p0_stnbde_chabrier300_bin.csv","L150N2040 (ST+NB+DE)",150,ax11)

# DoforFile("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/SPM3/data/out_L250N2040_z7p0_st_chabrier300_bin.csv","L250N2040 (ST)",250,ax11)
# DoforFile("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/SPM3/data/out_L250N2040_z7p0_stnb_chabrier300_bin.csv","L250N2040 (ST+NB)",250,ax11)



x = [-16.526785714285715, -17.1875, -18.276785714285715, -19.151785714285715, -20.1875, -21.13392857142857, -21.50892857142857, -21.803571428571427, -22.151785714285715, -22.50892857142857, -23.473214285714285, -23.848214285714285, -23.955357142857142]
y = [-2.2781954887218046, -2.5338345864661656, -2.984962406015038, -3.3533834586466167, -3.8646616541353387, -4.360902255639098, -4.571428571428571, -4.7894736842105265, -4.93984962406015, -5.180451127819548, -6.007518796992481, -6.12781954887218, -6.285714285714286]
x=np.array(x)
y=np.array(y)
plt.plot(x,10**y,':',label="Astrid")




plt.legend()




#Harikane
year,z,MUV,MUV_p,MUV_n,phi,phi_p,phi_n,phi_exp = np.loadtxt("/mnt/home/student/cranit/RANIT/Repo/galspy/obs/uvlf/uvlf.txt",usecols=(1,2,3,4,5,6,7,8,9)).T

val = np.log10(phi * (10**phi_exp))
val_p = np.log10((phi + phi_p) * 10**phi_exp)
val_n = np.log10((phi + phi_n) * 10**phi_exp)


plt.plot(MUV,10**val,'.',ms=10,color='k',label="Harikane+24")
for m,n,p in zip(MUV,val_n,val_p):
    plt.plot([m,m],10**np.array([n,p]),'_-k')


# # Finkelstein
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

plt.plot(MUV,10**phi,'.',ms=10,color='r',label="Finkelstein+15")

for m,n,p in zip(MUV,phi_n,phi_p):
    plt.plot([m,m],10**np.array([n,p]),'_-r')






plt.show()
