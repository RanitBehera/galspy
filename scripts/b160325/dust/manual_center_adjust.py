import numpy as np
import galspy
from galspy.utility.visualization import CubeVisualizer
import matplotlib.pyplot as plt

gids,_ = np.loadtxt("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/dust/data/gid_wdef32.txt").T
gids = np.int64(gids)

# Read
SNAPSPATH = "/mnt/home/student/cranit/NINJA/simulations/L150N2040/SNAPS/"
SNAPNUM=43

root = galspy.NavigationRoot(SNAPSPATH)

star_pos_all = root.PIG(SNAPNUM).Star.Position()
star_gid = root.PIG(SNAPNUM).Star.GroupID()

for gid in gids:
    if not gid==69699:continue
    print(gid)
    mask = star_gid==gid
    star_pos = star_pos_all[mask]

    cm=root.PIG(SNAPNUM).FOFGroups.MassCenterPosition()[gid-1]
    cx,cy,cz=cm

    cx+=0
    cy+=0
    cz+=0

    cm=np.array([cx,cy,cz])
    print(cm)

    cv=CubeVisualizer()
    cv.add_points([cm],1000,'k',points_marker='+')
    cv.add_points(star_pos,1,'r',points_alpha=0.5)

    cv.show()
    # plt.savefig(f"/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/dust/imgs/gid_{gid}.png")
# print(f"{gid} {cm[0]} {cm[1]} {cm[2]}")











