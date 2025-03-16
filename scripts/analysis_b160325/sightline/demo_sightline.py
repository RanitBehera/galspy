import galspy.MPGadget as mp
import matplotlib.pyplot as plt
from galspy.utility.visualization import CubeVisualizer
import numpy as np
from scipy import spatial
import pickle
import galspy.utility.sightline as sl

# SIM = mp.NavigationRoot("/mnt/home/student/cranit/Data/MP_Gadget/Nishi/L10N64/output")
SIM = mp.NavigationRoot("/mnt/home/student/cranit/Data/MP_Gadget/Nishi/L50N640")
SNAP = 36
BOX_SIZE = SIM.PART(SNAP).Header()["BoxSize"]

# print(SIM.PIG(SNAP).FOFGroups.MassCenterPosition()[0]/BOX_SIZE)


if False:
    gas_pos = SIM.PART(SNAP).Gas.Position()
    print("Building kd-Tree...",end="",flush=True)
    kdt = spatial.cKDTree(gas_pos)
    print("Done",flush=True)

    print("Saving Pickle...",end="",flush=True)
    with open("/mnt/home/student/cranit/Repo/galspy/scripts/temp/outs/L10N64S17.ckdtree","wb") as fp:
    # with open("/mnt/home/student/cranit/Repo/galspy/scripts/temp/outs/L50N640S36.ckdtree","wb") as fp:
        pickle.dump(kdt,fp)
else:
    SLIDE = 3
    
    fig = plt.figure()
    ax = fig.add_subplot(111,projection='3d')
    # ax1 = fig.add_subplot(121,projection='3d')
    # ax2 = fig.add_subplot(122,projection='3d')


    if SLIDE==1: # The Box
        gas_pos = SIM.PART(SNAP).Gas.Position()
        cv=CubeVisualizer(ax)
        cv.add_points(gas_pos)
        cv.beautify_axis()
        cv.show()
    elif SLIDE==2: # Sightline through Box
        gas_pos = SIM.PIG(SNAP).Gas.Position()
        cv=CubeVisualizer(ax)
        cv.add_points(gas_pos)
        START       = np.array([0.5,0,0.5])*BOX_SIZE
        END         = np.array([0.5,1,0.5])*BOX_SIZE
        SX,SY,SZ    = np.array([START,END]).T
        ax.plot(SX,SY,SZ,'r',lw=2)
        ax.plot(0,0,0,'m.',ms=20)
        cv.show()
    elif SLIDE == 3:    # kd-tree nn cylinder
        # with open("/mnt/home/student/cranit/Repo/galspy/temp/outs/L10N64S17.ckdtree","rb") as fp:
        with open("/mnt/home/student/cranit/Repo/galspy/temp/outs/L50N640S36.ckdtree","rb") as fp:
            kdt = pickle.load(fp)

        # origin = np.array((0.621,0.547,0.193))*BOX_SIZE
        origin = np.array((0.181,0.600,0.684))*BOX_SIZE

        thetas = np.array([0,0.25,0.5,0.75,1])*np.pi
        phis   = np.array([0,0.25,0.5,0.75,1,1.25,1.5,1.75])*np.pi


        sightlines = []
        for th in thetas:
            for ph in phis:
                sightlines.append(sl.AngularSightline(origin,th,ph,BOX_SIZE))

        SMOOTHING_LENGTH = 200 # kpc 
        
        ind_within_cyl_of_infl = []
        for sight in sightlines:
            STOPS = sight.Get_CartesianSightline().Get_Steps(100)
            for i,stop in enumerate(STOPS):
                neighbours_index=kdt.query_ball_point(stop,2*SMOOTHING_LENGTH)
                ind_within_cyl_of_infl += neighbours_index

        ind_within_cyl_of_infl = list(set(ind_within_cyl_of_infl))
        
        pos_in_cyl = kdt.data[ind_within_cyl_of_infl]
        
        cv=CubeVisualizer(ax)
        cv.add_points(pos_in_cyl)
        cv.show()



