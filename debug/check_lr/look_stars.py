import galspy
import matplotlib.pyplot as plt
import numpy as np

from galspy.utility.visualization import CubeVisualizer


print("hi")

SNAPPATH ="/mnt/home/student/cranit/Data/MP_Gadget/Nishi/L50N1008z05"

root=galspy.NavigationRoot(SNAPPATH)

PIG = root.PIG(174)

pos= PIG.Star.Position()
gid = PIG.Star.GroupID()

tgid = 827
mask = gid==tgid

tpos = pos[mask]

cv = CubeVisualizer()
cv.add_points(tpos,points_alpha=0.1)

cv.show()

