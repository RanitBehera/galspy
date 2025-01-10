import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import galspy, os
from galspy.utility.visualization import CubeVisualizer
import itertools
from scipy.spatial import KDTree
from scipy.ndimage import gaussian_filter
from scipy.signal import find_peaks
from scipy.signal import butter, filtfilt




def GetHitogramProfilePeaks(data,bins=250,apply_log10=True):
    hist, bin_edges = np.histogram(data,bins=bins)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    # Treat as signal
    signal = hist
    
    # Detection limit
    # signal = np.where(signal>1,signal,0)

    if apply_log10:
        signal = np.log10(signal+1)

 
    signal = gaussian_filter(signal, sigma=2)
    peaks_idx,_ = find_peaks(signal,prominence=0.3)
    peaks = bin_centers[peaks_idx]

    # Pin at two ends
    signal[[0,-1]]=[0,0]
    return bin_centers,signal,peaks


def FindProjectionPeaks(positions,mass,uselog=True,reclevel=0,**kwargs):
    print("  Recursion Level",reclevel)
    x,y,z=positions.T
    tree = KDTree(positions)


    # =========================
    # 1. FIND PEAKS CANDIDATES
    # =========================
    # Adaptipe binning
    spanx,spany,spanz=np.ptp(x),np.ptp(y),np.ptp(z)
    BIN_SIZE= 0.165*(1+7)/(0.6736)#ckpc
    nbinx,nbiny,nbinz=int(spanx/BIN_SIZE),int(spany/BIN_SIZE),int(spanz/BIN_SIZE)

    binx,countx,peaksx = GetHitogramProfilePeaks(x,nbinx,apply_log10=uselog)
    biny,county,peaksy = GetHitogramProfilePeaks(y,nbiny,apply_log10=uselog)
    binz,countz,peaksz = GetHitogramProfilePeaks(z,nbinz,apply_log10=uselog)

    
    # x,y,z=kwargs["dmpos"].T
    # binx_dm,countx_dm,peaksx_dm = GetHitogramProfilePeaks(x,apply_log10=uselog)
    # biny_dm,county_dm,peaksy_dm = GetHitogramProfilePeaks(y,apply_log10=uselog)
    # binz_dm,countz_dm,peaksz_dm = GetHitogramProfilePeaks(z,apply_log10=uselog)


    candidates = list(itertools.product(peaksx,peaksy,peaksz))


    if True and (not DUMP):
        fig = plt.figure(figsize=(12,8))
        gs = GridSpec(3,2,figure=fig)
        ax_px = fig.add_subplot(gs[0,0])
        ax_py = fig.add_subplot(gs[1,0])
        ax_pz = fig.add_subplot(gs[2,0])
        ax_3d = fig.add_subplot(gs[:,1],projection='3d')


        ax_px.plot(binx,countx)
        ax_py.plot(biny,county)
        ax_pz.plot(binz,countz) 

        # ax_px.plot(binx_dm,countx_dm)
        # ax_py.plot(biny_dm,county_dm)
        # ax_pz.plot(binz_dm,countz_dm) 

        for ax,peaks in zip([ax_px,ax_py,ax_pz],[peaksx,peaksy,peaksz]):
            for p in peaks:
                ax.axvline(p,color='k',lw=1)

        cv = CubeVisualizer(ax_3d)
        cv.add_points(positions,points_size=1,points_color='r')
        cv.add_points(candidates,points_size=50,points_color='b',points_marker='+')
        cv.show(False)
    
    
    # ===========================
    # 2. PEAK REJECTION TEST
    # ===========================
    
    # Loneliness check
    passed_level1 = []
    for c in candidates:
        dist,i = tree.query(c,k=10)
        # print(dist)
        if dist[0]>30:continue
        passed_level1.append(c)

    # Diffuseness check
    passed_level2 =[]
    # for c in passed_level1:
    #     dist,i = tree.query(c,k=10)
    #     neighbours = positions[i]
    #     nx,ny,nz = neighbours.T
    #     dx,dy,dz = nx-c[0],ny-c[1],nz-c[2]
    #     # dx,dy,dz = np.abs(dx),np.abs(dy),np.abs(dz)
    #     # print(np.unique(np.sign(dx)))

    #     # Spreads
    #     sx = np.std(dx)
    #     sy = np.std(dy)
    #     sz = np.std(dz)
    #     sr = np.std(dist)
    #     # print(sr)
    #     if sr>1:continue
    #     passed_level2.append(c)

    for c in passed_level1:
        ind = tree.query_ball_point(c,10)
        bnd_mass = np.sum(mass[ind])
        bnd_mass*=1e10
        if bnd_mass<35*(1.4e6):continue
        
        passed_level2.append(c)

    centers = passed_level2
    if len(centers)==0:centers=passed_level1
    
    centers=np.array(centers)

    # ===========================
    # 3. OPTIMIZE CENTERS
    # ===========================
    # Meanshift Algorithm
    opt_centers = []
    for i,c in enumerate(centers):
        centroid = c
        while True:
            _,idx = tree.query(centroid,k=min(len(positions),128))
            ngbs = positions[idx]
            
            # Local neighbours so that far away neighbourhood don't drag the mean
            ngb_dist = np.linalg.norm(ngbs-centroid,axis=1)  
            local_mask = ngb_dist<10
            local_ngbs = ngbs[local_mask]
            ngbs=local_ngbs

            if len(ngbs)==0:
                mean = centroid
            else:
                mean = np.mean(ngbs.T,axis=1)
            
            if np.linalg.norm(mean-centroid)>1e-3:
                centroid = mean
            else:
                opt_centers.append(centroid)
                break
    
    # opt_centers=np.array(opt_centers)

    # Merge nearby centers
    for a,anchor in enumerate(opt_centers):
        for t,target in enumerate(opt_centers):
            if a>=t:continue
            if np.linalg.norm(target-anchor)<=5:
                opt_centers.pop(t)

    # opt_centers=np.array(centers)

    

    # ============================
    # 4. BOUNDARY FINDING
    # ============================
    _PLOT=True
    if _PLOT:
        fig,axs= plt.subplots(len(opt_centers),1)
        if len(opt_centers)==1:axs=[axs]
        axs:list[plt.Axes]

    cntr_rad = []
    for i,cntr in enumerate(opt_centers):
        dist,idx = tree.query(cntr,len(positions))
        count,bin_edges = np.histogram(dist,bins=1000)
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
        
        logcount = np.log10(1+count)
        dist_logcount = gaussian_filter(logcount,sigma=5)
        if _PLOT: axs[i].plot(bin_centers,dist_logcount)

        slope_sign = np.sign(np.gradient(dist_logcount))
        if _PLOT: axs[i].plot(bin_centers,slope_sign,alpha=0.2)

        triggers = np.diff(slope_sign)
        if _PLOT: axs[i].plot(bin_centers[:-1],triggers,alpha=0.2)

        boundary = bin_centers[np.where(triggers>0)][0]
        if _PLOT: axs[i].axvline(boundary)

        cntr_rad.append([cntr,boundary])


    # ===============================
    # 4. COLLIDING BOUNDARY SHRINK
    # ===============================
    if True:
        for a,(anchor,arad) in enumerate(cntr_rad):
            for t,(target,trad) in enumerate(cntr_rad):
                if a>=t:continue
                ctr_dist = np.linalg.norm(target-anchor)
                rad_sum   = arad + trad
                if rad_sum<ctr_dist:continue
                
                ratio =rad_sum/ctr_dist
                cntr_rad[a]=[anchor,arad/ratio]
                cntr_rad[t]=[target,trad/ratio]


    # =================================
    # 5. MASS CALCULATION
    # =================================
    sub_count = []
    sub_mass = []
    accounted_ind = []
    for i,(anchor,arad) in enumerate(cntr_rad):
        bound_part_ind = tree.query_ball_point(anchor,arad)
        bound_part_mass = np.sum(mass[bound_part_ind])
        sub_mass.append(bound_part_mass)
        sub_count.append(len(mass[bound_part_ind]))
        accounted_ind.extend(bound_part_ind)






    table=[]
    for (cntr,rad),bmass,bcount in zip(cntr_rad,sub_mass,sub_count):
        table.append([*cntr,rad,bmass,bcount])
    table=np.array(table)


    # =================================
    # 6. RECURSION
    # =================================

    mask = np.zeros(len(positions),dtype=bool)
    mask[accounted_ind]=True
    upos = positions[~mask]
    umass = mass[~mask]

    MAX_REC_LEVEL= 0
    if reclevel<MAX_REC_LEVEL:
        plt.show()
        table2=FindProjectionPeaks(upos,umass,True,reclevel+1)
        table = np.vstack([table,table2])

    
    
    if DUMP:
        fp.write(f"#{cid}"+"\n")
        try:
            # gid nsubs subid nstar_group nstar_sub st_mass_sum st_mass_sub gid_rec_count gid_rec_count_frac gid_rec_mass gid_rec_mass_frac cx cy cz cr 
            outrow=[]
            pig_st_mass_sum = np.sum(mass)
            for i,row in enumerate(table):
                cx,cy,cz,cr,bmass,bcount=row
                outrow.append(np.array([cid,
                                        len(table),i,
                                        len(mass),bcount,pig_st_mass_sum,bmass,
                                        np.sum(table.T[-1]),np.sum(table.T[-1])/len(mass),
                                        np.sum(table.T[-2]),np.sum(table.T[-2])/pig_st_mass_sum,
                                        cx,cy,cz,cr
                                        ]))


            # np.savetxt(fp, np.array(table), fmt='%d %d %d %d %d %.08f %.8f %.8f %.8f %.8f %.8f %.8f')
            
            np.savetxt(fp, outrow, fmt='%d %d %d %d %d %0.08f %0.08f %d %0.04f %0.08f %0.04f %0.08f %0.08f %0.08f %0.08f')
        except:
            fp.write(f"#{cid} -1 -1 {len(mass)} -1 {np.sum(mass):.04f}\n")

        fp.flush()
    
    
    rec_mass_frac = np.sum(table.T[-2])/np.sum(mass)

    return table,rec_mass_frac    













