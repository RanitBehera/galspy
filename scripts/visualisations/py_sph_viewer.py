#%%
import galspy
from sphviewer.tools import QuickView
import matplotlib.pyplot as plt
import numpy as np

print("Hi")
L150N2040 = "/mnt/home/student/cranit/NINJA/simulations/L150N2040/SNAPS"
root = galspy.NavigationRoot(L150N2040)
parti = root.PIG(63).Gas
pos = parti.Position()/1000
gid = parti.GroupID()
mass = parti.Mass()
print("Hi")

#%%

print("Hi")
mask = (gid==11)
pos_m = pos[mask]
mass_m = mass[mask]
print("Hi")

minp= np.min(pos_m.T,axis=1)
maxp= np.max(pos_m.T,axis=1)
minmax = 0.5*(minp+maxp)


def sigmoid(x,x0=0,sig=1):
    return 1/(np.exp(-sig*(x-x0))+1)


#%%
qv = QuickView(pos_m, r="infinity", plot=False,
                # mass=mass,
                x=minmax[0]-0.3,
                y=minmax[1]+0.2,
                z=minmax[2],
                t=0,
                extent=list(0.5*np.array([-1,1,-1,1])))

img = qv.get_image()
extent = qv.get_extent()
fig = plt.figure(1, figsize=(12,12))

# imgn=img/np.max(img)
# imgn=sigmoid(imgn,0.9,20)
# print(imgn)

plt.imshow(img**5, extent=extent, cmap='grey')
plt.axis("equal")
plt.gca().set_facecolor('k')
plt.axis("off")
plt.tight_layout()
plt.show()



# %%
