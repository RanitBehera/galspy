import galspy,numpy
from galspy.utility.visualization import CubeVisualizer
import pickle,os
import matplotlib.pyplot as plt
# from 
from galspy.utility.Figure.Beautification import SetMyStyle
SetMyStyle()

SAVEDIR = "/mnt/home/student/cranit/RANIT/Repo/galspy/scripts_2/pysphviewer/data_spm"

CX,CY,CZ = numpy.loadtxt(SAVEDIR+os.sep+"region_info_star.txt",delimiter=',')[0]   #<-----
print(CX,CY,CZ)

with open(SAVEDIR+os.sep+"pos_star.dat","rb") as fp:     #<-----
    pos_star=pickle.load(fp) - numpy.array([CX,CY,CZ])

with open(SAVEDIR+os.sep+"mass_star.dat","rb") as fp:    #<-----
    M_star=pickle.load(fp)

with open(SAVEDIR+os.sep+"pos_bh.dat","rb") as fp:     #<-----
    pos_bh=pickle.load(fp) - numpy.array([CX,CY,CZ])

with open(SAVEDIR+os.sep+"mass_bh.dat","rb") as fp:    #<-----
    M_bh=pickle.load(fp)




cv=CubeVisualizer()
cv.add_points(pos_star,points_size=2,points_alpha=0.5,points_color='tomato')
# cv.add_points(pos_bh,points_size=[300,0,0],points_alpha=1,points_color='k')
# cv.add_points(numpy.array([[-4,-3,-1]]),200,points_alpha=1,points_color='g')
# cv.axis3d.scatter(pos_bh[0][0],pos_bh[0][1],pos_bh[0][2],s=10000,color='k',ec='none',alpha=1,marker='+',lw=2)
ax=cv.show(False)

plt.show()
# plt.savefig("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts_ppt/BBGB_2024/data/frames"+os.sep+f"fr_{a}.png",dpi=400)
    









