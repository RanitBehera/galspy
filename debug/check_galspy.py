import galspy

root=galspy.NavigationRoot("/mnt/home/student/cranit/NINJA/simulations/L150N2040/SNAPS")

hd=root.PART(11).Header()



print(type(hd),hd)