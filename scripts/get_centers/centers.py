import galspy
import numpy as np
import matplotlib.pyplot as plt
from galspy.utility.visualization import CubeVisualizer

# a=np.array([43129,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43129,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43129,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43129,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130,43130])
# b=a.sum()
# print(b)


print("="*60)
print("PEAK FINDER".center(60))
print("-"*60)

SNAPSPATH = "/mnt/home/student/cranit/NINJA/simulations/L150N2040/SNAPS/"
SNAPNUM=43
MASSUNIT=1e10

# Cluster Defibition.
# Number of stars a halo should have to further post process.
# Linked to minimum stellar mass in the cluster.
CLDEF = 32     


# =========
root = galspy.NavigationRoot(SNAPSPATH)
print("[ TARGET BOX ]")
print(f"- Path:{SNAPSPATH}")
print(f"- Snapshot Number:{SNAPNUM}")
a=root.PART(SNAPNUM).Header.Time()
z=(1/a)-1
print(f"- Redshift:{z:.02}")

# print()
# print("[ READING PART ]")
# print("- Star Positions : ",end="")
# part_star_pos = root.PART(SNAPNUM).Star.Position()
# print("Done")

PIG=root.PIG(SNAPNUM)

print()
print("[ READING PIG ]")
print("- FOF GroupIDs : ",end="",flush=True)
gids = PIG.FOFGroups.GroupID()
print("Done")
print(f"  * Found {len(gids)} Groups.")

print("- FOF Group Stellar Mass : ",end="",flush=True)
gsm = PIG.FOFGroups.MassByType().T[4]*MASSUNIT
argmax_gsm= np.argmax(gsm)
max_gsm_gid,max_gsm = gids[argmax_gsm],gsm[argmax_gsm] 
single_star_mass = PIG.Header.MassTable()[4]*MASSUNIT
min_clmass = CLDEF*single_star_mass
cl_mask = gsm>min_clmass
cids    = gids[cl_mask]  # Cluster ids
csm     = gsm[cl_mask]
print("Done")
print(f"  * Mass of single star particle {single_star_mass:.02} M_solar/h.")
print(f"  * Maximum group stellar mass in GroupID {max_gsm_gid} with {max_gsm:.02} M_solar/h corresponding to {round(max_gsm/single_star_mass)} star count in group.")
print(f"  * Found {len(cids)} groups with cluster definition of {CLDEF} star particles corresponding to minimum cluster stellar mass of {min_clmass:.02} M_solar/h.")

print()
proceed = ""
while proceed.strip()=="":
    proceed = input("Proceed?[y/n] : ")

if proceed.lower() not in ['y']:
    exit()


print()
print("[ READING PIG ]")
print("- STAR Positions : ",end="",flush=True)
spos = PIG.Star.Position()
print("Done")
print("- STAR GroupIDs : ",end="",flush=True)
sgid = PIG.Star.GroupID()
print("Done")
print("- FOF Halo Center Mass : ",end="",flush=True)
hcm = PIG.FOFGroups.MassCenterPosition()
print("Done")




def FindPeaks(cid):
    print("  * Filtering for stars in group.")
    star_pos = spos[sgid==cid] 
    x,y,z=star_pos.T
    print(f"  * Found {len(star_pos)} stars.")
    print(f"  * Creating bounding box.")
    # origin
    ox,oy,oz = np.min(x),np.min(y),np.min(z)
    x,y,z=x-ox,y-oy,z-oz
    sx,sy,sz = np.max(x),np.max(y),np.max(z)
    span_kpc = max([sx,sy,sz])+1e-10
    # Added small length so that the end boundary particle will fall inside the range when mapped.
    # Otherwise it will get grid index 100 in  grid of size 100 where idnex should range from 0-99.
    print(f"  * Spanned over {span_kpc:.02f} kpc/h.")
    
    gr = 100
    print(f"  * Creating grid of dimension {gr}x{gr}x{gr}.")
    grid = np.ones((gr,gr,gr))
    # 8MB for 100x100x100
    # np.ones() instead of np.zeros() so that when log scaled,
    # zero count cells will become zero instead of -inf.

    print(f"  * Mapping coordinates to grid indices.")
    ix=np.int32(gr*(x/span_kpc))
    jy=np.int32(gr*(y/span_kpc))
    kz=np.int32(gr*(z/span_kpc))

    print("  * Filling grids.")
    # for i,j,k in zip(ix,jy,kz):
        # grid[i,j,k] +=1  
    # grid[ix,jy,kz]+=1
    # Above numpy method is a simultaneous operation.
    # Can't handle filling when cell indices are repeated.
    # For this the following method works and gives same result as bruteforce loop above.
    np.add.at(grid, (ix, jy, kz), 1)
    print(f"  * Maximum cell count {int(np.max(grid))}.")

    
    print("  * Post-processing cells for log scale.")
    grid = np.log10(grid)

    print("  * Normalising cells.")
    grid /= np.max(grid)


    clim=0.8 
    sharpness=1000
    print(f"  * Increasing contrast centered at {clim} with sharpness {sharpness}.")
    u=sharpness*(grid-clim)
    # grid=1/(1+(np.exp(-u))) # This version gives overflow erros. The folloing version doesn't being the same function.
    # grid=np.exp(np.min(u,0))/(1+(np.exp(-np.abs(u))))


    print("  * Finding peaks.")
    peaks = np.array(np.where(grid>0.9)).T

    print(f"  * Found {len(peaks)} peaks.")

    print("  * Remapping peak cells grid indices to bouding box coordinates.")
    peak_cell_pos   = peaks*(span_kpc/gr)

    print("  * Shifting bounding box to its global location.")
    pcpx,pcpy,pcpz=peak_cell_pos.T
    pcpx,pcpy,pcpz=pcpx+ox,pcpy+oy,pcpz+oz
    peak_pos = np.column_stack((pcpx,pcpy,pcpz))

    [print(t) for t in peak_pos]
    print()
    print(hcm[cid-1])





print()
print("[ ANALYSING GROUPS ]")
lencids = len(cids)
for i,cid in enumerate(cids):
    if not cid==2:continue
    print(f"- GroupID : {cid} ({i+1}/{lencids})")
    FindPeaks(cid)



exit()

# Visualise particles
# gid=4
# cv=CubeVisualizer()
# cv.add_points(star_pos_fof[star_gid_fof==gid],1,'r')
# cv.add_points([halo_cm[gid-1]],100,'k')
# cv.show()

















