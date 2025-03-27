import galspy
from galspy.utility.visualization import CubeVisualizer
import numpy as np
import matplotlib.pyplot as plt

SNAPSPATH = "/mnt/home/student/cranit/NINJA/simulations/L150N2040/SNAPS/"
root = galspy.NavigationRoot(SNAPSPATH)
PIG = root.PIG(43)


star_pos_all    = PIG.Star.Position()
star_gid_all    = PIG.Star.GroupID()
star_gen_all    = PIG.Star.Generation()
star_bt_all     = PIG.Star.StarFormationTime()
star_sml_all    = PIG.Star.SmoothingLength()


def DoForGID(tid):
    # tid = 1
    mask = star_gid_all==tid

    star_pos=star_pos_all[mask]
    star_gid=star_gid_all[mask]
    star_gen=star_gen_all[mask] 
    star_bt=star_bt_all[mask]
    star_sml=star_sml_all[mask]

    lnp=len(star_pos)
    print(lnp)

    unq_gens,count = np.unique(star_gen,return_counts=True)
    for u,c in zip(unq_gens,count):
        print(u,":",c)



    # ====================================================================

    fig = plt.figure(figsize=(18,8))
    ax1_3d = fig.add_subplot(1,3,1,projection='3d')
    ax2_3d = fig.add_subplot(1,3,2,projection='3d')
    ax3_3d = fig.add_subplot(1,3,3,projection='3d')




    cv1=CubeVisualizer(ax1_3d)
    cv2=CubeVisualizer(ax2_3d)
    cv3=CubeVisualizer(ax3_3d)

    cv1.add_points(star_pos,points_color='k',points_size=1,points_alpha=0.5)
    cv1.show(False)



    apts = cv1.get_anchor_points()
    cv2.add_points(apts,points_alpha=0)
    cv3.add_points(apts,points_alpha=0)


    # GENERATIONS
    def ShowGen(gen):
        gen_mask=(star_gen==gen)
        gen_pos = star_pos[gen_mask]
        cv2.add_points(gen_pos)
        ax:plt.Axes=cv2.show(False)
        ax.set_title(f"Gen {gen}")

    ShowGen(5)


    # BT or SML
    para=star_sml
    para_sort = np.argsort(para)
    star_pos_sorted = star_pos[para_sort]

    cv3.add_points(star_pos_sorted[:int(0.95*lnp)])
    cv3.show(False)

    plt.figure()
    bc,be=np.histogram(np.log10(star_sml),bins=100)
    br=(be[:-1]+be[1:])/2
    plt.plot(br,np.log10(bc))
    
    plt.show()


for i in range(4,5):
    print(i,'-'*40)
    DoForGID(i)







