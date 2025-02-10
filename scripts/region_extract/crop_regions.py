import galspy
import numpy as np
import matplotlib.pyplot as plt
import os
import pickle
from multiprocessing import Pool

L50N1008 = "/mnt/home/student/cranit/Data/MP_Gadget/Nishi/L50N1008z05"
SNAP_NUM = 174
SAVEDIR = "/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/region_extract/data_kanish"

root = galspy.NavigationRoot(L50N1008)
PART = root.PART(SNAP_NUM)
PIG = root.PIG(SNAP_NUM)
# PTYPE=0     # Only 0,4,5 supported
SPAN = 505  # kpc - center to edge

def GetSelectedGIDs():
    st_mass = root.PIG(SNAP_NUM).FOFGroups.MassByType().T[4]
    gid     = root.PIG(SNAP_NUM).FOFGroups.GroupID()

    mask = np.argsort(st_mass)
    st_mass = st_mass[mask]
    gid = gid[mask]

    select_mask = (st_mass>=0.5) & (st_mass<=5)

    return gid[select_mask]

    # plt.plot(gid[select_mask],st_mass[select_mask],'.g',ms=2)
    # plt.plot(gid[~select_mask],st_mass[~select_mask],'.k',ms=1)
    # plt.xscale("log")
    # plt.yscale("log")
    # plt.axhspan(0.1,10,color='k',alpha=0.1,ec=None)
    # plt.show()

def Check_Blob_Intersection(arg):
    blobname,bounds = arg

    if PTYPE==0:
        X,Y,Z = PART.Gas.Position([blobname]).T
    elif PTYPE==4:
        X,Y,Z = PART.Star.Position([blobname]).T
    elif PTYPE==5:
        X,Y,Z = PART.BlackHole.Position([blobname]).T
    else:
        return False


    minX,maxX = np.min(X),np.max(X)
    minY,maxY = np.min(Y),np.max(Y)
    minZ,maxZ = np.min(Z),np.max(Z)
    
    # Overlaps
    bxn,bxp,byn,byp,bzn,bzp=bounds
    ovlX = (maxX>=bxn) and (minX<=bxp)
    ovlY = (maxY>=byn) and (minY<=byp)
    ovlZ = (maxZ>=bzn) and (minZ<=bzp)
    
    intersecting = ovlX and ovlY and ovlZ
    return intersecting

def Get_Intersecting_Blobs(gid):
    center_kpc = PIG.FOFGroups.MassCenterPosition()[gid-1]
    span_kpc   = SPAN*np.ones(3)

    bxn,bxp=center_kpc[0]-span_kpc[0],center_kpc[0]+span_kpc[0]
    byn,byp=center_kpc[1]-span_kpc[1],center_kpc[1]+span_kpc[1]
    bzn,bzp=center_kpc[2]-span_kpc[2],center_kpc[2]+span_kpc[2]
    bounds = [bxn,bxp,byn,byp,bzn,bzp]

    blobnames = sorted(os.listdir(root.PART(SNAP_NUM).DarkMatter.GroupID.path))
    blobnames.remove("attr-v2")
    blobnames.remove("header")

    # -----
    args = [(bn,bounds) for bn in blobnames]
    with Pool(20) as pool:
        mask = pool.map(Check_Blob_Intersection,args)
    iblobs=list(np.array(blobnames,dtype=str)[mask])

    return iblobs


