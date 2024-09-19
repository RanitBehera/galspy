import galspy
import numpy
import matplotlib.pyplot as plt
from galspy.utility.visualization import CubeVisualizer



# MPGADGET_OUTPUT_DIR = "/mnt/home/student/cranit/Data/MP_Gadget/Nishi/L50N640"
MPGADGET_OUTPUT_DIR = "/mnt/home/student/cranit/NINJA/simulations/L150N2040/SNAPS"
SNAP = 38
GROUP_OFFSET = 0


root = galspy.NavigationRoot(MPGADGET_OUTPUT_DIR)
PIG = root.PIG(SNAP)
target_group_id = PIG.FOFGroups.GroupID()[GROUP_OFFSET]
dm_pos = PIG.DarkMatter.Position()[PIG.DarkMatter.GroupID()==target_group_id]



gas_pos = PIG.Gas.Position()[PIG.Gas.GroupID()==target_group_id]
star_pos = PIG.Star.Position()[PIG.Star.GroupID()==target_group_id]
bh_pos = PIG.BlackHole.Position()[PIG.BlackHole.GroupID()==target_group_id]


# ----- Visualise
cv=CubeVisualizer()
# cv.add_points(dm_pos,points_color='k',points_alpha=0.5)
# cv.add_points(gas_pos,points_color='c',points_alpha=0.8)
cv.add_points(star_pos,points_color='r',points_alpha=0.5,points_size=10)
cv.add_points(bh_pos,points_color='k',points_alpha=1,points_size=300)
cv.show()



