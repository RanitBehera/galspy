import galspy as gs
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import KDTree


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

def Target(tgid):
    # STEP 0 - Mask for target particles 
    tmask=gid==tgid
    tpos=pos[tmask]
    tmet=met[tmask]
    tsml=sml[tmask]
    tstar_pos = pos_star[gid_star==tgid]

    # STEP 1 - Build KDTree and  
    tree = KDTree(tpos)
    
    # STEP 2 - Sample Sightlines
    start_points = tstar_pos
    for i,sp in enumerate(start_points):
        if i>3:break
        print(i,sp,"--->")

    box_end = np.max(tpos.T[2])
    end_points  = np.array(start_points)
    end_points[:,2] = box_end*np.ones(len(end_points)) 

    for i,(sp,ep) in enumerate(zip(start_points,end_points)):
        if i>3:break
        print(i,sp,"--->",ep)

    # STEP 3 - Query for neighbours
    # res=tree.query_ball_point(tpos_star,1)
    # print(res)

Target(2)








