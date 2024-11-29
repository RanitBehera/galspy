import galspy,numpy
from galspy.utility.visualization import CubeVisualizer
import pickle,os
# from 

SAVEDIR = "/mnt/home/student/cranit/RANIT/Repo/galspy/scripts_2/pysphviewer/data_spm"


CX,CY,CZ = numpy.loadtxt(SAVEDIR+os.sep+"region_info_star.txt",delimiter=',')[0]   #<-----
print(CX,CY,CZ)

with open(SAVEDIR+os.sep+"pos_star.dat","rb") as fp:     #<-----
    pos_star=pickle.load(fp)

with open(SAVEDIR+os.sep+"mass_star.dat","rb") as fp:    #<-----
    M_star=pickle.load(fp)



CX,CY,CZ = numpy.loadtxt(SAVEDIR+os.sep+"region_info_gas.txt",delimiter=',')[0]   #<-----
print(CX,CY,CZ)

with open(SAVEDIR+os.sep+"pos_gas.dat","rb") as fp:     #<-----
    pos_gas=pickle.load(fp)

with open(SAVEDIR+os.sep+"mass_gas.dat","rb") as fp:    #<-----
    M_gas=pickle.load(fp)


CX,CY,CZ = numpy.loadtxt(SAVEDIR+os.sep+"region_info_bh.txt",delimiter=',')[0]   #<-----
print(CX,CY,CZ)

with open(SAVEDIR+os.sep+"pos_bh.dat","rb") as fp:     #<-----
    pos_bh=pickle.load(fp)

with open(SAVEDIR+os.sep+"mass_bh.dat","rb") as fp:    #<-----
    M_bh=pickle.load(fp)



cv=CubeVisualizer()
cv.add_points(pos_star,points_size=1,points_alpha=0.6,points_color='tomato')
cv.add_points(pos_gas,points_size=1,points_alpha=1,points_color='b')
cv.add_points(pos_bh,points_size=30,points_alpha=1,points_color='k')
# cv.add_points(numpy.array([[CX,CY,CZ]]),points_size=30,points_alpha=1,points_color='r')
cv.show()








