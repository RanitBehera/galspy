import numpy
import matplotlib.pyplot as plt
from typing import Literal


_BOX_MODE = Literal["AxisWise","MaxAxis"]

class CubeVisualizer:
    def __init__(self,ax:plt.Axes=None,spanmode:_BOX_MODE="MaxAxis") -> None:
        if ax==None:
            ax=plt.axes(projection="3d")
        if not ax.name=="3d": raise Exception("ERROR : Axes type is not 3d")
        
        self.axis3d = ax
        self.points_bank = []
        self.text_bank = []
        self.sphere_wire_bank =[]
        
        self.spanmode:_BOX_MODE=spanmode

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
    
    def add_text(self,pos:list[list[float]],text:str,clr:str):
        self.text_bank.append({"POS":pos,"TEXT":text,"CLR":clr})


    def add_sphere_wire(self,center_pos:list[float],radius:float,wireclr:str):
        self.sphere_wire_bank.append({"CENTER":center_pos,"RADIUS":radius,"WIRECLR":wireclr})


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

    def get_axis(self):
        return self.axis3d


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
        if self.spanmode == "AxisWise":
            pass
        elif self.spanmode == "MaxAxis":
            SX = LX - OX
            SY = LY - OY
            SZ = LZ - OZ

            MaxSpan = max([SX,SY,SZ])
            
            CX = OX + SX/2
            CY = OY + SY/2
            CZ = OZ + SZ/2

            OX = CX - MaxSpan/2
            LX = CX + MaxSpan/2
            OY = CY - MaxSpan/2
            LY = CY + MaxSpan/2
            OZ = CZ - MaxSpan/2
            LZ = CZ + MaxSpan/2
        else:
            pass

        ax.set_xlim3d(OX,LX);ax.set_ylim3d(OY,LY);ax.set_zlim3d(OZ,LZ)

        # Hide Axis Ticks
        # ax.set_xticks([]);ax.set_yticks([]);ax.set_zticks([])
        
        # Hide Axis
        # ax.set_axis_off()

        # Hide Background Grid
        ax.grid(False)
        
        # Set BG Plane Transparent
        ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
        
        # Draw Cube Edge
        if True:
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
        # ax.set_aspect('equal', adjustable='datalim')
        # ax.tight_layout()

    def draw_annotate(self):
        ax = self.axis3d
        for text in self.text_bank:
            X,Y,Z = text["POS"]
            ax.text(X,Y,Z,text["TEXT"],size=16,zorder=100,color=text["CLR"])
    
    def draw_wire(self):
        ax=self.axis3d
        for sphere in self.sphere_wire_bank:
            r=sphere["RADIUS"]
            ox,oy,oz = sphere["CENTER"]
            u, v = numpy.mgrid[0:2*numpy.pi:20j, 0:numpy.pi:10j]
            x = r*numpy.cos(u)*numpy.sin(v)
            y = r*numpy.sin(u)*numpy.sin(v)
            z = r*numpy.cos(v)
            ax.plot_wireframe(ox+x, oy+y, oz+z, color=sphere["WIRECLR"],lw=0.5)

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
        self.draw_annotate()
        self.draw_wire()
        plt.show()
