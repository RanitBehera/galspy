import numpy as np
import matplotlib.pyplot as plt
from galspec.Utility import LuminosityFunction
import galspy




GID,BLOBNUM,UV_F115W_ST,UV_F115W_STNB,SUM_ST_W0,SUM_ST_WO0,SUM_STNB_W0,SUM_STNB_WO0 = np.loadtxt("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/SPM2/data/blob_UV.txt").T


BOXSIZE=150/0.6736







LSOL=3.846e33 #erg s-1
def Lum2MAB(L):
    uvlum = L
    # uvlum=L/200 #roughly 1400A to 1600A    or 1257 to 1611          # <------
    
    uvlum =uvlum*LSOL # erg s-1 AA-1

    PC2CM = 3.086e18
    D = 10*PC2CM  # In cm

    flam=uvlum/(4*np.pi*D**2)

    # lam . f_lam = nu . f_nu
    c=3e8*1e10  #in AA s-1
    lam = 1437 #in AA in rest

    fnu = (lam**2)*flam/c #erg s-1 cm-2 Hz-1 at obs
    Jy=1e-23 #erg s-1 cm-2 Hz-1

    mAB = -2.5*np.log10(fnu/(3631*Jy))
    M_AB = mAB #as distance was 10pc

    return M_AB



def plot_blobwise_lf():
    mask=BLOBNUM!=0
    uvlum_st = UV_F115W_ST[mask]
    uvlum_stnb = UV_F115W_STNB[mask]
    log_L,dn_dlogL,error = LuminosityFunction(Lum2MAB(uvlum_st),BOXSIZE**3,0.5)
    plt.plot(log_L,dn_dlogL,label="BLOB-wise (Stellar)")
    log_L,dn_dlogL,error = LuminosityFunction(Lum2MAB(uvlum_stnb),BOXSIZE**3,0.5)
    plt.plot(log_L,dn_dlogL,label="BLOB-wise (Stellar+Nebular)")

plot_blobwise_lf()


def plot_gidwise_lf():
    unq,ind= np.unique(GID,return_index=True)
    uvlum_st = SUM_ST_W0[ind]
    uvlum_stnb = SUM_STNB_W0[ind]
    log_L,dn_dlogL,error = LuminosityFunction(Lum2MAB(uvlum_st),BOXSIZE**3,0.5)
    plt.plot(log_L,dn_dlogL,label="GID-wise-W (Stellar)")
    log_L,dn_dlogL,error = LuminosityFunction(Lum2MAB(uvlum_stnb),BOXSIZE**3,0.5)
    plt.plot(log_L,dn_dlogL,label="GID-wise-W (Stellar+Nebular)")

    uvlum_st = SUM_ST_WO0[ind]
    uvlum_stnb = SUM_STNB_WO0[ind]
    log_L,dn_dlogL,error = LuminosityFunction(Lum2MAB(uvlum_st),BOXSIZE**3,0.5)
    plt.plot(log_L,dn_dlogL,label="GID-wise-WO (Stellar)")
    log_L,dn_dlogL,error = LuminosityFunction(Lum2MAB(uvlum_stnb),BOXSIZE**3,0.5)
    plt.plot(log_L,dn_dlogL,label="GID-wise-WO (Stellar+Nebular)")

plot_gidwise_lf()



def plot_lf_sfr():
    root=galspy.NavigationRoot("/mnt/home/student/cranit/NINJA/simulations/L150N2040/SNAPS/")
    sfr = root.PIG(43).FOFGroups.StarFormationRate()

    KUV=1.15e-28  #Msol yr-1 erg S-1 Hz-1
    LUV = sfr[sfr>0.03]/KUV

    PC2CM = 3.086e18
    D = 10*PC2CM  # In cm

    fUV = LUV/(4*np.pi*D**2)
    Jy=1e-23 #erg s-1 cm-2 Hz-1
    mAB = -2.5*np.log10(fUV/(3631*Jy))
    M_AB = mAB #as distance was 10pc
    

    log_L,dn_dlogL,error = LuminosityFunction(M_AB,BOXSIZE**3,0.5)   # 200 multiplied so that it gets cancelled in the other logic
    plt.plot(log_L,dn_dlogL,label="MD Scaling")

plot_lf_sfr()







x = [-22.965968509217227, -22.714659508937057, -22.431937018434454, -22.094240830167536, -21.67801001759394, -21.175392736034077, -20.594240470667298, -19.97382215139801, -19.345549470947468, -18.803664697484145, -18.308900339104593, -17.735602434919073, -17.264398284081402]
y = [-7.426086369245929, -6.730434553005776, -6.026086820375284, -5.399999946925958, -4.782608591811657, -4.2347825775434975, -3.765217422456503, -3.36521760821565, -3.008695783705235, -2.739130535738666, -2.5304349112555586, -2.2434784275912847, -2.0347828031081754]
y=10**np.array(y)
plt.plot(x,y,label="Cosmos-Web")

plt.xlabel("$M_{UV}$")
plt.ylabel("$\phi$")

plt.yscale("log")
# plt.xlim(-24,-18)
plt.legend()
plt.show()
