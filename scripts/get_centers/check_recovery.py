import numpy as np
import matplotlib.pyplot as plt




# FILEPATH = "/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/get_centers/data/clusterinfo200.1.txt"
def DoForFile(FILEPATH,**kwargs):

    gid,nsubs,subid,nstar_group,nstar_sub,st_mass_sum,st_mass_sub,gid_rec_count,gid_rec_count_frac,gid_rec_mass,gid_rec_mass_frac,cx,cy,cz,cr=np.loadtxt(FILEPATH).T
    u,ind=np.unique(gid,return_index=True)

    unq_gid = gid[ind]
    unq_gid_rec_mass_frac=gid_rec_mass_frac[ind]
    unq_st_mass_sum = st_mass_sum[ind]

    # print(len(unq_gid))

    # for ui,ni in zip(ugid,nstar_group):
    #     print(int(ui),int(ni))


    mrf=np.linspace(0.0,1,100)

    nhalo=[]
    for u in mrf:
        mask=unq_gid_rec_mass_frac>u
        temp = unq_gid_rec_mass_frac[mask]
        nhalo.append(len(temp)/len(unq_gid))

    ax1.plot(mrf,nhalo,**kwargs)
    ax2.plot(unq_st_mass_sum,unq_gid_rec_mass_frac,'.',color=kwargs["c"],ms=2)


fig,axs=plt.subplots(1,2)
ax1,ax2=axs

# DoForFile("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/get_centers/data/clusterinfo200_p05.txt",c='r',label="p=0.5")
# DoForFile("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/get_centers/data/clusterinfo200_p03.txt",c='g',label="p=0.3")
DoForFile("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/get_centers/data/clusterinfo700_010125.txt",c='g',label="p=0.3")


ax1.set_yticks(np.linspace(0,1,11))
ax1.grid()
ax1.set_xlabel("Mass Recovery Fraction")
ax1.set_ylabel("Halo Fraction")
ax1.legend()

ax2.set_xscale('log')

plt.show()
