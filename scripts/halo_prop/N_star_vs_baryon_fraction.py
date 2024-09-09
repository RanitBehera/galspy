import galspy
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams["font.size"]=16


SNAP_PATH = "/mnt/home/student/cranit/NINJA/simulations/L150N2040/SNAPS"
SNAP_PATH = "/mnt/home/student/cranit/Data/MP_Gadget/Nishi/L50N640"
root = galspy.NavigationRoot(SNAP_PATH)

MASS_UNIT = 1e10 
SNAP_NUM=36

hm  = root.PIG(SNAP_NUM).FOFGroups.Mass()*MASS_UNIT
mbt = root.PIG(SNAP_NUM).FOFGroups.MassByType().T * MASS_UNIT
dm = mbt[1]
gm = mbt[0]
sm = mbt[4]

ns = root.PIG(SNAP_NUM).FOFGroups.LengthByType().T[4]
ng = root.PIG(SNAP_NUM).FOFGroups.LengthByType().T[0]

nt=ns+ng

bf = (gm+sm)/(gm+sm+dm)

count = root.PIG(SNAP_NUM).FOFGroups.LengthByType().T
dm_count = count[1]



mask = (dm_count>200)
# bf=bf[mask]




fig,axs = plt.subplots(1,2)

# SCATTER PLOT
axs[0].plot(nt,bf,'y.',ms=4)
# axs[0].set_xscale('log')
# axs[0].set_yscale('log')
axs[0].set_xlabel("Number of Stars $M_\odot$")
axs[0].set_ylabel("Baryon Fraction $M_\odot$")

axs[0].axhline(0.0493/0.3153,color='k')

# # BARYON FRACTION DISTRIBUTION
# axs[1].hist(bf,bins=20,color='y',)
# axs[1].set_xlabel("Baryon Fraction $f_b$")
# axs[1].set_ylabel("Halo Count")
# axs[1].set_yscale('log')
# axs[1].axvline(0.0493/0.3153,color='k')


# axs[1].plot(gm[mask],bf[mask],'.',ms=5)
# axs[1].set_xscale('log')
# axs[1].set_yscale('log')
# axs[1].set_xlabel("Halo Mass $M_\odot$")
# axs[1].set_ylabel("Baryon fraction")

# axs[1].axhline(0.0493/0.3153,color='k')
# axs[1].axhline(0.0493/0.3153,color='k')





plt.show()
