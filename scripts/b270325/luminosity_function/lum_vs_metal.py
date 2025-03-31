import galspy as gs
import numpy as np
import matplotlib.pyplot as plt



data = np.loadtxt("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/b270325/SPM3/data/out_L150N2040_z7p0_st_chabrier300_bin.csv",
                  usecols=(1,5))
TGID,MAB = data.T
TGID = np.int64(TGID)

SIM = gs.NavigationRoot(gs.NINJA.L150N2040)
PIG = SIM.PIG(SIM.SnapNumFromRedshift(7))

# -----------------------------------------------------------

MMASS = PIG.FOFGroups.GasMetalMass()[TGID-1]
GMASS = PIG.FOFGroups.MassByType().T[0][TGID-1]
SMASS = PIG.FOFGroups.MassByType().T[4][TGID-1]

AVG_Z_by_M = MMASS/GMASS


# plt.plot(MAB,AVG_Z_by_M,'.',ms=2)
Y=np.log10(AVG_Z_by_M/0.02)
# plt.hexbin(MAB[Y<-2.75],Y[Y<-2.75],gridsize=100,cmap="Blues",bins='log',extent=(-28,-14,-10,0))
plt.hexbin(MAB,Y,gridsize=100, cmap="Oranges",bins='log',extent=(-28,-14,-3,0))

# plt.axhline(0,color='k',ls='--',lw=1)
# plt.axhline(-2.75,color='k',ls='--',lw=1)
# plt.axhspan(0,-2.75,color='orange',alpha=0.05)
plt.axvline(-19.5,color='k',ls='--',lw=1)
plt.axvline(-20.85,color='k',ls='--',lw=1)

plt.colorbar()
plt.xlabel("$M_{UV}$")
plt.ylabel("$\left<Z_m\\right>$")

# plt.annotate(f"f={len((Y[MAB< -19.5])[Y[MAB< -19.5]> -2.75])/len(Y[MAB< -19.5])*100:.02f}%",(0,1),(8,-8),"axes fraction","offset pixels",va="top",ha="left")

# print(len(Y[Y> -3]))
plt.xlim(-28,-14)
plt.ylim(-3,0)
# plt.show()
# exit()


# -------------------------
target= TGID[0]
print("TGID",target)

gas_gid = PIG.Gas.GroupID()
mask = gas_gid==target
gas_mass = PIG.Gas.Mass()[mask]
gas_met = PIG.Gas.Metallicity()[mask]
gas_pos = PIG.Gas.Position()[mask]
gas_sfr = PIG.Gas.StarFormationRate()[mask]

star_gid = PIG.Star.GroupID()
mask = star_gid==target
star_mass = PIG.Star.Mass()[mask]
star_met = PIG.Star.Metallicity()[mask]
star_pos = PIG.Star.Position()[mask]


# plt.figure()
# plt.hist(np.log10(gas_met[~(gas_met==0)]/0.02),bins=100)



from galspy.Utility.Visualization import Cube3D


mask_met = np.log10(gas_met/0.02)> -1
mask_sfr = np.log10(gas_sfr)> -3

plt.figure()
c3d = Cube3D()
c3d.add_points(gas_pos[mask_met],points_size=10,points_color='b')
c3d.add_points(gas_pos[~mask_met],points_size=5,points_color='y')
c3d.add_points(star_pos,points_size=5,points_color='r')
c3d.show(False)

plt.figure()
c3d = Cube3D()
c3d.add_points(gas_pos[mask_sfr],points_size=10,points_color='b')
c3d.add_points(gas_pos[~mask_sfr],points_size=5,points_color='y')
c3d.add_points(star_pos,points_size=5,points_color='r')
c3d.show(False)







# plt.figure()
# def GetA(mstar,mab,m1,m2,K):
#     return 10**(m1*np.log10(mstar)+m2*mab+K)

# A6=GetA(SMASS*1e10/0.6736,MAB,0.0319,-0.3083,-6.8107)
# A8=GetA(SMASS*1e10/0.6736,MAB,0.5585,-0.0953,-6.9932)

# plt.plot(MAB,A8,'.',ms=2,label="z=8")
# plt.plot(MAB,A6,'.',ms=2,label="z=6")
# plt.yscale("log")

# plt.xlabel("$M_{AB}$")
# plt.ylabel("$A_{1500}$")
# plt.title("z=7")
# plt.legend()
plt.show()
 












