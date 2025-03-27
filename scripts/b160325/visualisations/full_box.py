import galspy
import numpy
import matplotlib.pyplot as plt
from galspy.utility.visualization import CubeVisualizer


# MPGADGET_OUTPUT_DIR = "/mnt/home/student/cranit/Data/MP_Gadget/Nishi/L50N640"
# MPGADGET_OUTPUT_DIR = "/mnt/home/student/cranit/NINJA/simulations/L150N2040/SNAPS"
MPGADGET_OUTPUT_DIR = "/mnt/home/student/cranit/NINJA/simulations/L10N64_Debug/sig8/TwoRun/L10N64/WithSig8/SNAPS"
SNAP_NUM = 33


# Target Group Filter
root = galspy.NavigationRoot(MPGADGET_OUTPUT_DIR)
PIG = root.PIG(SNAP_NUM)


dm_pos = PIG.DarkMatter.Position()
gas_pos = PIG.Gas.Position()
star_pos = PIG.Star.Position()
bh_pos = PIG.BlackHole.Position()


# ----- Visualise
cv=CubeVisualizer()
cv.add_points(dm_pos,points_color='k',points_alpha=0.1)
# cv.add_points(gas_pos,points_color='c',points_alpha=0.2)
# cv.add_points(star_pos,points_color='r',points_alpha=0.1,points_size=10)
# cv.add_points(bh_pos,points_color='k',points_alpha=1,points_size=30)

cv.show()



