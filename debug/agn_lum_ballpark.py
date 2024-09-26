import galspy
import numpy
import matplotlib.pyplot as plt
from galspy.utility.visualization import CubeVisualizer
import astropy


# MPGADGET_OUTPUT_DIR = "/mnt/home/student/cranit/Data/MP_Gadget/Nishi/L50N640"
MPGADGET_OUTPUT_DIR = "/mnt/home/student/cranit/NINJA/simulations/L150N2040/SNAPS"
SNAP = 51
GROUP_OFFSET = 0


root = galspy.NavigationRoot(MPGADGET_OUTPUT_DIR)
# PIG = root.PIG(SNAP)

ac=root.PIG(34).BlackHole.BlackholeAccretionRate()
bm= root.PIG(34).BlackHole.BlackholeMass()*1e10


plt.plot(bm,ac,'.',ms=2)
plt.xscale('log')
plt.yscale('log')
plt.show()


exit()


if False:
    print(ac.dtype)
    max_float32 = numpy.finfo(numpy.float32).max
    print(max_float32)
    print("-"*32)

    print(ac)

    # Touch the bound
    print(max(ac*1e20*1e20*1.38))
    print(max(ac*1e20*1e20*1.39))

    # Okay
    print(max(ac*4e40))
    print(max(ac*2e20*2e20))



ac = ac.astype(numpy.float128)
ac=ac #M_sun/year
ac=ac*(2e30)/(365*24*3600) #kg/sec
# print(max(ac))
c=3e8
L = 0.1 * ac * (c**2) #SI Rest


z=8
from astropy.cosmology import FlatLambdaCDM
cosmo = FlatLambdaCDM(H0=67.36, Om0=0.3153)
DL=cosmo.luminosity_distance(z).value # In MPC

# ------ Rest to Obaserved
m_per_Mpc = 3.086e22
DL *= m_per_Mpc
Area = 4*numpy.pi*(DL**2)
f=L/Area #SI Observed : J s-1 m-2


# ----- Bolometric to Spectral
# f=0.1*f #- 10% in UV

# Jy = 1e-26
# Ang = 1e-10

# d_lam = 1000 * Ang * (1+z)
# lam = 1500 * Ang * (1+z)

# d_nu = (c/(lam**2))*d_lam


# f=(f/d_nu)/Jy

# m_AB = -2.5*numpy.log10(f)+8.90






# plt.hist(f,bins=100)
# plt.plot()


# plt.plot(bm,ac,'.',ms=2)
# plt.xscale('log')
# plt.yscale('log')
# plt.show()

# print(L/)


# Blackhole mass,  accretion Rate
