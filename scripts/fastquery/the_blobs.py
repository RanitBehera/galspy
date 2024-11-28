import galspy,os
import numpy as np
from multiprocessing import Pool

L150N2040 = "/mnt/home/student/cranit/NINJA/simulations/L150N2040/SNAPS"
root = galspy.NavigationRoot(L150N2040)
SNAP_NUM = 43


GID = 1

blobnames = sorted(os.listdir(root.PART(SNAP_NUM).Gas.GroupID.path))
blobnames.remove("attr-v2")
blobnames.remove("header")

for blobname in blobnames:
    print(f"{blobname}")
    gas_gids = root.PART(SNAP_NUM).Gas.GroupID()
    if GID in gas_gids:break