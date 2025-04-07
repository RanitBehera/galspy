import numpy,os 
from multiprocessing import Pool
from tqdm import tqdm
import pickle

# ===================================================================
def GetForTargetGID(tgid):
    tmask = star_gid==tgid
    tstar_pot = star_pot[tmask]
    tstar_pos = star_pos[tmask]
    cloc=tstar_pos[numpy.argmin(tstar_pot)]
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
        # there might be Groups without stars
        all_st_len = PIG.FOFGroups.LengthByType().T[4]
        mask = all_st_len>0
        target_gids = all_gids[mask]

        cstar_loc = {}
        with Pool(num_pool_worker) as pool:
            for tgid,cloc in tqdm(pool.imap_unordered(GetForTargetGID,target_gids),total=len(target_gids)):
                cstar_loc[tgid]=cloc


        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath,"wb") as fp:
            pickle.dump(cstar_loc,fp)

    print(f"Using Cache File : {filepath}")
    with open(filepath,"rb") as fp:
        return pickle.load(fp)



# ===================================================================




















