import galspy.MPGadget as mp
import galspy.utility.HaloQuery as rs
import galspy.utility.visualization as vis
import matplotlib.pyplot as plt
import galspy.IO.BigFile as bf

import os,numpy

OUTBASE = "/mnt/home/student/cranit/Work/test_para_rock/L10N64"
SNAP = 17
root = mp.NavigationRoot(OUTBASE)
qr = rs.RSGQuery(root.RSG(SNAP).path)

ax = plt.axes(projection="3d")
cv = vis.CubeVisualizer(ax)
BLOBNAME = "000006"



def plot_all_sub(ihid,clr='r',with_child=False):
    if not with_child:
        pos = qr.get_child_particle_positions([ihid],BLOBNAME)
        cv.add_points(pos,2,clr,1)
    else:
        all_sub = qr.get_descendant_halos_of(ihid,BLOBNAME)
        all_sub = numpy.array(list(all_sub)+[ihid])
        valid = qr.check_if_valid_sub(all_sub,BLOBNAME)
        for sub,v in zip(all_sub,valid):
            if v:
                c = clr
                a = 1
            else:
                c= 'k'
                a = 0.1
            cv.add_points(qr.get_child_particle_positions([sub],BLOBNAME),2,c,0.1)

    
    
    cpos = qr.get_centre_position([ihid],BLOBNAME)
    cv.add_points(cpos,5,'k')
    cv.add_text(cpos[0],str(ihid),'k')
    
    vrad = qr.get_virial_radius([ihid],BLOBNAME)
    cv.add_sphere_wire(cpos[0],vrad/1000,'k')

    print(vrad)

    # po = qr.get_vmax_r([ihid],BLOBNAME)
    # cv.add_sphere_wire(cpos[0],po,'r')
    

# L50N640 - HID 8
#region
# plot_all_sub(461,'b')
# plot_all_sub(688)
# plot_all_sub(480,'r')
# plot_all_sub(510,'g')
# plot_all_sub(461)
# plot_all_sub(473)
# plot_all_sub(519)
# plot_all_sub(596)       # With sub : seems like a sheet
# plot_all_sub(549)         # With sub : seems like a sheet
# plot_all_sub(731)        # ??
# plot_all_sub(528)         # With sub : seems at a node but with offset
# plot_all_sub(602)         # With sub : seems at a node but with offset
# plot_all_sub(480)
# plot_all_sub(510)
# plot_all_sub(602)
# plot_all_sub(761)
#endregion

# L10N64S17
#region HID 172
# plot_all_sub(27)
# plot_all_sub(18,'b')
# plot_all_sub(19,'y')
# plot_all_sub(26,'m')
# plot_all_sub(28,'g')
# plot_all_sub(28,'g')
# plot_all_sub(30,'r')
# plot_all_sub(31,'r')
# plot_all_sub(1,'y')
# plot_all_sub(11,'b')
#endregion

#region HID 250
plot_all_sub(16)      #DM Halo
# plot_all_sub(31,'y')  #Gas Halo, but no HID??
# plot_all_sub(32,'m')  #Galaxy 1
# plot_all_sub(33,'g')  #Galaxy 2
#endregion

#region HID 2
# plot_all_sub(7)
# plot_all_sub(10)
# plot_all_sub(9)
# plot_all_sub(11,'m')
# plot_all_sub(14,'b')
# plot_all_sub(3)
#endregion




cv.show()
