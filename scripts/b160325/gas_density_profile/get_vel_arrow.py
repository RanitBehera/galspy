import numpy as np
import pickle
import matplotlib.pyplot as plt
import time

def GetPickle(filepath):
    with open(filepath,"rb") as fp:
        data = pickle.load(fp)
    return data

pos = GetPickle("scripts/gas_density_profile/cache/pos_gas_1.dat")
vel = GetPickle("scripts/gas_density_profile/cache/vel_gas_1.dat")
# mass = GetPickle("scripts/gas_density_profile/cache/mass_gas_1.dat")
# metallicity = GetPickle("scripts/gas_density_profile/cache/metallicity_gas_1.dat")


# Recenter
if True:
    CX,CY,CZ=131462.60496180426,15102.526179407781,91828.29217856088
    CVX,CVY,CVZ=-96.1464614868164,70.83936309814453,-52.537715911865234
    Center = np.column_stack((CX,CY,CZ))
    CenterVel = np.column_stack((CVX,CVY,CVZ))
    pos = pos-Center
    vel = vel-CenterVel



# mask = (np.random.random(len(pos))>0.99)
# pos=pos[mask]
# vel=vel[mask]



from galspy.utility.visualization import CubeVisualizer
cv=CubeVisualizer()



# radial vel
uvecs = np.array([v / np.linalg.norm(v) for v in pos])
uvels = np.array([v / np.linalg.norm(v) for v in vel])
v_rad = np.array([np.dot(a, b) for a, b in zip(vel, uvecs)])
v_theta = np.array([np.dot(a, b) for a, b in zip(uvels, uvecs)])

mask = (v_theta>0.9)&(v_rad>0)
pos=pos[mask]
vel=vel[mask]


print(len(pos))

cv.add_points(pos,points_alpha=0)
vel=np.array([v/np.linalg.norm(v) for v in vel])
vel*=1
for v,p in zip(vel,pos):
    cv.add_arrow(p+v,p)

cv.show()
