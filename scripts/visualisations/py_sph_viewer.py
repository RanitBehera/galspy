import galspy
from sphviewer.tools import QuickView
import matplotlib.pyplot as plt

print("Hi")
L150N2040 = "/mnt/home/student/cranit/NINJA/simulations/L150N2040/SNAPS"

root = galspy.NavigationRoot(L150N2040)

dm_pos = root.PIG(63).Gas.Position()
dm_gid = root.PIG(63).Gas.GroupID()
mask = (dm_gid==1)
dm_pos = dm_pos[mask]

print("Hi")

qv = QuickView(dm_pos, r='infinity', plot=False)
            #    x=-0.100,y=-0.100,z=0)
                # z=0,x=0)
            #    extent=[-200,200,-200,200])
img = qv.get_image()
extent = qv.get_extent()
fig = plt.figure(1, figsize=(7,7))
plt.imshow(img, extent=extent, cmap='grey')

plt.show()