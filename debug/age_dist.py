import galspy

PATH = "/mnt/home/student/cranit/NINJA/simulations/L150N2040/SNAPS"

root = galspy.NavigationRoot(PATH)

age = root.PIG(11).Star.StarFormationTime()

print(age)