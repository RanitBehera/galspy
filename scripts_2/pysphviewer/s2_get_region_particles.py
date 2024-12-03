
import galspy,numpy
from galspy.utility.visualization import CubeVisualizer
import pickle,os

PATH = "/mnt/home/student/cranit/NINJA/simulations/L150N2040/SNAPS"
ROOT = galspy.NavigationRoot(PATH)
SAVEDIR = "/mnt/home/student/cranit/RANIT/Repo/galspy/scripts_2/pysphviewer/data"


print("Reading centers")
CX,CY,CZ = ROOT.PIG(43).FOFGroups.MassCenterPosition()[1]
CX += -4
CY += -3
CZ += -1
print(CX,CY,CZ)


if True:
    SPAN = 2500
    # BLOBS = ['000000', '00000E', '000032', '000033', '000040', '000042', '000043', '00006A', '00006B', '000075', '000076']            #<----DM
    BLOBS = ['000000', '00002E', '00002F', '00003D', '00003E', '000075']    #<----Gas
    # BLOBS = ['000000', '000001', '00002E', '00002F', '000039', '00003A', '00003B', '00003D', '000075']    #<----Star
    # BLOBS = ['000000', '00003B', '00003C', '00003D', '000075']    #<----BH

    with open(SAVEDIR+os.sep+"region_info_gas.txt","w") as fp:      #<-----
        fp.write("# lengths in ckpc/h\n")
        fp.write(f"{CX},{CY},{CZ}\n{SPAN},{SPAN},{SPAN}")

    print("Reading particle pos")
    X,Y,Z = ROOT.PART(43).Gas.Position(BLOBS).T          #<------


    print("Reading particle mass")
    # M = ROOT.PART(43).Gas.Mass(BLOBS)                    #<------
    M = ROOT.PART(43).Gas.InternalEnergy(BLOBS)                    #<------
    # M = ROOT.PART(43).BlackHole.BlackholeMass(BLOBS)                    #<------

    

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
    M=M[mask]
    print(f"Found {len(M)} particles with masking.")

    print("stacking")
    pos = numpy.column_stack((X,Y,Z))

    with open(SAVEDIR+os.sep+"pos_gas.dat","wb") as fp:     #<-----
        pickle.dump(pos,fp)

    with open(SAVEDIR+os.sep+"mass_gas.dat","wb") as fp:    #<-----
        pickle.dump(M,fp)

    print("dumped")


