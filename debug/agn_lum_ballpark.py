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

ac=root.PART(51).BlackHole.BlackholeAccretionRate()
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


from astropy.cosmology import FlatLambdaCDM
cosmo = FlatLambdaCDM(H0=67.36, Om0=0.3153)
D=cosmo.luminosity_distance(8).value # In MPC
D *= 3.086e22 #in m

f=L/(4*numpy.pi*(D**2)*((1+8)**2)) #SI Observed
Jy = 1e-26
f=f/Jy

plt.hist(numpy.log10(f),bins=100)
plt.yscale('log')
plt.show()

# print(L/)
