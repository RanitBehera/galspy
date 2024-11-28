
import galspy,numpy
from galspy.utility.visualization import CubeVisualizer
import pickle

PATH = "/mnt/home/student/cranit/NINJA/simulations/L150N2040/SNAPS"
ROOT = galspy.NavigationRoot(PATH)

print("Reading centers")
CX,CY,CZ = ROOT.PIG(43).FOFGroups.MassCenterPosition()[0]
# SPAN = 2500
# BLOBS = ['000000', '00000D', '00000E', '000032', '000033', '000040', '000042', '000043', '00006A', '00006B', '000075', '000076']

print(CX,CY,CZ)

# print("Reading particle pos")
# X,Y,Z = ROOT.PART(43).Gas.Position(BLOBS).T

# print("Reading gas mass")
# M = ROOT.PART(43).Gas.Mass(BLOBS)

# print(len(M))

# print("masking X")
# maskx = (CX-SPAN<X)&(X<CX+SPAN)
# print("masking Y")
# masky = (CY-SPAN<Y)&(Y<CY+SPAN)
# print("masking Z")
# maskz = (CZ-SPAN<Z)&(Z<CZ+SPAN)
# print("combining mask")



# mask = maskx & masky & maskz

# print("applying mask")
# X,Y,Z = X[mask],Y[mask],Z[mask]
# M=M[mask]
# print("stacking")
# pos = numpy.column_stack((X,Y,Z))

# print(len(pos))

# with open("/mnt/home/student/cranit/RANIT/Repo/galspy/temp/share_somak/pos.dat","wb") as fp:
#     pickle.dump(pos,fp)

# with open("/mnt/home/student/cranit/RANIT/Repo/galspy/temp/share_somak/mass.dat","wb") as fp:
#     pickle.dump(M,fp)




# with open("/mnt/home/student/cranit/RANIT/Repo/galspy/temp/share_somak/pos.dat","rb") as fp:
#     pos=pickle.load(fp)

# with open("/mnt/home/student/cranit/RANIT/Repo/galspy/temp/share_somak/mass.dat","rb") as fp:
#     M=pickle.load(fp)


# mini = numpy.random.random(len(pos))
# mask = mini>0.95

# cv=CubeVisualizer()
# cv.add_points(pos/1000,points_size=1,points_alpha=0.1)
# # cv.add_points([[CX,CY,CZ]],points_size=30,points_alpha=1,points_color='r')

# cv.show()

