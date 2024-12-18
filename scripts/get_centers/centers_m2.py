import galspy
import numpy as np
import matplotlib.pyplot as plt
from galspy.utility.visualization import CubeVisualizer
from scipy.signal import find_peaks
from scipy.spatial import KDTree
import itertools


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
print("Done")
print("- STAR GroupIDs : ",end="",flush=True)
sgid = PIG.Star.GroupID()
print("Done")
print("- FOF Halo Center Mass : ",end="",flush=True)
hcm = PIG.FOFGroups.MassCenterPosition()
print("Done")


# Check DM profile
# dmpos = PIG.DarkMatter.Position()
# dmgid = PIG.DarkMatter.GroupID()



from scipy.ndimage import gaussian_filter
def HistProfile(signal,bins=1000):
    count,edge=np.histogram(signal,bins=bins)
    bin=0.5*(edge[:-1]+edge[1:])
    logcount=np.log10(count+1)
    # Gaussian Smooth
    sm_logcount= gaussian_filter(logcount, sigma=2)
    # Peaks
    peak_indices,_ = find_peaks(sm_logcount,prominence=0.5,)#,height=np.log10(10))
    peaks = bin[peak_indices]

    return bin,sm_logcount,peaks

def FindPeaks(cid):
    star_pos = spos[sgid==cid] 
    x,y,z=star_pos.T
    hcm = PIG.FOFGroups.MassCenterPosition()[cid-1]
    hcmx,hcmy,hcmz = hcm


    # fig,axs = plt.subplots(3,1)
    # axs:list[plt.Axes]

    bin,sm_logcount,peaksx = HistProfile(x)
    # axs[0].plot(bin,sm_logcount)
    # axs[0].axvline(hcmx,color='k',ls='--',lw=1)
    # for p in peaksx:
    #     axs[0].axvline(p,color='k',lw=1)

    bin,sm_logcount,peaksy = HistProfile(y)
    # axs[1].plot(bin,sm_logcount)
    # axs[1].axvline(hcmy,color='k',ls='--',lw=1)
    # for p in peaksy:
    #     axs[1].axvline(p,color='k',lw=1)

    bin,sm_logcount,peaksz = HistProfile(z)
    # axs[2].plot(bin,sm_logcount)
    # axs[2].axvline(hcmz,color='k',ls='--',lw=1)
    # for p in peaksz:
    #     axs[2].axvline(p,color='k',lw=1)

    plt.show()

    # return
    # DM Check 
    # dm_pos = dmpos[dmgid==cid]
    # x,y,z=dm_pos.T

    # bin,sm_logcount,peaksx = HistProfile(x)
    # axs[0].plot(bin,sm_logcount)

    # bin,sm_logcount,peaksy = HistProfile(y)
    # axs[1].plot(bin,sm_logcount)

    # bin,sm_logcount,peaksy = HistProfile(z)
    # axs[2].plot(bin,sm_logcount)


    
    # return
    
    candidates = list(itertools.product(peaksx,peaksy,peaksz))
    n_clusters = np.max([len(peaksx),len(peaksy),len(peaksz)])
    # Tried : Directly feeding to k-mean. farthest lone wonderer gets priority


    # KdTree
    tree = KDTree(star_pos)

    # Rejection 1 : Neareast star particle should be within 10kpc.
    # Rejection 2 : Nearest 10 star particle shpuld have small spread.
    candidates1 = []
    for cand in candidates:
        distance,_ = tree.query(cand,k=10)
        if distance[0]>10:continue
        spread = np.std(distance)
        if spread>1:continue
        candidates1.append(cand)

    
    # Optimize Centers
    centers = []
    for cand in candidates1:
        centroid = cand
        while True:
            _,index = tree.query(centroid,k=100)
            neighbours = star_pos[index]
            mean = np.mean(neighbours.T,axis=1)
            
            if np.linalg.norm(mean-centroid)>0.01:
                centroid = mean
            else:
                centroid = mean
                centers.append(centroid)
                break

    # Radius Determination
    # fig,axs = plt.subplots(len(centers),1)
    # axs:list[plt.Axes]
    cntr_rad=[]
    for i,cntr in enumerate(centers):
        distance,_ = tree.query(cntr,k=len(star_pos))
        count,edge=np.histogram(distance,bins=1000)
        logcount=np.log10(1+count)
        sm_logcount= gaussian_filter(logcount, sigma=5)

        bin=0.5*(edge[:-1]+edge[1:])
        # axs[i].plot(bin,sm_logcount)

        trigers=np.sign(np.gradient(sm_logcount))
        # axs[i].plot(bin[:-1],trigers)
        trigers=np.diff(trigers)
        # axs[i].plot(bin[:-1],trigers)
        rad = bin[np.where(trigers>0)][0]
        # axs[i].axvline(rad)
        cntr_rad.append([cntr,rad])


    # Sphere coliision detection and shrink
    for a,(anchor,arad) in enumerate(cntr_rad):
        for t,(target,trad) in enumerate(cntr_rad):
            if a>=t:continue
            ctr_dist = np.linalg.norm(target-anchor)
            rad_sum   = arad + trad
            if rad_sum<ctr_dist:continue
            
            ratio =rad_sum/ctr_dist
            cntr_rad[a]=[anchor,arad/ratio]
            cntr_rad[t]=[target,trad/ratio]



    cv=CubeVisualizer()
    cv.add_points(star_pos,points_alpha=1,points_color='r')
    cv.add_points([hcm],points_color='k',points_size=2000,points_marker='+')
    # cv.add_points(candidates,points_color='b',points_size=300,points_marker='+')
    # cv.add_points(candidates1,points_color='b',points_size=300,points_marker='+')
    cv.add_points(centers,points_color='b',points_size=2000,points_marker='+')
    for cntr,rad in cntr_rad:
        cv.add_sphere_wire(cntr,rad,"b")
    
    ax=cv.show(False)
    ax.set_title(f"GID {cid} : N={len(centers)}")
    plt.show()





print()
print("[ ANALYSING GROUPS ]")
lencids = len(cids)
for i,cid in enumerate(cids):
    if not cid==1:continue
    # if cid>20:break
    print(f"- GroupID : {cid} ({i+1}/{lencids})")
    FindPeaks(cid)










