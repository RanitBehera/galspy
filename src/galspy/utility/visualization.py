import numpy
import matplotlib.pyplot as plt



class CubeVisualizer:
    def __init__(self,ax:plt.Axes=None) -> None:
        if ax==None:
            ax=plt.axes(projection="3d")
        if not ax.name=="3d": raise Exception("ERROR : Axes type is not 3d")
        
        self.axis3d = ax
        self.points_bank = []
        
        self.viewangle()

        self._need_bound_update=True

    def add_points(self,pos:list[list[float]],points_size=1,points_color='k',points_alpha=1):
        self.points_bank.append({
            "POSITION"  : pos,
            "SIZE"      : points_size,
            "COLOR"     : points_color,
            "ALPHA"     : points_alpha
        })
        self._need_bound_update = True
    

    def update_axis_range(self):
        if not self._need_bound_update: return
        all_pos = numpy.concatenate([point_dict["POSITION"] for point_dict in self.points_bank])
        ox,oy,oz = numpy.min(all_pos.T,axis=1)
        sx,sy,sz = numpy.max(all_pos.T,axis=1)
        self.origin = numpy.array([ox,oy,oz])
        self.bound = numpy.array([sx,sy,sz])
        self._need_bound_update = False

    def get_axis_origin(self):
        self.update_axis_range()
        return self.origin
    
    def get_axis_bound(self):
        self.update_axis_range()
        return self.bound
    
    def get_axis_span(self):
        return self.bound - self.origin

    def beautify_axis(self):
        ax=self.axis3d
        self.update_axis_range()
        OX,OY,OZ = self.origin
        LX,LY,LZ = self.bound

        # Set Label
        ax.set_xlabel("X",fontsize=18)
        ax.set_ylabel("Y",fontsize=18)
        ax.set_zlabel("Z",fontsize=18)
        
        # Limit Axis Range
        ax.set_xlim3d(OX,LX);ax.set_ylim3d(OY,LY);ax.set_zlim3d(OZ,LZ)
        
        # Hide Axis Ticks
        ax.set_xticks([]);ax.set_yticks([]);ax.set_zticks([])
        
        # Hide Axis
        # ax.set_axis_off()

        # Hide Background Grid
        ax.grid(False)
        
        # Set BG Plane Transparent
        ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        
        # Draw Cube Edge
        alp=1
        ax_cx=numpy.array([OX,LX,LX,OX,OX,OX,LX,LX,OX,OX])
        ax_cy=numpy.array([OY,OY,LY,LY,OY,OY,OY,LY,LY,OY])
        ax_cz=numpy.array([OZ,OZ,OZ,OZ,OZ,LZ,LZ,LZ,LZ,LZ])
        ax.plot(ax_cx,ax_cy,ax_cz,'k-',alpha=alp,lw=1)
        ax.plot([LX,LX],[OY,OY],[OZ,LZ],'k-',alpha=alp,lw=1)
        ax.plot([OX,OX],[LY,LY],[OZ,LZ],'k-',alpha=alp,lw=1)
        ax.plot([LX,LX],[LY,LY],[OZ,LZ],'k-',alpha=alp,lw=1)
    
        # Set equal aspect
        ax.set_aspect('equal', adjustable='box')
        # ax.tight_layout()
    
    def viewangle(self,elv=20,azim=40+35):
        self.axis3d.view_init(elv,azim)

    def plot(self):
        for points_dict in self.points_bank:
            x,y,z=numpy.transpose(points_dict["POSITION"])
            sz=points_dict["SIZE"]
            pc=points_dict["COLOR"]
            al=points_dict["ALPHA"]
            self.axis3d.scatter(x,y,z,s=sz,color=pc,ec='none',alpha=al)
        return self.axis3d

    def show(self):
        self.beautify_axis()
        self.plot()
        plt.show()
