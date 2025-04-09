import numpy as np
import os 
from multiprocessing import Pool
from tqdm import tqdm
import pickle
from scipy.spatial import KDTree

# ===================================================================
def _get_central_star_position(tgid):
    tmask = star_gid==tgid
    tstar_pot = star_pot[tmask]
    tstar_pos = star_pos[tmask]
    cloc=tstar_pos[np.argmin(tstar_pot)]
    return (tgid, cloc)

def GetCentralStarPosition(filepath,PIG,num_pool_worker):
    if not os.path.exists(filepath):
        print("Central star location cache file not found ...")
        print("Creating Cache ...")

        global star_gid,star_pos,star_pot
        star_gid = PIG.Star.GroupID()
        star_pos = PIG.Star.Position()
        star_pot = PIG.Star.Potential()

        all_gids = PIG.FOFGroups.GroupID()
        all_st_len = PIG.FOFGroups.LengthByType().T[4]
        mask = all_st_len>0
        target_gids = all_gids[mask]

        cstar_loc = {}
        with Pool(num_pool_worker) as pool:
            for tgid,cloc in tqdm(pool.imap_unordered(_get_central_star_position,target_gids),total=len(target_gids)):
                cstar_loc[tgid]=cloc


        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath,"wb") as fp:
            pickle.dump(cstar_loc,fp)

    print(f"Using Cache File : {filepath}")
    with open(filepath,"rb") as fp:
        return pickle.load(fp)



# ===================================================================

# from galspy.MPGadget import _PIG


def CubicSpline(r,h): #q=r/h
    C = (8/(np.pi*h**3))
    q = r/h
    I1=C*(1 - 6*(q**2) + 6*(q**3))
    I2=C*(2*((1-q)**3))
    I3=np.zeros_like(q)
    conditions = [q <= 0.5, np.logical_and(0.5 < q, q <= 1), q > 1]
    output = np.select(conditions,[I1,I2,I3])

    return output

def _get_stellar_sph_column_density(star_id):
    tgid,spos=star_data_dict[star_id]
    # spos is star position which is also start position
    tmask = gas_gid==tgid
    tgas_pos = gas_pos[tmask]
    tgas_mass = gas_mass[tmask]
    tgas_met = gas_met[tmask]
    tgas_sml = gas_sml[tmask]

    # Start point and end point
    spt=np.array(spos)
    ept_z = np.max(tgas_pos.T[2])        # <------ Towards Positive Z axis
    ept = np.array(spt)
    ept[2] = ept_z

    # Probe points
    PROBE_SPACING = 0.1*avg_ips
    PROBE_RADIUS = np.max(gas_sml)

    num_points = np.int32((ept[2]-spt[2])/PROBE_SPACING)
    probe_z = np.linspace(spt[2],ept[2],num_points)
    probe_points = np.array([[spt[0],spt[1],zp] for zp in probe_z])

    # Tree and Probe
    tree = KDTree(tgas_pos)
    ngb_ids=tree.query_ball_point(probe_points,PROBE_RADIUS)
    probe_vals=np.zeros(len(probe_points))
    for i in range(len(ngb_ids)):
        pp=probe_points[i]
        pp_ngb_ids=ngb_ids[i]
        pp_ngb_sml = tgas_sml[pp_ngb_ids]
        pp_ngb_dist = np.linalg.norm(tgas_pos[pp_ngb_ids]-pp,axis=1)
        pp_ngb_mass = tgas_mass[pp_ngb_ids]
        probe_vals[i]=np.sum(pp_ngb_mass*CubicSpline(pp_ngb_dist,pp_ngb_sml))

    # Integrate
    ndens = probe_vals
    ds=np.diff(probe_z)

    N=np.sum(ndens[:-1]*ds)
    return (star_id,N)


    


def GetStellarSPHColumnDensity(filepath,PIG,num_pool_worker):
    if not os.path.exists(filepath):
        print("Stellar SPH column density cache file not found ...")
        print("Creating Cache ...")



        global gas_gid,gas_pos,gas_mass,gas_met,gas_sml
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


        global avg_ips
        avg_ips = PIG.Header.BoxSize()/2040
        print("- Star".ljust(8),">","GroupIDs")
        star_gid = PIG.Star.GroupID()
        print("- Star".ljust(8),">","Positions")
        star_pos = PIG.Star.Position()
        print("- Star".ljust(8),">","IDs")
        star_ids = PIG.Star.ID()

        global star_data_dict
        star_data_dict = dict(zip(star_ids,zip(star_gid,star_pos)))

        clm_den = {}
        star_ids = star_ids[:100]
        with Pool(num_pool_worker) as pool:
            for st_id,st_cld in tqdm(pool.imap_unordered(_get_stellar_sph_column_density,star_ids),total=len(star_ids)):
                clm_den[st_id]=st_cld

        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath,"wb") as fp:
            pickle.dump(clm_den,fp)

    print(f"Using Cache File : {filepath}")
    with open(filepath,"rb") as fp:
        return pickle.load(fp)




















