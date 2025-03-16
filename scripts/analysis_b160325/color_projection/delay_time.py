#%%
import galspy as gs
import matplotlib.pyplot as plt
import numpy as np

root=gs.NavigationRoot(gs.NINJA.L150N2040)

gid = root.PIG(43).Gas.GroupID()
dt=root.PIG(43).Gas.DelayTime()

#%%
frac_all=np.zeros(6000)

for i in range(6000):
    print(i)
    tgid=i+1
    mask = gid==tgid
    dt_t= dt[mask]
    dt_t_nz = dt_t[~(dt_t==0)]
    frac = len(dt_t_nz)/len(dt_t)
    frac_all[i]=frac


#%%
M=root.PIG(43).FOFGroups.MassByType().T[0]
plt.plot(M[:6000]*(10**10),frac_all,'.')
plt.xscale("log")
plt.xlabel("FOF Mass ($M_\odot$)")
plt.ylabel("Fraction of gas particle in winds")
plt.show()



#%%

# dt = dt*3.08568e16 / (3600*24*365*1e6)

# plt.hist(dt,bins=100)
# plt.yscale("log")
# plt.show()
# %%
