import galspy.IO.MPGadget as mp
import matplotlib.pyplot as plt
from galspy.utility.visualization import CubeVisualizer
import numpy as np
from scipy import spatial
import pickle, time
import galspy.utility.sightline as sl

SIM_PATH = "/mnt/home/student/cranit/Data/MP_Gadget/Nishi/L140N1008"
SNAP = 24
PICKLE_PATH = "/mnt/home/student/cranit/Repo/galspy/temp/outs/L140N1008_S24.ckdtree"

# ---------------
SIM = mp.NavigationRoot(SIM_PATH)
BOX_SIZE = SIM.PART(SNAP).Header()["BoxSize"]

start_time = time.time()
def elapsed():return "[" + f"{round(time.time()-start_time)}".rjust(5) + "s] "

# ---------------
if True:
    print(elapsed() + "Reading Position ...")
    POSITION = SIM.PART(SNAP).Gas.Position()
    print(elapsed() + "Reading Velocity ...")
    VELOCITY = SIM.PART(SNAP).Gas.Velocity()
    print(elapsed() + "Reading Density ...")
    DENSITY = SIM.PART(SNAP).Gas.Density()
    print(elapsed() + "Reading Mass ...")
    MASS = SIM.PART(SNAP).Gas.Mass()
    print(elapsed() + "Reading SmoothingLength ...")
    SMOOTHING = SIM.PART(SNAP).Gas.SmoothingLength()
    print(elapsed() + "Reading Internal Energy ...")
    IENERGY = SIM.PART(SNAP).Gas.InternalEnergy()
    print(elapsed() + "Reading kdt pickle ...")
    with open(PICKLE_PATH,"rb") as fp:kdt = pickle.load(fp)

# ---------------
# GET LOS to compare
def get_los_data(path):
    with open(path) as fp: head = fp.readline()
    data = np.loadtxt(path)
    target_str = head.split(',')[0][:-1].split('#')[-1].split('_')
    C0,C1,C2 = [int(target_str[0]),float(target_str[1]),float(target_str[2])]    
    return data, [C0,C1,C2]

ORIGIN = np.array([6099.15254055,5441.4186793,1950.43327123])
ORIGIN = np.array([1.016110515594482422e+01, 1.519624996185302734e+01, 1.630469894409179688e+01]) * 1000 / BOX_SIZE


los0,_ = get_los_data("/mnt/home/student/cranit/Repo/galspy/temp/los/LOS_140Mpc1008cube_z10_0_group_0_modified_conditions1.txt")
los1,_ = get_los_data("/mnt/home/student/cranit/Repo/galspy/temp/los/LOS_140Mpc1008cube_z10_1_group_0_modified_conditions1.txt")
los2,_ = get_los_data("/mnt/home/student/cranit/Repo/galspy/temp/los/LOS_140Mpc1008cube_z10_2_group_0_modified_conditions1.txt")

START = np.array([0,5441.4186793,1950.43327123]) /BOX_SIZE
START0 = np.array([0, 1.519624996185302734e+01, 1.630469894409179688e+01]) * 1000 / BOX_SIZE
START1 = np.array([1.016110515594482422e+01, 0, 1.630469894409179688e+01]) * 1000 / BOX_SIZE
START2 = np.array([1.016110515594482422e+01, 1.519624996185302734e+01, 0]) * 1000 / BOX_SIZE

END = np.array([10000,5441.4186793,1950.43327123]) /BOX_SIZE
END0 = np.array([140, 1.519624996185302734e+01, 1.630469894409179688e+01]) * 1000 / BOX_SIZE
END1 = np.array([1.016110515594482422e+01, 140, 1.630469894409179688e+01]) * 1000 / BOX_SIZE
END2 = np.array([1.016110515594482422e+01, 1.519624996185302734e+01, 140]) * 1000 / BOX_SIZE

