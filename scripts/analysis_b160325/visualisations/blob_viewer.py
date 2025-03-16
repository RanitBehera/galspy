import galspy
from galspy.utility.visualization import CubeVisualizer


# MPGADGET_OUTPUT_DIR = "/mnt/home/student/cranit/NINJA/simulations/L150N2040/SNAPS"
MPGADGET_OUTPUT_DIR = "/mnt/home/student/cranit/NINJA/simulations/L10N64_Debug/sig8/TwoRun/L10N64/WithSig8/SNAPS/"
SNAP_NUM = 33

root = galspy.NavigationRoot(MPGADGET_OUTPUT_DIR)
SNAP = root.PART(SNAP_NUM)

dm_pos0=SNAP.DarkMatter.Position(["000000"])/1e3
dm_pos1=SNAP.DarkMatter.Position(["000001"])/1e3
dm_pos2=SNAP.DarkMatter.Position(["000002"])/1e3
dm_pos3=SNAP.DarkMatter.Position(["000003"])/1e3



# ----- Visualise
cv=CubeVisualizer()
cv.add_points(dm_pos0,points_color='r',points_alpha=0.5)
cv.add_points(dm_pos1,points_color='g',points_alpha=0.5)
cv.add_points(dm_pos2,points_color='b',points_alpha=0.5)
cv.add_points(dm_pos3,points_color='c',points_alpha=0.5)



# cv.add_points(gas_pos,points_color='c',points_alpha=0.2)
# cv.add_points(star_pos,points_color='r',points_alpha=0.1,points_size=10)
# cv.add_points(bh_pos,points_color='k',points_alpha=1,points_size=30)

cv.show()

