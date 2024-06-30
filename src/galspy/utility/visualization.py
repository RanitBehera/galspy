import numpy
import matplotlib.pyplot as plt

def CubeVisualizer(ax:plt.Axes,pos:list[list[float]],box_size,point_size,point_color,alpha=1):    
    # Validation
    if not ax.name=="3d": raise Exception("ERROR : Axes type is not 3d")
    if box_size==0:raise Exception("ERROR : Box Size=0.")
    L=box_size

    #------------------------------------------------------------
    x,y,z=numpy.transpose(pos)
    ax.scatter(x,y,z,s=point_size,color=point_color,ec='none',alpha=alpha)
    # ax.plot(x,y,z)

    #------------------------------------------------------------

    # --- BEAUTIFY
    # Limit Range
    # ax.set_xlim(0,L);ax.set_ylim(0,L);ax.set_zlim(0,L)
    #Hide axis ticks
    ax.set_axis_off()
    ax.set_xticks([]);ax.set_yticks([]);ax.set_zticks([])
    # Hide BG Grid
    ax.grid(False)
    # BG plane transparent
    ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    # Draw Sim Cube
    if True:
        alp=1
        ax_cx=numpy.array([0,1,1,0,0,0,0,1,1,0,0])*L
        ax_cy=numpy.array([0,0,1,1,0,0,0,0,1,1,0])*L
        ax_cz=numpy.array([0,0,0,0,0,1,1,1,1,1,1])*L
        ax.plot(ax_cx,ax_cy,ax_cz,'k-',alpha=alp,lw=1)
        ax.plot([L,L],[0,0],[0,L],'k-',alpha=alp,lw=1)
        ax.plot([L,L],[L,L],[0,L],'k-',alpha=alp,lw=1)
        ax.plot([0,0],[L,L],[0,L],'k-',alpha=alp,lw=1)

    # plt.tight_layout()
    #Rotate view(elev,azim)
    ax.view_init(20,40+35)
    ax.axis("equal")