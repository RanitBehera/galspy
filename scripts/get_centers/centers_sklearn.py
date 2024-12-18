import galspy
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN, KMeans, AffinityPropagation
from sklearn.cluster import HDBSCAN
from sklearn.mixture import GaussianMixture
from sklearn.cluster import MeanShift, estimate_bandwidth
from galspy.utility.visualization import CubeVisualizer


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


# np.savetxt("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/get_centers/data/gid_wdef32.txt",cids,fmt="%d")


# print()
# proceed = ""
# while proceed.strip()=="":
#     proceed = input("Proceed?[y/n] : ")

# if proceed.lower() not in ['y']:


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
 
    points=star_pos
    # === K-Mean
    # Limitations : n_cluster, Randomness in centroid seed not in Kmean++
    # kmeans = KMeans(n_clusters=7)
    # kmeans.fit(points)
    # cluster_centers = kmeans.cluster_centers_
    # labels = kmeans.labels_

    # === Mean-Shift
    # Limitations : Too many cluster centers.
    # bandwidth = estimate_bandwidth(points, quantile=0.2, n_samples=len(points))
    bandwidth = 10
    ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
    ms.fit(points)
    cluster_centers = ms.cluster_centers_
    labels = ms.labels_


    # === DBSCAN
    # Limitations: No cluster centers. FoF Nature linkssucessful fillament.
    # dbscan = DBSCAN( min_samples=10)
    # labels = dbscan.fit_predict(points)
    # clustered_points = points[labels != -1]

    # cluster_centers= []
    # for label in labels[labels!=-1]:
    #     cpoints = points[labels == label]
    #     if len(cpoints)<100:continue
    #     ccenter = np.mean(cpoints, axis=0)
    #     cluster_centers.append(ccenter)
    # cluster_centers=np.array(cluster_centers)

    

    # === Gaussian Mixture
    # gmm=GaussianMixture(7)
    # gmm.fit(points)
    # labels = gmm.predict(points)
    # cluster_centers =  gmm.means_

    # === Affinity Propagation/OPTICS
    # Ridiculously slow
    # aff=AffinityPropagation(random_state=5).fit(points)
    # cluster_centers=aff.cluster_centers_
    # labels = aff.labels_

    # === 
    

    # print(labels)

    # VISUALISATION
    # fig1=plt.figure()
    # fig2 = plt.figure()
    # ax1=fig1.add_subplot(111, projection='3d') 
    # ax2=fig2.add_subplot(111, projection='3d') 

    # cv1=CubeVisualizer(ax1)
    # cv1.add_points(star_pos,1,'k',1)
    # cv1.add_points([hcm[cid-1]],300,'r',1,'+')

    # cv=CubeVisualizer(ax2)
    # cv.add_points(cluster_centers,300,'k',points_marker='+')
    # cv.add_points(points[labels ==0],1,'r')
    # cv.add_points(points[labels==1],1,'g')
    # cv.add_points(points[labels ==2],1,'b')
    # cv.add_points(points[labels ==3],1,'c')
    # cv.add_points(points[labels ==4],1,'y')
    # cv.add_points(points[labels ==5],1,'m')

    # cv1.show(False)
    # cv.show(False)

    # plt.show()    
    
    # Get labels and couts
    u,c = np.unique(labels,return_counts=True)
    # sort counts
    srt = np.argsort(c)[::-1]
    u,c = u[srt],c[srt]
    # lower limit
    mask = c>100
    u,c=u[mask],c[mask]

    cc = cluster_centers[u]

    for ui,ci in zip(u,c):
        print(ui,"-",ci)

    cv=CubeVisualizer()
    cv.add_points(cc,300,'k',points_marker='+')

    for ui in u:
        cv.add_points(points[labels==ui],points_alpha=1,points_size=10)
        cv.add_points(points[labels==ui],points_alpha=1,points_size=10)
        cv.add_points(points[labels==ui],points_alpha=1,points_size=10)

    cv.show()


print()
print("[ ANALYSING GROUPS ]")
lencids = len(cids)
for i,cid in enumerate(cids):
    if not cid==1:continue
    print(f"- GroupID : {cid} ({i+1}/{lencids})")
    FindPeaks(cid)



exit()



