# ============================================================================

#region
print("="*60)
print("PEAK FINDER".center(60))
print("-"*60)

SNAPSPATH = "/mnt/home/student/cranit/NINJA/simulations/L150N2040/SNAPS/"
SNAPNUM=43
MASSUNIT=1e10

# Cluster Definition.
# Number of stars a halo should have to further post process.
# Linked to minimum stellar mass in the cluster.
CLDEF = 700     

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


# print("- FOF DM : ",end="",flush=True)
# Dark Matter
# dmgid=PIG.DarkMatter.GroupID()
# dmmass=PIG.DarkMatter.Mass()
# dmpos=PIG.DarkMatter.Position()
print("Done")





print()
print("[ ANALYSING GROUPS ]")
lencids = len(cids)


#endregion

DUMP=False
FILENAME="clusterinfo700_010125_1.txt"
if DUMP:
    fp = open(f"/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/get_centers/data/{FILENAME}",'w')
    fp.write("#gid nsubs subid nstar_group nstar_sub st_mass_sum st_mass_sub gid_rec_count gid_rec_count_frac gid_rec_mass gid_rec_mass_frac cx cy cz cr\n")
    fp.close()
    
    fp = open(f"/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/get_centers/data/{FILENAME}",'a')




for i,cid in enumerate(cids):


    # if cid<168:continue
    
    if not cid==10:continue
    # if cid not in [78, 127, 165, 330]:continue
    # if cid>100: continue
    # if cid<2000 or cid>2020: continue

    # if cid not in okay:continue

    # ================
    print(f"- GroupID : {cid} ({i+1}/{lencids})",'-'*20)
    # Star
    cpos = spos[sgid==cid]
    cmass = smass[sgid==cid]
    # print(cpos)
    # print("  Star :",np.sum(cmass)*100)
    x,y,z=cpos.T
    print("x:",np.ptp(x),"\ny:",np.ptp(y),"\nz:",np.ptp(z))

    # DM
    # cposdm = dmpos[dmgid==cid]
    # cmassdm = dmmass[dmgid==cid]
    # print("DM :",np.sum(cmassdm))

    table,rmf=FindProjectionPeaks(cpos,cmass)#,dmpos=cposdm)


    if True and (not DUMP):
        fig = plt.figure()
        cv = CubeVisualizer()
        cv.add_points(cpos,points_alpha=0.5,points_color='r')
        

        for i,(cx,cy,cz,r,m,count) in enumerate(table):
            cntr=np.array([cx,cy,cz])
            cv.add_points([cntr],points_color='k',points_size=1000,points_marker='+')
            cv.add_sphere_wire(cntr,r,'b')
            # cv.add_text(cntr,str(int(i)))


        ax=cv.show(False)
        ax.set_title(f"GID={cid} : N={len(table)} : RF={rmf*100:.2f}%")
        # print(table)

        plt.show()


if DUMP:
    fp.close()





# 
# 49,50,57,61,73,82,83, 93,111, 112, 129
# 101,105, 122, 156
# 168, 185, 188, 191, 276, 290, 297, 337
# 322,357


# Radius
# 107, 158, 177, 195, 242
# 244, 262, 280, 292, 316

# Mean Shift - Fixed
# 78, 127, 165, 330

# Closeby Rejection - Fixed with 5ckpc look region
# 155

# ellipsoid
# 134, 142, 278


# Center rejection issue
# 295



# ??
# 322, 357