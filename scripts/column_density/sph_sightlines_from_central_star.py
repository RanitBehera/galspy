# %%
import galspy as gs
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import KDTree
import pickle
from tqdm import tqdm
import os
from multiprocessing import Pool



SIM = gs.NavigationRoot(gs.NINJA.L150N2040)
PIG = SIM.PIG(z=6)
UNITS=PIG.Header.Units


print("Target Box ".ljust(32,"="))
PIG.print_box_info()


print("\nReading Fields ".ljust(32,"="))
print("- Gas".ljust(8),">","GroupIDs")
gas_gid = PIG.Gas.GroupID()
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
    tmask_gas = gas_gid==tgid
    tgas_pos = gas_pos[tmask_gas]
    tgas_mass = gas_mass[tmask_gas]
    tgas_sml = gas_sml[tmask_gas]
    tgas_met = gas_met[tmask_gas]
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
    probe_z = np.linspace(spt[2],ept[2],num_points)
    probe_points = np.array([[spt[0],spt[1],zp] for zp in probe_z])

    # Tree and Probe
    tree = KDTree(tgas_pos)
    if len(probe_points)==0:
        return (tgid,-1)

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

    # ----- Salting
    probe_dens +=1e-30 #To avoid divide by zero errors
    _Z = probe_mets/probe_dens
    # ----- Metallicity Scaling
    probe_dens *=(_Z/0.02)**1.0
    # ----- Units
    h=0.6736
    probe_dens *= PIG.Header.Units.Density * (h**2)   # Mass / Volume
    probe_z *= PIG.Header.Units.Length/h
    # ----- Density to Number
    probe_ndens = probe_dens * 0.75 / 1.67e-24
    # ----- Comoving to Physical
    probe_ndens *=(1+PIG.Header.Redshift())**3
    probe_z /=(1+PIG.Header.Redshift())

    # ----- Integrate
    ds=np.diff(probe_z)
    N=np.sum(probe_ndens[:-1]*ds)

    # ----- Convert to Physical
    kappa = 1/3e22
    AV = N*kappa


    return (tgid,N,AV)




# %%
clm_den = {}
with Pool(24) as pool:
    for tgid,cld,AV in tqdm(pool.imap_unordered(TargetFoF,TFOF_GIDS),total=len(TFOF_GIDS)):
        clm_den[tgid]=(cld,AV)

clm_den=dict(sorted(clm_den.items()))

filepath = f"/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/column_density/data/{PIG.sim_name}_z10p0_Av_a1p0.dict"

os.makedirs(os.path.dirname(filepath), exist_ok=True)
with open(filepath,"wb") as fp:
    pickle.dump(clm_den,fp)



# %%
