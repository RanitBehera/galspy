import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.ndimage import gaussian_filter


table = np.loadtxt("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/get_centers/data/subokay.txt")
gid,nsubs,subid,nstar_group,nstar_sub,st_mass_fof,st_mass_sum,st_mass_sub,cx,cy,cz,cr=table.T


massmap = {}
for g,stm in zip(gid,st_mass_sub):
    massmap[int(g)]=stm

NHmap={}

# ===========


DIR="/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/get_centers/data/profs"
FILES = sorted(os.listdir(DIR))

h=0.6736
z=7
Ob=0.0493
n_igm = (1.6e-7)*(Ob*(h**2)/0.019)*((1+z)**3)

fig,axs = plt.subplots(1,2)
axs:list[plt.Axes]

for file in FILES:
    print(file)
    filepath = DIR + os.sep + file
    r,rho,nH = np.loadtxt(filepath).T
    axs[0].plot(r,nH)

    # 
    mask = ~(np.abs(nH)==np.inf)
    r,rho,nH=r[mask],rho[mask],nH[mask]

    # Integrate for
    r = r*(3.086e21)  #pkpc to cm
    dr=np.diff(r)
    nH=nH[:-1]
    NH = np.sum(nH*dr)

    g=int(file.split("_")[-1].split('.')[0])
    NHmap[g]=NH


axs[0].axhline(n_igm)
axs[0].set_xscale("log")
axs[0].set_yscale("log")
axs[0].axvline((10000/0.6736)/(1+7))
axs[0].set_xlabel("Radius (pkpc)")
axs[0].set_ylabel("nH ($cm^{-3}$)")

st_arr = []
NH_arr=[]

for file in FILES:
    g=int(file.split("_")[-1].split('.')[0])
    st_arr.append(massmap[g])
    NH_arr.append(NHmap[g])

st_arr=np.array(st_arr)
NH_arr=np.array(NH_arr)

axs[1].plot(st_arr*1e10/0.6736,NH_arr,'.',ms=10)
axs[1].set_xscale("log")
axs[1].set_yscale("log")

axs[1].set_xlabel("Cluster Stellar Mass ($M_\odot$)")
axs[1].set_ylabel("Column Density (gm $cm^{-2}$)")

plt.show()
