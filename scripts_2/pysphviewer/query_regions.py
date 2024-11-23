import galspy,os
import numpy as np


L150N2040 = "/mnt/home/student/cranit/NINJA/simulations/L150N2040/SNAPS"
root = galspy.NavigationRoot(L150N2040)
SNAP_NUM = 63
GID = 1


pos = np.round(root.PIG(SNAP_NUM).FOFGroups.MassCenterPosition()[GID-1]/1000,2)
print(f"Position : x={pos[0]}  ;  y={pos[1]}  ;  z={pos[2]} in cMpc/h")


blobnames = sorted(os.listdir(root.PART(SNAP_NUM).DarkMatter.GroupID.path))
blobnames.remove("attr-v2")
blobnames.remove("header")

for blobname in blobnames:
    print(blobname,end='\r')
    gids = root.PART(SNAP_NUM).DarkMatter.GroupID([blobname])
    if GID in gids:
        print(f"BLOBNAME : {blobname}")
        break