def Crop_And_Save_Fields(iblobs,OUTDIR:str):
    CX,CY,CZ        = PIG.FOFGroups.MassCenterPosition()[gid-1]       #1 for gid
    CVX,CVY,CVZ     = PIG.FOFGroups.MassCenterVelocity()[gid-1]
    BLOBS = iblobs
    with open(OUTDIR+os.sep+f"header.txt","w") as fp:
        fp.write(f"GID:{gid}\n")
        fp.write("\nPART HEADER"+'-'*32+"\n")
        fp.write("\n".join([f"{key}:{val}" for key,val in PART.Header().items()]))
        fp.write("\n\nPIG HEADER"+'-'*32+"\n")
        fp.write("\n".join([f"{key}:{val}" for key,val in PIG.Header().items()]))
        fp.write("\n\nOTHER"+'-'*32+"\n")
        fp.write(f"Center of Mass:{CX},{CY},{CZ}\n")
        fp.write(f"Center of Mass Velocity:{CVX},{CVY},{CVZ}\n")
        fp.write(f"Stellar Mass:{PIG.FOFGroups.MassByType().T[4][gid-1]}\n")
        fp.write(f"Region Span (Center to Edge) (ckpc/h):{SPAN}\n")


    if PTYPE==0:
        PT=PART.Gas
        # Read
        X,Y,Z = PT.Position(BLOBS).T
        VX,VY,VZ = PT.Velocity(BLOBS).T
        M = PT.Mass(BLOBS)
        IID = PT.ID(BLOBS)
        GID = PT.GroupID(BLOBS)
        rho = PT.Density(BLOBS)
        sml = PT.SmoothingLength(BLOBS)
        inteng = PT.InternalEnergy(BLOBS)
        Zm = PT.Metallicity(BLOBS)
        NH1 = PT.NeutralHydrogenFraction(BLOBS)
        metals = PT.Metals(BLOBS)
        elec_abdn = PT.ElectronAbundance(BLOBS)

        # Find Mask
        maskx = (CX-SPAN<X)&(X<CX+SPAN)
        masky = (CY-SPAN<Y)&(Y<CY+SPAN)
        maskz = (CZ-SPAN<Z)&(Z<CZ+SPAN)
        mask = maskx & masky & maskz

        # Apply Mask
        X,Y,Z = X[mask],Y[mask],Z[mask]
        VX,VY,VZ = VX[mask],VY[mask],VZ[mask]
        M=M[mask]
        rho=rho[mask]
        sml=sml[mask]
        inteng=inteng[mask]
        Zm=Zm[mask]
        NH1=NH1[mask]
        IID=IID[mask]
        GID=GID[mask]
        metals=metals[mask]
        elec_abdn=elec_abdn[mask]


        # Dump
        pos = np.column_stack((X,Y,Z))
        vel = np.column_stack((VX,VY,VZ))

        with open(OUTDIR+os.sep+f"Position.dat","wb") as fp:
            pickle.dump(pos,fp)

        with open(OUTDIR+os.sep+f"Velocity.dat","wb") as fp:
            pickle.dump(vel,fp)

        with open(OUTDIR+os.sep+f"Mass.dat","wb") as fp:
            pickle.dump(M,fp)

        with open(OUTDIR+os.sep+f"Metallicity.dat","wb") as fp:
            pickle.dump(Zm,fp)

        with open(OUTDIR+os.sep+f"Density.dat","wb") as fp:
            pickle.dump(rho,fp)

        with open(OUTDIR+os.sep+f"ID.dat","wb") as fp:
            pickle.dump(IID,fp)

        with open(OUTDIR+os.sep+f"GroupID.dat","wb") as fp:
            pickle.dump(GID,fp)

        with open(OUTDIR+os.sep+f"SmoothingLength.dat","wb") as fp:
            pickle.dump(sml,fp)

        with open(OUTDIR+os.sep+f"InternalEnergy.dat","wb") as fp:
            pickle.dump(inteng,fp)

        with open(OUTDIR+os.sep+f"NeutralHydrogenFraction.dat","wb") as fp:
            pickle.dump(NH1,fp)

        with open(OUTDIR+os.sep+f"Metals.dat","wb") as fp:
            pickle.dump(metals,fp)

        with open(OUTDIR+os.sep+f"ElectronAbundance.dat","wb") as fp:
            pickle.dump(elec_abdn,fp)

    elif PTYPE==4:
        PT=PART.Star
        # Read
        X,Y,Z = PT.Position(BLOBS).T
        VX,VY,VZ = PT.Velocity(BLOBS).T
        M = PT.Mass(BLOBS)
        IID = PT.ID(BLOBS)
        GID = PT.GroupID(BLOBS)

        # Find Mask
        maskx = (CX-SPAN<X)&(X<CX+SPAN)
        masky = (CY-SPAN<Y)&(Y<CY+SPAN)
        maskz = (CZ-SPAN<Z)&(Z<CZ+SPAN)
        mask = maskx & masky & maskz

        # Apply Mask
        X,Y,Z = X[mask],Y[mask],Z[mask]
        VX,VY,VZ = VX[mask],VY[mask],VZ[mask]
        M=M[mask]
        IID=IID[mask]
        GID=GID[mask]

        # Dump
        pos = np.column_stack((X,Y,Z))
        vel = np.column_stack((VX,VY,VZ))

        with open(OUTDIR+os.sep+f"Position.dat","wb") as fp:
            pickle.dump(pos,fp)

        with open(OUTDIR+os.sep+f"Velocity.dat","wb") as fp:
            pickle.dump(vel,fp)

        with open(OUTDIR+os.sep+f"Mass.dat","wb") as fp:
            pickle.dump(M,fp)

        with open(OUTDIR+os.sep+f"ID.dat","wb") as fp:
            pickle.dump(IID,fp)

        with open(OUTDIR+os.sep+f"GroupID.dat","wb") as fp:
            pickle.dump(GID,fp)

def DumpPtype(GIDDIR):
    PDIR = GIDDIR+os.sep+str(PTYPE)
    os.makedirs(PDIR,exist_ok=True)
    IBLOB_FILE = PDIR+os.sep+"iblobs.txt"
    if os.path.exists(IBLOB_FILE):
        print("  Using Existing iblob file.")
        with open(IBLOB_FILE,'r') as fp:
            iblobs=fp.read().split("\n")
    else:
        print("  Getting intersecting blobs.")
        iblobs = Get_Intersecting_Blobs(gid)
        print("  Caching iblob file.")
        with open(IBLOB_FILE,'w') as fp:
            fp.write('\n'.join(iblobs))

    Crop_And_Save_Fields(iblobs,PDIR)


# ------------------------------------------------------------------
selected_gids=GetSelectedGIDs()

SAVEDIR = SAVEDIR + os.sep + "GIDSET"
os.makedirs(SAVEDIR,exist_ok=True)

for i,gid in enumerate(selected_gids):
    print(f"- GID : {gid} ({i+1}/{len(selected_gids)})",'-'*32)
    GIDDIR=SAVEDIR+os.sep+f"GID_{gid}"
    os.makedirs(GIDDIR,exist_ok=True)
    PTYPE=0
    print("  Gas")
    DumpPtype(GIDDIR)
    PTYPE=4
    print("  Star")
    DumpPtype(GIDDIR)
    
    break