import numpy as np
from galspy.utility.MassFunction import MassFunction
import matplotlib.pyplot as plt


table = np.loadtxt("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/get_centers/data/subokay.txt")
gid,nsubs,subid,nstar_group,nstar_sub,st_mass_fof,st_mass_sum,st_mass_sub,cx,cy,cz,cr=table.T

# Filter for single system
mask_single = nsubs==1
gid,nsubs,subid,nstar_group,nstar_sub,st_mass_fof,st_mass_sum,st_mass_sub,cx,cy,cz,cr=table[mask_single].T


# Filter for single system
unique_gids = np.int64(np.unique(gid))
subsum = {}
for ugid in unique_gids:
    subsum[ugid]=0

for ugid,sub_mass in zip(gid,st_mass_sub):
    subsum[ugid] +=sub_mass

subsum=np.array(list(subsum.values()))
recovery_fraction = subsum/st_mass_fof


mask_rec = (recovery_fraction>0.95)&(recovery_fraction<1.0)

okgid=np.int32(gid[mask_rec])


# ====
print(len(okgid))
print(okgid)

# np.savetxt("scripts/get_centers/data/subok.txt",table[mask_single][mask_rec],fmt='%d %d %d %d %d %.08f %.8f %.8f')
