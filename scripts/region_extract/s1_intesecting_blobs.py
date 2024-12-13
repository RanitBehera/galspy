import galspy,os
import numpy as np
from multiprocessing import Pool

L150N2040 = "/mnt/home/student/cranit/NINJA/simulations/L150N2040/SNAPS"
root = galspy.NavigationRoot(L150N2040)
SNAP_NUM = 43


center_kpc = root.PIG(SNAP_NUM).FOFGroups.MassCenterPosition()[1]
span_kpc   = 2500*np.ones(3)

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
    X,Y,Z = root.PART(SNAP_NUM).Gas.Position([blobname]).T          #<------
    
    minX,maxX = np.min(X),np.max(X)
    minY,maxY = np.min(Y),np.max(Y)
    minZ,maxZ = np.min(Z),np.max(Z)
    
    # Overlaps
    ovlX = (maxX>=bxn) and (minX<=bxp)
    ovlY = (maxY>=byn) and (minY<=byp)
    ovlZ = (maxZ>=bzn) and (minZ<=bzp)
    
    # Not Full box boundary blobs
    # smallX = (maxX-minX)<148000
    # smallY = (maxY-minY)<148000
    # smallZ = (maxZ-minZ)<148000
    
    intersecting = ovlX and ovlY and ovlZ #and smallX and smallY and smallZ
    return intersecting

if __name__=="__main__":
    with Pool(20) as pool:
        mask = pool.map(Checkblob,blobnames)
    iblobs=list(np.array(blobnames,dtype=str)[mask])
    print(iblobs)











