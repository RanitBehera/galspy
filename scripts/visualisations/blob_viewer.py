import galspy
from galspy.utility.visualization import CubeVisualizer


MPGADGET_OUTPUT_DIR = "/mnt/home/student/cranit/NINJA/simulations/L10N64_Debug/sig8/TwoRun/L10N64/WithSig8/SNAPS"
SNAP_NUM = 33
BLOB="00003A"

root = galspy.NavigationRoot(MPGADGET_OUTPUT_DIR)
SNAP = root.PART(SNAP_NUM)
dm_pos=SNAP.DarkMatter.Position()/1e3



# ----- Visualise
cv=CubeVisualizer()
cv.add_points(dm_pos,points_color='k',points_alpha=0.5)
# cv.add_points(gas_pos,points_color='c',points_alpha=0.2)
# cv.add_points(star_pos,points_color='r',points_alpha=0.1,points_size=10)
# cv.add_points(bh_pos,points_color='k',points_alpha=1,points_size=30)

cv.show()