sight=sl.CartesianSightLine(START*BOX_SIZE,END*BOX_SIZE)
sight0=sl.CartesianSightLine(START0*BOX_SIZE,END0*BOX_SIZE)
sight1=sl.CartesianSightLine(START1*BOX_SIZE,END1*BOX_SIZE)
sight2=sl.CartesianSightLine(START2*BOX_SIZE,END2*BOX_SIZE)

sight = sight0
# Sightline Visualisation
#region
if False:
    fig = plt.figure()
    ax = fig.add_subplot(111,projection='3d')
    SMOOTHING_LENGTH = max(SMOOTHING) # kpc 
    ind_within_cyl_of_infl = []
    STOPS = sight.Get_Stops(100)
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
def CubicSpline(r,h): #q=r/h
    C = (8/(np.pi*h))
    q = r/h

    if q<=0 and q<=0.5: return C*(1 - 6*(q**2) + 6*(q**3))
    elif q<0.5 and q<=1: return C*(2*((1-q)**3))
    else: return 0


def SPH_A(mb,Ab,rho_b,r,h):
    return (mb*Ab/rho_b)*CubicSpline(r,h)


STOPS = sight.Get_Stops(2016)
SMOOTHING_LENGTH = max(SMOOTHING) #kpc

NSTOP = len(STOPS)
dens = np.zeros(NSTOP)
ienr = np.zeros(NSTOP)
Vx   = np.zeros(NSTOP)
Vy   = np.zeros(NSTOP)
Vz   = np.zeros(NSTOP)
sight_dist  = np.zeros(NSTOP)  


print(elapsed() + "Tracing Sightline ...")
for i,stop in enumerate(STOPS):
    n_index=kdt.query_ball_point(stop,2*SMOOTHING_LENGTH)
    n_crdn = POSITION[n_index]
    # Relative to stop
    n_rel_crdn = n_crdn - stop
    n_rel_dist = np.linalg.norm(n_rel_crdn,axis=1)
    
    n_dens      = DENSITY[n_index]
    n_ienergy   = IENERGY[n_index]
    n_velocity  = VELOCITY[n_index]
    n_mass      = MASS[n_index]
    n_smlength  = SMOOTHING[n_index]

    
    dens[i] = np.sum([SPH_A(n_mass[j],n_dens[j],n_dens[j],n_rel_dist[j],n_smlength[j]) for j in range(len(n_index))]) 
    ienr[i] = np.sum([SPH_A(n_mass[j],n_ienergy[j],n_dens[j],n_rel_dist[j],n_smlength[j]) for j in range(len(n_index))]) 
    Vx[i]   = np.sum([SPH_A(n_mass[j],n_velocity[j][0],n_dens[j],n_rel_dist[j],n_smlength[j]) for j in range(len(n_index))]) 
    Vy[i]   = np.sum([SPH_A(n_mass[j],n_velocity[j][1],n_dens[j],n_rel_dist[j],n_smlength[j]) for j in range(len(n_index))]) 
    Vz[i]   = np.sum([SPH_A(n_mass[j],n_velocity[j][2],n_dens[j],n_rel_dist[j],n_smlength[j]) for j in range(len(n_index))]) 

    sight_dist[i] = stop[0]




print("plotting ...")
plt.subplot(3,1,1)

# ---- DENSITY

unit = 6.811e-22 #g/cm^3
mass_hydro = 1.67e-24 #g
X=0.76
h=0.697
dens *= X * (h**2) #h^3/h
n_hydro = dens * unit / mass_hydro

kpc_to_cm = 3.086e+21

# label="Log10 Number Density $(cm^{-3})$"

# print(len(sight_dist),len(n_hydro))
plt.plot(sight_dist*kpc_to_cm,n_hydro)

cdens = los0[:,8]
cpos = los0[:,0]
plt.plot(cpos,cdens)

# plt.legend()





# plt.subplot(3,1,2)
# plt.plot(sight_dist,ienr,label="Temperature")
# plt.legend()


# plt.subplot(3,1,3)
# plt.plot(sight_dist,Vx,label="Vx")
# plt.plot(sight_dist,Vy,label="Vy")
# plt.plot(sight_dist,Vz,label="Vz")
# plt.legend()


plt.show()


