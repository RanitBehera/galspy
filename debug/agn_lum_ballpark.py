import galspy
import numpy as np
import matplotlib.pyplot as plt
from galspy.utility.visualization import CubeVisualizer
import astropy


# MPGADGET_OUTPUT_DIR = "/mnt/home/student/cranit/Data/MP_Gadget/Nishi/L50N640"
MPGADGET_OUTPUT_DIR = "/mnt/home/student/cranit/NINJA/simulations/L150N2040/SNAPS"
SNAP = 52
GROUP_OFFSET = 0


root = galspy.NavigationRoot(MPGADGET_OUTPUT_DIR)

ac=root.PIG(SNAP).BlackHole.BlackholeAccretionRate() 
ac*= (1e10/3.08568e+16) * 365 * 24 * 3600 # M_sun /year
ac = ac.astype(np.float128)
ac=ac*(2e30)/(365*24*3600) #kg/sec
bm= root.PIG(SNAP).BlackHole.BlackholeMass()*1e10   # M_sun


c=3e8
Ang = 1e-10

# Rest Frame Bolometric Luminosity
L = 0.3 * ac * (c**2) # joules/sec

# plt.hist(np.log10(L*1e7),bins=100)
# plt.yscale("log")
# # plt.show()
# plt.savefig("temp/temp.png")

#region
if False:
    # Say 10% goes to UV Band from 1200-2400 Angstrom centered at 1500A
    lam = 1450 * Ang
    d_lam = (2400-1200) * Ang

    # Rest Frame Spectral Luminosity in UV band - wave
    f_lam = 0.1 * L / d_lam #jouls/sec/m

    # Rest Frame Spectral Luminosity in UV band - freq
    f_nu = ((lam**2)/c)*f_lam #jouls/sec/Hz
#endregion


#region

# plt.hist(np.log10(L*1e7),bins=100)
# plt.show()


# from astropy.cosmology import FlatLambdaCDM
# cosmo = FlatLambdaCDM(H0=67.36, Om0=0.3153)
# z=8
# DL=cosmo.luminosity_distance(z).value # In MPC

# ------ Rest to Obaserved

# plt.hist(f,bins=100)
# plt.plot()


# plt.plot(bm,ac,'.',ms=2)
# plt.xscale('log')
# plt.yscale('log')
# plt.show()

# print(L/)


# Blackhole mass,  accretion Rate
#endregion


def _lum_function_from_lum_list(Lum,VOLUME,LogBinStep):
    Lum = Lum[Lum!=0]

    log_Lum=np.log10(Lum)
    # log_Lum=np.log(Lum)
    # print(np.max(log_Lum))

    log_bin_start=np.floor(min(log_Lum))
    log_bin_end=np.ceil(max(log_Lum))

    BinCount=np.zeros(int((log_bin_end-log_bin_start)/LogBinStep))

    for lm in log_Lum:
        i=int((lm-log_bin_start)/LogBinStep)
        BinCount[i]+=1

    log_L=np.arange(log_bin_start,log_bin_end,LogBinStep)+(LogBinStep/2)
    dn_dlogL=BinCount/(VOLUME*LogBinStep)
    error=np.sqrt(BinCount)/(VOLUME*LogBinStep)

    return bin_AB,bin_phi,error



LL, dn_dlogL,error = _lum_function_from_lum_list(L*1e7,(150/0.67)**3,1)
plt.plot(LL,dn_dlogL,'-',color='k')
plt.fill_between(LL,dn_dlogL-0.9*error,dn_dlogL+0.9*error,color='k',alpha=0.2,ec=None)
plt.yscale("log")
plt.savefig("temp/temp.png")







