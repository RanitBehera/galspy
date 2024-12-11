import galspy
import numpy as np
import matplotlib.pyplot as plt

root = galspy.NavigationRoot("/mnt/home/student/cranit/NINJA/simulations/L150N2040/SNAPS/")

print("Reading positions ...")
star_pos = root.PART(43).Star.Position()
sx,sy,sz=star_pos.T


IMRES=150
BXRES=150000

ix=np.int32(IMRES*(sx/BXRES))
jy=np.int32(IMRES*(sy/BXRES))
kz=np.int32(IMRES*(sz/BXRES))

grid = np.ones((IMRES,IMRES,IMRES))
print("Mapping ...")
for i,j,k in zip(ix,jy,kz):
    grid[i,j,k] +=1


# ===== POST-PROCESS
def PostProcess(A):
    C=np.log10(A)
    C=C/np.max(C)
    C=1/(1+(np.exp(-1000*(C-0.7))))
    return C

grid=PostProcess(grid)

targets = np.where(grid>0.5)
indices_triplets = list(zip(targets[0]*(BXRES/IMRES), targets[1]*(BXRES/IMRES), targets[2]*(BXRES/IMRES)))
[print(t) for t in indices_triplets]




















