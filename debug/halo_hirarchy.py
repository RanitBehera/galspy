import galspy.IO.MPGadget as mp
import galspy.utility.HaloQuery as rs
import galspy.utility.visualization as vis
import matplotlib.pyplot as plt
import galspy.IO.BigFile as bf

import os,numpy


path = "/mnt/home/student/cranit/Work/test_para_rock/OUT_L10N64"
root = mp.NavigationRoot(path)
snap = 17
qr = rs.RSGQuery(root.RSG(snap).path)

# print(qr.get_massive_halos())

bn = qr.get_blobname_of_halo_id(121)
ihid = qr.get_internal_halo_id_of(121,bn)

des = qr.get_descendant_halos_of(ihid,bn)

ax = plt.axes(projection="3d")
cv = vis.CubeVisualizer(ax)
colors= ['r','g','b','y','m','lime','pink']
for i,d in enumerate(des):
    pos=qr.get_child_particle_positions(des,bn)
    cv.add_points(pos,1,colors[i])

print(des)


cv.show()


