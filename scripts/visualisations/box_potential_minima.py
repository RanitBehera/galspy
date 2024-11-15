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

# Check potential minimum
dm_gid = PIG.DarkMatter.GroupID()
dm_pot = PIG.DarkMatter.Potential()
gid,ind,count = numpy.unique(dm_gid,return_index=True,return_counts=True)

pot_min = []
for gid,ind,count in zip(gid,ind,count):
    if count<1000:continue
    chunk_pot = dm_pot[ind:ind+count]
    ind_sort = numpy.argsort(chunk_pot)
    min_pos = dm_pos[ind:ind+count][ind_sort][0]
    pot_min.append(min_pos)
pot_min = numpy.array(pot_min)

# ----- Visualise
cv=CubeVisualizer()
cv.add_points(dm_pos,points_color='k',points_alpha=0.1)
# cv.add_points(gas_pos,points_color='c',points_alpha=0.2)
# cv.add_points(star_pos,points_color='r',points_alpha=0.1,points_size=10)
# cv.add_points(bh_pos,points_color='k',points_alpha=1,points_size=30)
cv.add_points(pot_min,points_color='r',points_alpha=1,points_size=30)

cv.show()



