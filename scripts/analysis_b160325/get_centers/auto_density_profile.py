import galspy
import numpy as np
import os
from galspy.MPGadget import _PART
from multiprocessing import Pool


L150N2040 = "/mnt/home/student/cranit/NINJA/simulations/L150N2040/SNAPS"
root = galspy.NavigationRoot(L150N2040)
SNAP_NUM = 43
PART = root.PART(SNAP_NUM)


def Checkblob(packed_arguments):
    blobname,center_kpc,span_kpc = packed_arguments

    # Boundaries
    bxn,bxp=center_kpc[0]-span_kpc[0],center_kpc[0]+span_kpc[0]
    byn,byp=center_kpc[1]-span_kpc[1],center_kpc[1]+span_kpc[1]
    bzn,bzp=center_kpc[2]-span_kpc[2],center_kpc[2]+span_kpc[2]

    X,Y,Z = PART.Gas.Position([blobname]).T

    minX,maxX = np.min(X),np.max(X)
    minY,maxY = np.min(Y),np.max(Y)
    minZ,maxZ = np.min(Z),np.max(Z)
    
    # Overlaps
    ovlX = (maxX>=bxn) and (minX<=bxp)
    ovlY = (maxY>=byn) and (minY<=byp)
    ovlZ = (maxZ>=bzn) and (minZ<=bzp)  

    intersecting = ovlX and ovlY and ovlZ
    return intersecting
    

def GetIntersectingBlobs(center_kpc,span_kpc):
    if type(span_kpc) in [float,int]:span_kpc = span_kpc*np.ones(3)
    blobnames = sorted(os.listdir(PART.DarkMatter.GroupID.path))
    blobnames.remove("attr-v2")
    blobnames.remove("header")

    packed_arguments = [(bn,center_kpc,span_kpc) for bn in blobnames]
    
    with Pool(20) as pool:
        mask = pool.map(Checkblob,packed_arguments)
    iblobs=list(np.array(blobnames,dtype=str)[mask])
    
    return iblobs


def GetRegionParticles(center_kpc,span_kpc):
    if type(span_kpc) in [float,int]:span_kpc = span_kpc*np.ones(3)
    iblobs = GetIntersectingBlobs(center_kpc,span_kpc)

    # Masking
    CX,CY,CZ=center_kpc
    SX,SY,SZ=span_kpc
    X,Y,Z = PART.Gas.Position(iblobs).T
    maskx = (CX-SX<X)&(X<CX+SX)
    masky = (CY-SY<Y)&(Y<CY+SY)
    maskz = (CZ-SZ<Z)&(Z<CZ+SZ)
    mask = maskx & masky & maskz


    # Required fields
    M = PART.Gas.Mass(iblobs)[mask]          
    X,Y,Z = PART.Gas.Position(iblobs)[mask].T
    # VX,VY,VZ = PART.Gas.Velocity(iblobs)[mask].T
    # rho = PART.Gas.Density(iblobs)[mask]
    # sml = PART.Gas.SmoothingLength(iblobs)[mask]
    # inteng = PART.Gas.InternalEnergy(iblobs)[mask]
    # Zm = PART.Gas.Metallicity(iblobs)[mask]          
    # NH1 = PART.Gas.NeutralHydrogenFraction(iblobs)[mask]

    pos = np.column_stack([X,Y,Z])
    mass=M
    return pos,mass


h=PART.Header.HubbleParam()
a=PART.Header.Time()
Ob=PART.Header.OmegaBaryon()
z=PART.Header.Redshift()

def GetGasProfiles(center_kpc,span_kpc):
    if type(span_kpc) in [float,int]:span_kpc = span_kpc*np.ones(3)
    pos,mass = GetRegionParticles(center_kpc,span_kpc)
    
    # Go to local frame
    pos=pos-center_kpc


    # Get radial distance to particles
    rad = np.linalg.norm(pos,axis=1)
    
    # Physical Units
    mass*=1e10/h
    rad*=a/h

    # Radial Bin
    delta_rad = 1.
    bin_indices=np.int32(rad/delta_rad)
    num_bins = np.max(bin_indices) + 1
    # Brute force python for loop
    # bin_mass2[bin_indices[i]]+=mass[i]
    # Checked bruteforce gives same as following numpy method
    # Numpy advanced binning add - 7 times faster than brute force add
    bin_mass = np.zeros(num_bins)
    np.add.at(bin_mass,bin_indices,mass)

    # Evaluate profiles
    bin_rad = delta_rad*np.arange(num_bins)
    bin_volume = 4*np.pi*(bin_rad**2)*delta_rad
    
    # mass density
    bin_dens = bin_mass/bin_volume
    bin_dens *= 1.989e33/((3.086e21)**3) #M_sol/pkpc**3 to gm/cm**3 

    # number desnity
    nH = bin_dens*(0.753/(1.67e-24))

    return bin_rad,bin_dens,nH





table = np.loadtxt("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/get_centers/data/subokay.txt")
gid,nsubs,subid,nstar_group,nstar_sub,st_mass_fof,st_mass_sum,st_mass_sub,cx,cy,cz,cr=table.T
centers=np.column_stack([cx,cy,cz])




# r,rho,nH=GetGasProfiles(centers[0],10000)
# n_igm = (1.6e-7)*(Ob*(h**2)/0.019)*((1+z)**3)

DIR="/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/get_centers/data/profs"
for g,c in zip(gid,centers):
    g=int(g)
    print(g)
    r,rho,nH=GetGasProfiles(c,10000)
    with open(f"{DIR}/gid_{g}.txt","w") as fp:
        np.savetxt(fp,np.column_stack([r,rho,nH]))









# import matplotlib.pyplot as plt

# from scipy.ndimage import gaussian_filter

# prof=gaussian_filter(nH, sigma=2)

# plt.plot(r,prof)
# plt.axhline(n_igm)

# plt.xscale("log")
# plt.yscale("log")
# plt.show()
