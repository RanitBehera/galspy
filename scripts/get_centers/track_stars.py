import galspy
import numpy as np
import matplotlib.pyplot as plt
import os
from galspy.utility.visualization import CubeVisualizer



SNAPSPATH = "/mnt/home/student/cranit/NINJA/simulations/L150N2040/SNAPS/"
SNAPNUM=43

ROOT = galspy.NavigationRoot(SNAPSPATH)

TPART = ROOT.PART(SNAPNUM)
TPIG = ROOT.PIG(SNAPNUM)

# Get available previos snaps
snaps = sorted([c for c in os.listdir(SNAPSPATH) if c.startswith("PART") and os.path.isdir(os.path.join(SNAPSPATH, c))])
sn = np.array([int(s.split('_')[-1]) for s in snaps])
mask = sn<=SNAPNUM
sn = sn[mask]
sn=sn[4:]


# Get final star ids and pos
tstar_ids = TPIG.Star.ID()
tstar_gids = TPIG.Star.GroupID()
tstar_pos = TPIG.Star.Position()

GID=1
mask = tstar_gids==GID
tstar_ids = tstar_ids[mask]
tstar_pos = tstar_pos[mask]

tstar_ids = tstar_ids.astype(np.int64)

cv=CubeVisualizer()
cv.add_points(tstar_pos)
ox,lx,oy,ly,oz,lz = cv.get_axis_anchors()


pts_zl=(0.5*(ox+lx),0.5*(oy+ly),oz)
pts_zu=(0.5*(ox+lx),0.5*(oy+ly),lz)
pts_yl=(0.5*(ox+lx),oy,0.5*(oz+lz))
pts_yu=(0.5*(ox+lx),ly,0.5*(oz+lz))
pts_xl=(ox,0.5*(oy+ly),0.5*(oz+lz))
pts_xu=(lx,0.5*(oy+ly),0.5*(oz+lz))
pts=np.array([pts_zl,pts_zu,pts_yl,pts_yu,pts_xl,pts_xu])


pts = None
for i,sni in enumerate(sn):
    if sni not in [4,43]:continue
    print(i+1,"/",len(sn),":",sni)
    PSNAP = ROOT.PART(int(sni))
    pstar_ids = PSNAP.Star.ID()
    pstar_pos = PSNAP.Star.Position()
    pstar_ids = pstar_ids.astype(np.int64)

    mask = np.isin(pstar_ids, tstar_ids)
    pstar_pos = pstar_pos[mask]


    cv=CubeVisualizer()
    cv.add_points(pstar_pos, points_color='r', points_size=10)

    if not i==0:
        cv.add_points(pts, points_color='b', points_size=0)
    else:
        ox,lx,oy,ly,oz,lz = cv.get_axis_anchors()
        pts_zl=(0.5*(ox+lx),0.5*(oy+ly),oz)
        pts_zu=(0.5*(ox+lx),0.5*(oy+ly),lz)
        pts_yl=(0.5*(ox+lx),oy,0.5*(oz+lz))
        pts_yu=(0.5*(ox+lx),ly,0.5*(oz+lz))
        pts_xl=(ox,0.5*(oy+ly),0.5*(oz+lz))
        pts_xu=(lx,0.5*(oy+ly),0.5*(oz+lz))
        pts=np.array([pts_zl,pts_zu,pts_yl,pts_yu,pts_xl,pts_xu])


    # ax=cv.show(False)
    # plt.savefig(f"/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/get_centers/imgs_star_track/pos_{sni}.png")
    cv.show()
