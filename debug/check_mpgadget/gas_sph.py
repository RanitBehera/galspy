import galspy
import matplotlib.pyplot as plt
from scipy import spatial
import numpy as np

root=galspy.NavigationRoot("/mnt/home/student/cranit/Data/MP_Gadget/Nishi/L10N64/output")

mass = root.PART(17).Gas.Mass()
ids = root.PART(17).Gas.ID()
dens = root.PART(17).Gas.Density()
pos = root.PART(17).Gas.Position()
sml = root.PART(17).Gas.SmoothingLength()
# root.PART(17).Gas.


# Create kd-Tree
print("Building kdTree ...",end=" ")
kdt = spatial.cKDTree(pos)
print("Done")


# Target a particle
tid = 10000
tpos = pos[tid]
tsml = sml[tid] 


# print data density
print("In data :",dens[tid])

# Calculate yourself
# quintic kernel
ngb_ids=kdt.query_ball_point(tpos,tsml)

print("Neighbour Length",len(ngb_ids))

ngb_mass = [mass[nid] for nid in ngb_ids]
ngb_pos = [pos[nid] for nid in ngb_ids]
ngb_dist = np.linalg.norm(ngb_pos - tpos,axis=1)





def wk_qs(q):
    if(q < 1.0):
        return pow(3 - q, 5) - 6 * pow(2 - q, 5) + 15 * pow(1 - q, 5)
    if(q < 2.0):
        return pow(3 - q, 5)- 6 * pow(2 - q, 5)
    if(q < 3.0):
        return pow(3 - q, 5)
    return 0.0

def dwk_qs(q):
    if(q < 1.0):
        return -5 * pow(3 - q, 4) + 30 * pow(2 - q, 4) - 75 * pow (1 - q, 4)
    if(q < 2.0):
        return -5 * pow(3 - q, 4) + 30 * pow(2 - q, 4)
    if(q < 3.0):
        return -5 * pow(3 - q, 4)
    return 0.0


def kernel(dist):
    return wk_qs(dist/tsml)


dens_cont=0
for i in range(len(ngb_dist)):
    d=ngb_dist[i]
    m=ngb_mass[i]
    W=kernel(d)
    dens_cont += W*m


print(dens_cont)

