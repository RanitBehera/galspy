import galspy
import numpy

root=galspy.NavigationRoot("/mnt/home/student/cranit/NINJA/simulations/L10N64_Debug/SNAPS/")

gid = root.PIG(18).FOFGroups.GroupID() 
lbt = root.PIG(18).FOFGroups.LengthByType()

glbt,dmlbt,_,_,slbt,bhlbt = lbt.T


dmcs = numpy.cumsum(dmlbt)


# for cgid,gl,dml,sl,bhl in zip(gid,glbt,dmlbt,slbt,bhlbt):
#     print(cgid,gl,gl,dml,sl)

i=0
for cgid,dml,dmcsi in zip(gid,dmlbt,dmcs):
    print(cgid,dml,dmcsi)
    i+=1
    if i==10:break

particles = root.PIG(18).DarkMatter.GroupID()

print(particles[4010])
