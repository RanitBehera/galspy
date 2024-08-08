import galspy.IO.MPGadget as mp
import galspy.utility.HaloQuery as rs
import galspy.utility.visualization as vis
import matplotlib.pyplot as plt
import galspy.IO.BigFile as bf

import os,numpy

OUTBASE = "/mnt/home/student/cranit/Work/test_para_rock/L50N640"
SNAP = 36
root = mp.NavigationRoot(OUTBASE)
qr = rs.RSGQuery(root.RSG(SNAP).path)

ax = plt.axes(projection="3d")
cv = vis.CubeVisualizer(ax)




def plot_all_sub(ihid,clr='r'):
    if True:
        cv.add_points(qr.get_child_particle_positions([ihid],"000001"),2,clr)
    else:
        all_sub = qr.get_descendant_halos_of(ihid,"000001")
        all_sub = numpy.array(list(all_sub)+[ihid])
        valid = qr.check_if_valid_sub(all_sub,"000001")
        for sub,v in zip(all_sub,valid):
            if v:
                c = clr
                a = 1
            else:
                c= 'k'
                a = 0.1
            cv.add_points(qr.get_child_particle_positions([sub],"000001"),1,c,a)

    
    
    cpos = qr.get_centre_position([ihid],"000001")
    cv.add_points(cpos,50,'k')
    cv.add_text(cpos[0],str(ihid),'k')
    
    vrad = qr.get_virial_radius([ihid],"000001")
    cv.add_sphere_wire(cpos[0],vrad/1000,'k')

    # po = qr.get_vmax_r([ihid],"000001")
    # cv.add_sphere_wire(cpos[0],po,'r')
    


# L50N640 - HID 8
# plot_all_sub(461,'r')
# plot_all_sub(480,'r')
# plot_all_sub(510,'g')


# plot_all_sub(461)
# plot_all_sub(539)
# plot_all_sub(473)
# plot_all_sub(519)
# plot_all_sub(596)       # With sub : seems like a sheet
# plot_all_sub(549)         # With sub : seems like a sheet
# plot_all_sub(731)        # ??
# plot_all_sub(528)         # With sub : seems at a node but with offset
# plot_all_sub(602)         # With sub : seems at a node but with offset
# plot_all_sub(480)
# plot_all_sub(510)

plot_all_sub(602)

# plot_all_sub(311)



cv.show()
