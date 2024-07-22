import galspy.IO.MPGadget as mp
import galspy.utility.HaloQuery as rs
import galspy.utility.visualization as vis
import matplotlib.pyplot as plt
import galspy.IO.BigFile as bf

import os


path = "/mnt/home/student/cranit/Work/test_para_rock/OUT_L10N64"
root = mp.NavigationRoot(path)
snap = 17
qr = rs.RSGQuery(root.RSG(snap).path)

# print(qr.get_massive_halos())

bn = qr.get_blobname_of_halo_id(121)
ihid = qr.get_internal_halo_id_of(121,bn)

des = qr.get_descendant_halos_of(ihid,bn)

# print(bn)
# print(ihid)
# print(des)
# exit()

pos=qr.get_child_particle_positions(des,bn)

ax = plt.axes(projection="3d")
cv = vis.CubeVisualizer(ax)
cv.add_points(pos,1,'r')

# print(pos1)

centers=[]

chs = qr.get_descendant_halos_of(ihid,bn)

cpos = bf.Blob(root.RSG(snap).RKSHalos.Position.path + os.sep + bn).Read()
for ch in chs:
    centers.append(cpos[ch])

# print(centers)

cv.add_points(centers,50,'k')

cv.show()


