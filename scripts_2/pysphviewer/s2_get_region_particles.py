
import galspy,numpy
from galspy.utility.visualization import CubeVisualizer
import pickle,os

PATH = "/mnt/home/student/cranit/NINJA/simulations/L150N2040/SNAPS"
ROOT = galspy.NavigationRoot(PATH)
SAVEDIR = "/mnt/home/student/cranit/RANIT/Repo/galspy/scripts_2/pysphviewer/data"



print("Reading centers")
CX,CY,CZ = ROOT.PIG(43).FOFGroups.MassCenterPosition()[0]

if True:
    SPAN = 2500
    # BLOBS = ['000000', '00000E', '000032', '000033', '000040', '000042', '000043', '00006A', '00006B', '000075', '000076']    #<----DM
    # BLOBS = ['000000', '00000D', '00000E', '000032', '000033', '000040', '000042', '000043', '00006A', '00006B', '000075', '000076']    #<----Gas
    BLOBS = ['000000', '000001', '00000B', '00000C', '000030', '000031', '00003F', '000040', '000041', '000042', '000043', '00006A', '00006B', '00006C', '000075', '000076']    #<----Star

    with open(SAVEDIR+os.sep+"region_info_star.txt","w") as fp:      #<-----
        fp.write("# lengths in ckpc/h\n")
        fp.write(f"{CX} {CY} {CZ}\n{SPAN} {SPAN} {SPAN}")

    print("Reading particle pos")
    X,Y,Z = ROOT.PART(43).Star.Position(BLOBS).T          #<------

    print("Reading particle mass")
    M = ROOT.PART(43).Star.Mass(BLOBS)                    #<------

    print(len(M))

    print("masking X")
    maskx = (CX-SPAN<X)&(X<CX+SPAN)
    print("masking Y")
    masky = (CY-SPAN<Y)&(Y<CY+SPAN)
    print("masking Z")
    maskz = (CZ-SPAN<Z)&(Z<CZ+SPAN)
    print("combining mask")



    mask = maskx & masky & maskz

    print("applying mask")
    X,Y,Z = X[mask],Y[mask],Z[mask]
    M=M[mask]
    print("stacking")
    pos = numpy.column_stack((X,Y,Z))

    with open(SAVEDIR+os.sep+"pos_star.dat","wb") as fp:     #<-----
        pickle.dump(pos,fp)

    with open(SAVEDIR+os.sep+"mass_star.dat","wb") as fp:    #<-----
        pickle.dump(M,fp)



if True:
    with open(SAVEDIR+os.sep+"pos_star.dat","rb") as fp:     #<-----
        pos=pickle.load(fp)

    with open(SAVEDIR+os.sep+"mass_star.dat","rb") as fp:    #<-----
        M=pickle.load(fp)

    CX,CY,CZ = numpy.loadtxt(SAVEDIR+os.sep+"region_info_star.txt")[0]   #<-----

    mini = numpy.random.random(len(pos))
    mask = mini>0.5

    cv=CubeVisualizer()
    cv.add_points(pos/1000,points_size=1,points_alpha=0.1)
    cv.add_points(numpy.array([[CX,CY,CZ]])/1000,points_size=30,points_alpha=1,points_color='r')

    cv.show()

