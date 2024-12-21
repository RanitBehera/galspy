
import galspy,numpy
from galspy.utility.visualization import CubeVisualizer
import pickle,os

PATH = "/mnt/home/student/cranit/NINJA/simulations/L150N2040/SNAPS"
ROOT = galspy.NavigationRoot(PATH)
SAVEDIR = "/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/region_extract/data"
SPAN = 10000 #kpc
gid=2
SUFFIX=f"gas_{gid}"

print("Reading centers")
CX,CY,CZ = ROOT.PIG(43).FOFGroups.MassCenterPosition()[gid-1]       #1 for gid
CVX,CVY,CVZ = ROOT.PIG(43).FOFGroups.MassCenterVelocity()[gid-1]       #1 for gid


if True:
    BLOBS = ['000000', '000010', '000011', '000065', '000066', '000067', '000076']

    with open(SAVEDIR+os.sep+f"region_info_{SUFFIX}.txt","w") as fp:
        fp.write("# lengths in ckpc/h then velocity\n")
        fp.write(f"{CX},{CY},{CZ}\n{SPAN},{SPAN},{SPAN}\n")
        fp.write(f"{CVX},{CVY},{CVZ}")


    print("Reading particle pos")

    X,Y,Z = ROOT.PART(43).Gas.Position(BLOBS).T          #<------
    VX,VY,VZ = ROOT.PART(43).Gas.Velocity(BLOBS).T          #<------


    print("Reading particle mass")
    M = ROOT.PART(43).Gas.Mass(BLOBS)                    #<------
    rho = ROOT.PART(43).Gas.Density(BLOBS)
    sml = ROOT.PART(43).Gas.SmoothingLength(BLOBS)          #<-------
    inteng = ROOT.PART(43).Gas.InternalEnergy(BLOBS)
    Zm = ROOT.PART(43).Gas.Metallicity(BLOBS)                    #<------
    NH1 = ROOT.PART(43).Gas.NeutralHydrogenFraction(BLOBS)                    #<------

    

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
    rho=rho[mask]
    sml=sml[mask]
    inteng=inteng[mask]
    Zm=Zm[mask]
    NH1=NH1[mask]
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

    with open(SAVEDIR+os.sep+f"dens_{SUFFIX}.dat","wb") as fp:    #<-----
        pickle.dump(rho,fp)
    print("Density dumped.")

    with open(SAVEDIR+os.sep+f"sml_{SUFFIX}.dat","wb") as fp:    #<-----
        pickle.dump(sml,fp)
    print("Smoothing length dumped.")

    with open(SAVEDIR+os.sep+f"ie_{SUFFIX}.dat","wb") as fp:    #<-----
        pickle.dump(inteng,fp)
    print("Internal Energy dumped.")

    with open(SAVEDIR+os.sep+f"NHI_{SUFFIX}.dat","wb") as fp:    #<-----
        pickle.dump(NH1,fp)
    print("Neutral Hydrogen Fraction dumped.")




