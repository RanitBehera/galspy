# check all the particle positions dumped by rockstar


import galspy.IO.MPGadget as mp
import galspy.utility.HaloQuery as hq
import galspy.utility.visualization as vis
import os,numpy



root = mp.NavigationRoot("/mnt/home/student/cranit/Work/test_para_rock/L10N64").RSG(17)
cv = vis.CubeVisualizer()
BLOB = "000006"


particle_pos    = root.RKSParticles.Position(BLOB)
cv.add_points(particle_pos,points_color='magenta',points_alpha=0.5)

halo_cen        = root.RKSHalos.Position(BLOB) 
hid             = root.RKSHalos.HaloID(BLOB)
ihid            = root.RKSHalos.InternalHaloID(BLOB)

hcen = halo_cen[hid!=-1]
ihid = ihid[hid!=-1]
hid = hid[hid!=-1]


cv.add_points(hcen,points_color='k',points_size=20)
ax = cv.get_axis()
for j in range(len(hcen)):
    ax.text(hcen[j,0],hcen[j,1],hcen[j,2],str(ihid[j]),size=10,zorder=100)


cv.show()