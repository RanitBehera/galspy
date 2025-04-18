# %%
import galspy as gs
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import KDTree
import pickle
from tqdm import tqdm
import os
from multiprocessing import Pool



SIM = gs.NavigationRoot(gs.NINJA.L150N2040_WIND_WEAK)
PIG = SIM.PIG(z=7)
UNITS=PIG.Header.Units


print("Target Box ".ljust(32,"="))
PIG.print_box_info()


print("\nReading Fields ".ljust(32,"="))
print("- Gas".ljust(8),">","Positions")
gas_pos = PIG.Gas.Position()
print("- Gas".ljust(8),">","Masses")
gas_mass = PIG.Gas.Mass()
print("- Gas".ljust(8),">","Metallicity")
gas_met = PIG.Gas.Metallicity()
print("- Gas".ljust(8),">","Smoothing Lengths")
gas_sml = PIG.Gas.SmoothingLength()
print("- FOF".ljust(8),">","GroupIDs")
fof_gids = PIG.FOFGroups.GroupID()
print("- FOF".ljust(8),">","Stellar Mass")
fof_st_mass = PIG.FOFGroups.MassByType().T[4]
print("- FOF".ljust(8),">","Block Index")
BS,BE = PIG.GetParticleBlockIndex(gs.GAS)
print("- Star".ljust(8),">","Central Location")
star_cpos = PIG.GetCentralStarPosition()


# MASK FOFS =======================
MIN_STAR_NUM = 16
min_st_mass = MIN_STAR_NUM*PIG.Header.MassTable()[4]
fof_mask = fof_st_mass>min_st_mass
print("\nFiltering Target FoFs ".ljust(32,'='))
print(" - Minimum Star Number","=",MIN_STAR_NUM)
print(" - Corresponding Minimum Stellar Mass","=",f"{min_st_mass*1e10:.02e}","Mo/h")
TFOF_GIDS = fof_gids[fof_mask]
print(" - Number of target FoF found","=",len(TFOF_GIDS))


# KERNELS =======================
def CubicSpline(r,h):
    C = (8/(np.pi*h**3))
    q = r/h
    I1=C*(1 - 6*(q**2) + 6*(q**3))
    I2=C*(2*((1-q)**3))
    I3=np.zeros_like(q)
    conditions = [q <= 0.5, np.logical_and(0.5 < q, q <= 1), q > 1]
    output = np.select(conditions,[I1,I2,I3])
    return output


Kernel = CubicSpline
print("\nUsing Kernel :",Kernel.__name__)



# ================================
# %%
def TargetFoF(tgid):
    tgas_pos = gas_pos[BS[tgid]:BE[tgid]]
    tgas_mass = gas_mass[BS[tgid]:BE[tgid]]
    tgas_sml = gas_sml[BS[tgid]:BE[tgid]]
    tgas_met = gas_met[BS[tgid]:BE[tgid]]
    spos = star_cpos[tgid]

    # Start point and end point
    spt=np.array(spos)
    ept_z = np.max(tgas_pos.T[2])        # <------ Towards Positive Z axis
    ept = np.array(spt)
    ept[2] = ept_z

    # Probe points
    PROBE_SPACING = 0.01*PIG.Header.BoxSize()/2040
    PROBE_RADIUS = np.max(gas_sml)

    num_points = np.int32((ept[2]-spt[2])/PROBE_SPACING)
    if num_points<0:print(tgid,ept[2],spt[2],PROBE_SPACING)
    zstops = np.linspace(spt[2],ept[2],num_points)
    probe_points = np.array([[spt[0],spt[1],zp] for zp in zstops])

    # Tree and Probe
    tree = KDTree(tgas_pos)
    if len(probe_points)==0:
        return (tgid,0,0)

    ngb_ids=tree.query_ball_point(probe_points,PROBE_RADIUS)
    probe_dens=np.zeros(len(probe_points))
    probe_mets=np.zeros(len(probe_points))
    for i in range(len(ngb_ids)):
        pp=probe_points[i]
        pp_ngb_ids=ngb_ids[i]
        pp_ngb_sml = tgas_sml[pp_ngb_ids]
        pp_ngb_dist = np.linalg.norm(tgas_pos[pp_ngb_ids]-pp,axis=1)
        # -------
        pp_ngb_mass = tgas_mass[pp_ngb_ids]
        pp_ngb_met_mass = tgas_mass[pp_ngb_ids]*tgas_met[pp_ngb_ids]
        # pp_ngb_mass = tgas_mass[pp_ngb_ids]*((tgas_met[pp_ngb_ids]/0.02)**0.7)
        # -------
        probe_dens[i]=np.sum(pp_ngb_mass*CubicSpline(pp_ngb_dist,pp_ngb_sml))
        probe_mets[i]=np.sum(pp_ngb_met_mass*CubicSpline(pp_ngb_dist,pp_ngb_sml))

    # ----- Units
    h=PIG.Header.HubbleParam()
    probe_dens *= PIG.Header.Units.Density * (h**2)   # Mass / Volume
    zstops *= PIG.Header.Units.Length/h
    # ----- Salting
    probe_dens +=1e-30 #To avoid divide by zero errors
    probe_Z = probe_mets/probe_dens
    # ----- Metallicity Scaling
    metal_factor=1
    probe_dens_Z=probe_dens*((probe_Z/0.02)**metal_factor)
    # ----- Density to Number
    X=0.75
    MH=1.67e-24
    probe_ndens = probe_dens * (X/MH)
    probe_ndens_Z = probe_dens_Z * (X/MH)
    # ----- Comoving to Physical
    probe_ndens *=(1+PIG.Header.Redshift())**3
    probe_ndens_Z *=(1+PIG.Header.Redshift())**3
    zstops /=(1+PIG.Header.Redshift())

    # ----- Integrate
    ds=np.diff(zstops)
    N=np.sum(probe_ndens[:-1]*ds)
    NZ=np.sum(probe_ndens_Z[:-1]*ds)

    # kappa = 2e21
    # epsilon=15
    # AV = N/(epsilon*kappa)


    return (tgid,N,NZ)




# %%
# TFOF_GIDS=TFOF_GIDS[1:20000]
clm_den = {}
with Pool(24) as pool:
    for tgid,N,NZ in tqdm(pool.imap_unordered(TargetFoF,TFOF_GIDS),total=len(TFOF_GIDS)):
        clm_den[tgid]=(N,NZ)

clm_den=dict(sorted(clm_den.items()))

DDIR="/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/column_density/data/"
filepath = DDIR + f"{PIG.sim_name}_{PIG.redshift_name}.dict"

os.makedirs(os.path.dirname(filepath), exist_ok=True)
with open(filepath,"wb") as fp:
    pickle.dump(clm_den,fp)



# %%
