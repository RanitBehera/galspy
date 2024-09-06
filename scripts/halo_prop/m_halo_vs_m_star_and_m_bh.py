import galspy
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams["font.size"]=16


SNAP_PATH = "/mnt/home/student/cranit/NINJA/simulations/L150N2040/SNAPS"
SNAP_PATH = "/mnt/home/student/cranit/Data/MP_Gadget/Nishi/L50N640"
root = galspy.NavigationRoot(SNAP_PATH)

MASS_UNIT = 1e10 

hm  = root.PIG(20).FOFGroups.Mass()*MASS_UNIT
mbt = root.PIG(20).FOFGroups.MassByType().T * MASS_UNIT
sm = mbt[4]
bm = root.PIG(20).FOFGroups.BlackholeMass() * MASS_UNIT

plt.plot(hm,sm,'r*',ms=4,label="Star")
plt.plot(hm,bm,'k.',ms=10,label="Blackhole")

# Star unit mass
for i in range(4):
    plt.axhline((i*0.000543966/4)*MASS_UNIT,color='r',ls=':')



# BH Seeding
plt.axvline(0.5*MASS_UNIT,color='k',ls='--',lw=0.5)
plt.axhline(0.001*MASS_UNIT,color='k',ls='--',lw=0.5)
plt.axhspan((3.0e-6)*MASS_UNIT,(3.0e-5)*MASS_UNIT,color=(0,0,0),alpha=0.1)



plt.xscale('log')
plt.yscale('log')
plt.legend()
plt.xlim(3e8,1e11)
plt.ylim(1e4,1e9)

plt.xlabel("Halo Mass $M_\odot$")
plt.ylabel("Mass $M_\odot$")

plt.show()
