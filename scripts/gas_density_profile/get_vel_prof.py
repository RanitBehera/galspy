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
mass = GetPickle("scripts/gas_density_profile/cache/mass_gas_1.dat")
metallicity = GetPickle("scripts/gas_density_profile/cache/metallicity_gas_1.dat")

# Recenter
if True:
    CX,CY,CZ=131462.60496180426,15102.526179407781,91828.29217856088
    CVX,CVY,CVZ=-96.1464614868164,70.83936309814453,-52.537715911865234
    Center = np.column_stack((CX,CY,CZ))
    CenterVel = np.column_stack((CVX,CVY,CVZ))
    pos = pos-Center
    vel = vel-CenterVel

# Get unit vectors
uvecs = np.array([v / np.linalg.norm(v) for v in pos])

# Dot with vel
v_rad = np.array([np.dot(a, b) for a, b in zip(vel, uvecs)])

# get theta,phi
# unit vectors are normalized
_x,_y,_z=uvecs.T
theta = np.arccos(_z)
phi = np.arccos(_x/np.sqrt(1-(_z**2)))
r = np.array([np.linalg.norm(v) for v in pos])

mask1 = (100<r)&(r<300)
# mask2 = v_rad>100
mask=mask1#&mask2

theta=theta[mask]
phi=phi[mask]
v_rad=v_rad[mask]

# plt.plot(theta[mask],phi[mask],'.',ms=2,alpha=0.5)
plt.scatter(theta, phi, c=v_rad, cmap='viridis',s=2,alpha=0.1)
plt.axis("equal")
plt.colorbar()
plt.show()
