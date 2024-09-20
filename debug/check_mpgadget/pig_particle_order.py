import galspy
import numpy

root=galspy.NavigationRoot("/mnt/home/student/cranit/NINJA/simulations/L10N64_Debug/SNAPS/")

gid = root.PIG(18).FOFGroups.GroupID() 

print(gid)