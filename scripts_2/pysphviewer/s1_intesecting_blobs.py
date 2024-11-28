import galspy,os
import numpy as np
from multiprocessing import Pool

L150N2040 = "/mnt/home/student/cranit/NINJA/simulations/L150N2040/SNAPS"
root = galspy.NavigationRoot(L150N2040)
SNAP_NUM = 43


GID = 1
center_kpc = root.PIG(SNAP_NUM).FOFGroups.MassCenterPosition()[GID-1]
span_kpc   = [2500,2500,2500]

print(f"Scan Center : (ckpc/h)".ljust(32,"-"))
print(f"  - x : {center_kpc[0]:.2f}")
print(f"  - y : {center_kpc[1]:.2f}")
print(f"  - z : {center_kpc[2]:.2f}")
print()
print(f"Scan Span : (ckpc/h)".ljust(32,"-"))
print(f"  - x : {span_kpc[0]:.2f}")
print(f"  - y : {span_kpc[1]:.2f}")
print(f"  - z : {span_kpc[2]:.2f}")
print()
print(f"Scan Boundary : (ckpc/h)".ljust(32,"-"))
bxn,bxp=center_kpc[0]-span_kpc[0],center_kpc[0]+span_kpc[0]
byn,byp=center_kpc[1]-span_kpc[1],center_kpc[1]+span_kpc[1]
bzn,bzp=center_kpc[2]-span_kpc[2],center_kpc[2]+span_kpc[2]
print(f"  - x : {bxn:.2f} <-> {bxp:.2f}")
print(f"  - y : {byn:.2f} <-> {byp:.2f}")
print(f"  - x : {bzn:.2f} <-> {bzp:.2f}")
print()



blobnames = sorted(os.listdir(root.PART(SNAP_NUM).DarkMatter.GroupID.path))
blobnames.remove("attr-v2")
blobnames.remove("header")
    
print("Scanning Intersection")

def Checkblob(blobname:str):
    X,Y,Z = root.PART(SNAP_NUM).Gas.Position([blobname]).T
    inX = (np.max(X)>=bxn) and (np.min(X)<=bxp)
    inY = (np.max(Y)>=byn) and (np.min(Y)<=byp)
    inZ = (np.max(Z)>=bzn) and (np.min(Z)<=bzp)
    inblob = inX and inY and inZ
    return inblob

if __name__=="__main__":
    with Pool(20) as pool:
        mask = pool.map(Checkblob,blobnames)
    iblobs=list(np.array(blobnames,dtype=str)[mask])
    print(iblobs)











