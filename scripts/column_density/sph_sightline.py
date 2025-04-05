# %%
import galspy as gs
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import KDTree
import time

SIM = gs.NavigationRoot(gs.NINJA.L150N2040)
PIG = SIM.PIG(z=7)
UNITS=PIG.Header.Units


print("READING","-"*62)
gid = PIG.Gas.GroupID()
pos = PIG.Gas.Position()
met = PIG.Gas.Metallicity()
sml = PIG.Gas.SmoothingLength()
den = PIG.Gas.Density()

gid_star = PIG.Star.GroupID()
pos_star = PIG.Star.Position()


# %%
def CubicSpline(r,h): #q=r/h
    C = (8/(np.pi*h**3))
    q = r/h
    I1=C*(1 - 6*(q**2) + 6*(q**3))
    I2=C*(2*((1-q)**3))
    I3=np.zeros_like(q)
    conditions = [q<=0.5,0.5<q & q<=1,q>1]
    output = np.select(conditions,[I1,I2,I3])

    return output


# %%
def Target(tgid):
    # STEP 0 - Mask for target particles 
    print("- STEP 0 : Masking for target particles ...")
    tmask=gid==tgid
    tpos=pos[tmask]
    tmet=met[tmask]
    tsml=sml[tmask]
    tstar_pos = pos_star[gid_star==tgid]

    # STEP 1 - Build KDTree  
    print("- STEP 1 : Building KDTree...")
    tree = KDTree(tpos)
    
    # STEP 2 - Sightlines and Sampling
    print("- STEP 2.1 : Choosing sightlines...")
    start_points = tstar_pos
    TOWARDS_AXIS = 'Z'
    TAXIS = {'X':0,'Y':1,'Z':2}[TOWARDS_AXIS.upper()]
    box_end = np.max(tpos.T[TAXIS])
    end_points  = np.array(start_points)    # to avoid copy by reference, once can use np.array() instead of copy() or deepcopy()
    end_points[:,TAXIS] = box_end*np.ones(len(end_points)) 
    # 
    print("- STEP 2.2 : Sampling sightlines...")
    sightline_lengths = np.linalg.norm(end_points-start_points,axis=1)
    min_sml = np.min(tsml)
    max_sml = np.max(tsml)
    avg_ips = PIG.Header.BoxSize()/2040
    min_sl = np.min(sightline_lengths)
    segment_length = avg_ips
    num_segments = 1 + np.int32(sightline_lengths/segment_length)
    unit_segments = (end_points-start_points)/num_segments[:,np.newaxis]
    segment_lengths = np.linalg.norm(unit_segments,axis=1)
    # segment is required due to np.int32() rounding
    probe_points = np.concatenate([(np.arange(nseg)[:,np.newaxis]*useg)+spt for nseg,useg,spt in zip(num_segments,unit_segments,start_points)])


    print(f"  - Number of probes {len(probe_points)}")
    print(f"  - Max SML {max_sml}")
    print(f"  - Min SML {min_sml}")
    print(f"  - Avg Spacing {avg_ips}")
    print(f"  - Min SL {min_sl}")

    # STEP 3 - Query for neighbours
    print("- STEP 3 : Neighbour query...")
    ts=time.time()
    res=np.array(tree.query_ball_point(probe_points,max_sml/10,workers=4))
    te=time.time()
    print(te-ts)
    print(res)

Target(2)

# %%
