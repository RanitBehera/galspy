import galspy
import numpy as np
import matplotlib.pyplot as plt
from galspy.utility.visualization import CubeVisualizer
from scipy.signal import find_peaks
from scipy.spatial import KDTree
import itertools
from scipy.ndimage import gaussian_filter
from matplotlib.gridspec import GridSpec


def GetHitogramProfile(data,bins=1000,apply_log10=True):
    hist, bin_edges = np.histogram(data,bins=bins)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    if apply_log10:
        hist = np.log10(hist+1)
    sm_log_hist = gaussian_filter(hist, sigma=2)
    peaks_idx,_ = find_peaks(sm_log_hist,prominence=0.5)
    peaks = bin_centers[peaks_idx]
    return bin_centers,sm_log_hist,peaks


def FindProjectionPeaks(positions):
    x,y,z=positions.T
    tree = KDTree(positions)


    # ========================
    # 1. CANDIDATE PEAKS
    # ========================
    # Find peaks in 1D histograms of x,y,z

    binx,sm_logcountx,peaksx = GetHitogramProfile(x)
    biny,sm_logcounty,peaksy = GetHitogramProfile(y)
    binz,sm_logcountz,peaksz = GetHitogramProfile(z)

    candidates = list(itertools.product(peaksx,peaksy,peaksz))
    
    if True:
        fig = plt.figure(figsize=(12,8))
        gs = GridSpec(3,2,figure=fig)
        ax_px = fig.add_subplot(gs[0,0])
        ax_py = fig.add_subplot(gs[1,0])
        ax_pz = fig.add_subplot(gs[2,0])
        ax_3d = fig.add_subplot(gs[:,1],projection='3d')


        ax_px.plot(binx,sm_logcountx)
        ax_py.plot(biny,sm_logcounty)
        ax_pz.plot(binz,sm_logcountz) 

        for ax,peaks in zip([ax_px,ax_py,ax_pz],[peaksx,peaksy,peaksz]):
            for p in peaks:
                ax.axvline(p,color='k',lw=1)

        cv = CubeVisualizer(ax_3d)
        cv.add_points(positions,points_size=1,points_color='k')
        cv.add_points(candidates,points_size=50,points_color='r',points_marker='+')
        cv.show(False)
    
    
    # ===========================
    # 2. PEAK REJECTION TEST
    # ===========================
    
    # Loneliness check
    passed_level1 = []
    for c in candidates:
        dist,i = tree.query(c,k=10)
        if dist[0]>10:continue
        passed_level1.append(c)

    # Diffuseness check
    passed_level2 =[]
    for c in passed_level1:
        dist,i = tree.query(c,k=10)
        neighbours = positions[i]
        nx,xy,nz = neighbours.T
        dx,dy,dz = nx-c[0],xy-c[1],nz-c[2]

        # Spreads
        sx = np.std(dx)
        sy = np.std(dy)
        sz = np.std(dz)
        sr = np.std(dist)
        if sr>1:continue

        passed_level2.append(c)


    centers = passed_level2


    # ===========================
    # 3. OPTIMIZE CENTERS
    # ===========================

    # Meanshift Algorithm
    opt_centers = []
    for c in centers:
        centroid = c
        while True:
            _,idx = tree.query(centroid,k=100)
            ngbs = positions[idx]
            mean = np.mean(ngbs.T,axis=1)
            
            if np.linalg.norm(mean-centroid)>1e-3:
                centroid = mean
            else:
                opt_centers.append(centroid)
                break


    # ============================
    # 4. BOUNDARY FINDING
    # ============================
    cntr_bnd = []
    



    plt.show()


















# ============================================================================


print("="*60)
print("PEAK FINDER".center(60))
print("-"*60)

SNAPSPATH = "/mnt/home/student/cranit/NINJA/simulations/L150N2040/SNAPS/"
SNAPNUM=43
MASSUNIT=1e10

# Cluster Definition.
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



# print()
# proceed = ""
# while proceed.strip()=="":
#     proceed = input("Proceed?[y/n] : ")

# if proceed.lower() not in ['y']:
#     exit()


print()
print("[ READING PIG ]")
print("- STAR Positions : ",end="",flush=True)
spos = PIG.Star.Position()
smass = PIG.Star.Mass()
print("Done")
print("- STAR GroupIDs : ",end="",flush=True)
sgid = PIG.Star.GroupID()
print("Done")
print("- FOF Halo Center Mass : ",end="",flush=True)
hcm = PIG.FOFGroups.MassCenterPosition()
print("Done")




print()
print("[ ANALYSING GROUPS ]")
lencids = len(cids)



for i,cid in enumerate(cids):
    if not cid==1:continue
    # if cid>20:break

    # if cid not in okay:continue

    print(f"- GroupID : {cid} ({i+1}/{lencids})")
    # try:
    FindProjectionPeaks(spos[sgid==cid])
    # except:
    #     # pass
    #     fp.write(f"#{cid}\n")
    #     continue
