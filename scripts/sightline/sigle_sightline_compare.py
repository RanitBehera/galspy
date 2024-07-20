import galspy.IO.MPGadget as mp
import matplotlib.pyplot as plt
from galspy.utility.visualization import CubeVisualizer
import numpy as np
from scipy import spatial
import pickle
import galspy.utility.sightline as sl

# SIM = mp.NavigationRoot("/mnt/home/student/cranit/Data/MP_Gadget/Nishi/L10N64/output")
SIM = mp.NavigationRoot("/mnt/home/student/cranit/Data/MP_Gadget/Nishi/L50N640")
SNAP = 36
BOX_SIZE = SIM.PART(SNAP).Header()["BoxSize"]

print("Reading ...")
POSITION = SIM.PART(SNAP).Gas.Position()
VELOCITY = SIM.PART(SNAP).Gas.Velocity()
DENSITY = SIM.PART(SNAP).Gas.Density()
MASS = SIM.PART(SNAP).Gas.Mass()
SMOOTHING = SIM.PART(SNAP).Gas.SmoothingLength()
IENERGY = SIM.PART(SNAP).Gas.InternalEnergy()

print("Reading kdt pickle ...")
with open("/mnt/home/student/cranit/Repo/galspy/temp/outs/L50N640S36.ckdtree","rb") as fp:
    kdt = pickle.load(fp)

sight=sl.CartesianSightLine((np.array([0.5,0,0.5])*BOX_SIZE),np.array([0.5,1,0.5])*BOX_SIZE)

# Sightline Visualisation
#region
if True:
    fig = plt.figure()
    ax = fig.add_subplot(111,projection='3d')
    SMOOTHING_LENGTH = 200 # kpc 
    ind_within_cyl_of_infl = []
    STOPS = sight.Get_Steps(100)
    for i,stop in enumerate(STOPS):
        neighbours_index=kdt.query_ball_point(stop,2*SMOOTHING_LENGTH)
        ind_within_cyl_of_infl += neighbours_index


    ind_within_cyl_of_infl = list(set(ind_within_cyl_of_infl))
    # pos_in_cyl = kdt.data[ind_within_cyl_of_infl]
    pos_in_cyl = POSITION[ind_within_cyl_of_infl]
    cv=CubeVisualizer(ax)
    cv.add_points(pos_in_cyl,points_alpha=0.5,points_size=1)
    plt.tight_layout()
    cv.show()
#endregion


# Trace Fields
# def CubicSpline(r,h): #q=r/h
#     C = (8/(np.pi*h))
#     q = r/h

#     if q<=0 and q<=0.5: return C*(1 - 6*(q**2) + 6*(q**3))
#     elif q<0.5 and q<=1: return C*(2*((1-q)**3))
#     else: return 0


# def SPH_A(mb,Ab,rho_b,r,h):
#     return (mb*Ab/rho_b)*CubicSpline(r,h)


# STOPS = sight.Get_Steps(100)
# SMOOTHING_LENGTH = 200 #kpc

# NSTOP = len(STOPS)
# dens = np.zeros(NSTOP)
# ienr = np.zeros(NSTOP)
# Vx   = np.zeros(NSTOP)
# Vy   = np.zeros(NSTOP)
# Vz   = np.zeros(NSTOP)
# sight_dist  = np.zeros(NSTOP)  

# print("Tracing Sightline ...")
# for i,stop in enumerate(STOPS):
#     n_index=kdt.query_ball_point(stop,2*SMOOTHING_LENGTH)
#     n_crdn = POSITION[n_index]
#     # Relative to stop
#     n_rel_crdn = n_crdn - stop
#     n_rel_dist = np.linalg.norm(n_rel_crdn,axis=1)
    
#     n_dens      = DENSITY[n_index]
#     n_ienergy   = IENERGY[n_index]
#     n_velocity  = VELOCITY[n_index]
#     n_mass      = MASS[n_index]
#     n_smlength  = SMOOTHING[n_index]

    
#     dens[i] = np.sum([SPH_A(n_mass[j],n_dens[j],n_dens[j],n_rel_dist[j],n_smlength[j]) for j in range(len(n_index))]) 
#     ienr[i] = np.sum([SPH_A(n_mass[j],n_ienergy[j],n_dens[j],n_rel_dist[j],n_smlength[j]) for j in range(len(n_index))]) 
#     Vx[i]   = np.sum([SPH_A(n_mass[j],n_velocity[j][0],n_dens[j],n_rel_dist[j],n_smlength[j]) for j in range(len(n_index))]) 
#     Vy[i]   = np.sum([SPH_A(n_mass[j],n_velocity[j][1],n_dens[j],n_rel_dist[j],n_smlength[j]) for j in range(len(n_index))]) 
#     Vz[i]   = np.sum([SPH_A(n_mass[j],n_velocity[j][2],n_dens[j],n_rel_dist[j],n_smlength[j]) for j in range(len(n_index))]) 

#     sight_dist[i] = stop[1]




# print("plotting ...")

# plt.subplot(3,1,1)

# unit = 6.811e-22 #g/cm^3
# mass_hydro = 1.67e-24 #g
# X=0.76
# h=0.697
# dens *= X * (h**2) #h^3/h
# n_hydro = dens * unit / mass_hydro
# plt.plot(sight_dist,np.log10(n_hydro),label="Log10 Number Density $(cm^{-3})$")
# plt.legend()


# plt.subplot(3,1,2)
# plt.plot(sight_dist,ienr,label="Temperature")
# plt.legend()


# plt.subplot(3,1,3)
# plt.plot(sight_dist,Vx,label="Vx")
# plt.plot(sight_dist,Vy,label="Vy")
# plt.plot(sight_dist,Vz,label="Vz")
# plt.legend()

# plt.show()


