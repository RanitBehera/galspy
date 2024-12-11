
import galspy,numpy
from galspy.utility.visualization import CubeVisualizer
import pickle,os

PATH = "/mnt/home/student/cranit/NINJA/simulations/L150N2040/SNAPS"
ROOT = galspy.NavigationRoot(PATH)
SAVEDIR = "/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/region_extract/data"
SPAN = 2000 #kpc
SUFFIX="gas_1"

print("Reading centers")
CX,CY,CZ = ROOT.PIG(43).FOFGroups.MassCenterPosition()[1]       #1 for gid
CX += -4
CY += -3
CZ += -1
print(CX,CY,CZ)
CVX,CVY,CVZ = ROOT.PIG(43).FOFGroups.MassCenterVelocity()[1]       #1 for gid


if True:
    BLOBS = ['000000', '00002E', '00002F', '000030', '00003D', '00003E', '00003F', '000075']

    with open(SAVEDIR+os.sep+f"region_info_{SUFFIX}.txt","w") as fp:
        fp.write("# lengths in ckpc/h then velocity\n")
        fp.write(f"{CX},{CY},{CZ}\n{SPAN},{SPAN},{SPAN}\n")
        fp.write(f"{CVX},{CVY},{CVZ}")

    exit()

    print("Reading particle pos")
    X,Y,Z = ROOT.PART(43).Gas.Position(BLOBS).T          #<------
    VX,VY,VZ = ROOT.PART(43).Gas.Velocity(BLOBS).T          #<------


    print("Reading particle mass")
    M = ROOT.PART(43).Gas.Mass(BLOBS)                    #<------
    # M = ROOT.PART(43).Gas.InternalEnergy(BLOBS)                    #<------
    # M = ROOT.PART(43).BlackHole.BlackholeMass(BLOBS)                    #<------
    Zm = ROOT.PART(43).Gas.Metallicity(BLOBS)                    #<------

    

    print("masking X")
    maskx = (CX-SPAN<X)&(X<CX+SPAN)
    print("masking Y")
    masky = (CY-SPAN<Y)&(Y<CY+SPAN)
    print("masking Z")
    maskz = (CZ-SPAN<Z)&(Z<CZ+SPAN)
    print("combining mask")


    mask = maskx & masky & maskz

    print("Applying mask")
    X,Y,Z = X[mask],Y[mask],Z[mask]
    VX,VY,VZ = VX[mask],VY[mask],VZ[mask]
    M=M[mask]
    Zm=Zm[mask]
    print(f"Found {len(M)} particles with masking.")

    print("stacking")
    pos = numpy.column_stack((X,Y,Z))
    vel = numpy.column_stack((VX,VY,VZ))

    with open(SAVEDIR+os.sep+f"pos_{SUFFIX}.dat","wb") as fp:     #<-----
        pickle.dump(pos,fp)
        print("Position dumped.")

    with open(SAVEDIR+os.sep+f"vel_{SUFFIX}.dat","wb") as fp:     #<-----
        pickle.dump(vel,fp)
        print("Velocity dumped.")

    with open(SAVEDIR+os.sep+f"mass_{SUFFIX}.dat","wb") as fp:    #<-----
        pickle.dump(M,fp)
        print("Mass dumped.")

    with open(SAVEDIR+os.sep+f"metallicity_{SUFFIX}.dat","wb") as fp:    #<-----
        pickle.dump(Zm,fp)
        print("Metallicity dumped.")


