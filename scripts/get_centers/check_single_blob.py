import numpy as np
from galspy.utility.MassFunction import MassFunction
import matplotlib.pyplot as plt


table = np.loadtxt("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/get_centers/data/subinfo.txt")
gid,nsubs,subid,nstar_group,nstar_sub,st_mass_fof,st_mass_sum,st_mass_sub=table.T

st_mass_fof*=1e10
st_mass_sum*=1e10
st_mass_sub*=1e10


mask_single_blob=(nsubs==1)
st_mass_fof=(st_mass_fof[mask_single_blob])
st_mass_sub=(st_mass_sub[mask_single_blob])

delta_m=st_mass_fof-st_mass_sub
ratio = delta_m/st_mass_fof



gid_t = gid[mask1]


# from scipy.stats import gaussian_kde
# xy=np.vstack([st_mass_fof,st_mass_sub])
# print("Running Gaussian-KDE ... ( Turn OFF for fast plotting )")
# z=gaussian_kde(xy)(xy)
# plt.scatter(st_mass_fof,st_mass_sub,c=z,s=1,cmap='viridis')
# # plt.colorbar()

diff = np.log10(st_mass_fof)-np.log10(st_mass_sub)

print(f"Total {len(diff)}")
mask2 = diff>0.3


# mask = mask1 & mask2

gid_tt=gid_t[mask2]

# print(gid_tt)

# print(f"Masked {len(diff[mask])}")




plt.plot(st_mass_fof,st_mass_sub,'.')


minm=np.min(st_mass_fof)/10
maxm=np.max(st_mass_fof)*10
plt.plot([minm,maxm],[minm,maxm],color='k',ls='-',lw=1.5,alpha=0.3)

plt.xscale("log")
plt.yscale("log")
plt.axis("equal")


plt.show()