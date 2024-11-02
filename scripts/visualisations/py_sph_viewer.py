# %%
import galspy
from sphviewer.tools import QuickView
import matplotlib.pyplot as plt
import numpy as np

# %%
print("Hi")
L150N2040 = "/mnt/home/student/cranit/NINJA/simulations/L150N2040/SNAPS"
root = galspy.NavigationRoot(L150N2040)
pos = root.PIG(43).Star.Position()/1000
gid = root.PIG(43).Star.GroupID()
mass = root.PIG(43).Star.Mass()
print("Hi")

# %%
print("Hi")
mask = (gid==1)
pos_m = pos[mask]
mass_m = mass[mask]
print("Hi")

print(np.mean(pos.T,axis=1))

# %%
qv = QuickView(pos_m, r=0.5, plot=False,
                # mass=mass,
                x=78.891,
                y=76.872,
                z=75.025
)
                # z=0,
            #    extent=10*np.array([-1,1,-1,1]))

img = qv.get_image()
extent = qv.get_extent()
fig = plt.figure(1, figsize=(12,12))
plt.imshow(img, extent=extent, cmap='grey')
plt.axis("equal")
plt.gca().set_facecolor('k')

plt.show()

# %%
