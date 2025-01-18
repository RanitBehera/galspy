import numpy
import matplotlib.pyplot as plt
from typing import Literal
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d





# Taken from https://stackoverflow.com/questions/11140163/plotting-a-3d-cube-a-sphere-and-a-vector
# Corrected from https://github.com/matplotlib/matplotlib/issues/21688
class Arrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        super().__init__( (0, 0), (0, 0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def do_3d_projection(self, renderer=None):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, self.axes.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))

        return numpy.min(zs)

# If O(x,y,z) to A(l,m,n), pass as Arrow3D([x,l],[y,m],[z,n])
# a = Arrow3D([0, 1], [0, 1], [0, 1], mutation_scale=20,lw=1, arrowstyle="-|>", color="k")
# ax.add_artist(a)








_BOX_MODE = Literal["AxisWise","MaxAxis","FixedAxis"]

class CubeVisualizer:
    def __init__(self,ax:plt.Axes=None,spanmode:_BOX_MODE="MaxAxis") -> None:
        if ax==None:
            ax=plt.axes(projection="3d")
        if not ax.name=="3d": 
            raise Exception("ERROR : Axes type is not 3d")
        
        self.axis3d = ax
        self._points_bank = []
        self._text_bank = []
        self._sphere_wire_bank =[]
        self._arrow_bank = []
        
        self.spanmode:_BOX_MODE=spanmode

        self.viewangle()

        self._need_bound_update=True

    def add_points(self,pos:list[list[float]],points_size=1,points_color=None,points_alpha=1,points_marker='.'):
        if len(pos)==0:return
        self._points_bank.append({
            "POSITION"  : pos,
            "SIZE"      : points_size,
            "COLOR"     : points_color,
            "ALPHA"     : points_alpha,
            "MARKER"    : points_marker
        })
        self._need_bound_update = True
    
    def add_text(self,pos:list[list[float]],text:str,clr:str="k"):
        self._text_bank.append({"POS":pos,"TEXT":text,"CLR":clr})


    def add_sphere_wire(self,center_pos:list[float],radius:float,wireclr:str):
        self._sphere_wire_bank.append({"CENTER":center_pos,"RADIUS":radius,"WIRECLR":wireclr})

    def add_arrow(self,vector:list[float],origin:list[float]=[0,0,0],arrow_clr:str='k',arrow_width:int=1):
        self._arrow_bank.append({"FROM":origin,"TO":vector,"CLR":arrow_clr,"WIDTH":arrow_width})

    def update_axis_range(self):
        if not self._need_bound_update: return
        # TODO: fails if we draw only arrows and there are no points
        all_pos = numpy.concatenate([point_dict["POSITION"] for point_dict in self._points_bank])
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

    def get_axis_anchors(self):
        self.update_axis_range()
        
        OX,OY,OZ = self.origin
        LX,LY,LZ = self.bound

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

        return OX,LX,OY,LY,OZ,LZ

    def get_anchor_points(self):
        ox,lx,oy,ly,oz,lz = self.get_axis_anchors()
        pts_zl=(0.5*(ox+lx),0.5*(oy+ly),oz)
        pts_zu=(0.5*(ox+lx),0.5*(oy+ly),lz)
        pts_yl=(0.5*(ox+lx),oy,0.5*(oz+lz))
        pts_yu=(0.5*(ox+lx),ly,0.5*(oz+lz))
        pts_xl=(ox,0.5*(oy+ly),0.5*(oz+lz))
        pts_xu=(lx,0.5*(oy+ly),0.5*(oz+lz))
        pts=numpy.array([pts_zl,pts_zu,pts_yl,pts_yu,pts_xl,pts_xu])
        return pts

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

        # Hide labels and ticks
        # ax.axis("off")
        # ax.set_zticks([],[])
        # ax.set_xticks([],[])
        # ax.set_yticks([],[])
        # ax.xaxis.set_tick_params(pad=-100)




    def draw_annotate(self):
        ax = self.axis3d
        for text in self._text_bank:
            X,Y,Z = text["POS"]
            ax.text(X,Y,Z,text["TEXT"],size=16,zorder=100,color=text["CLR"])
    
    def draw_wire_sphere(self):
        ax=self.axis3d
        for sphere in self._sphere_wire_bank:
            r=sphere["RADIUS"]
            ox,oy,oz = sphere["CENTER"]
            u, v = numpy.mgrid[0:2*numpy.pi:20j, 0:numpy.pi:10j]
            x = r*numpy.cos(u)*numpy.sin(v)
            y = r*numpy.sin(u)*numpy.sin(v)
            z = r*numpy.cos(v)
            ax.plot_wireframe(ox+x, oy+y, oz+z, color=sphere["WIRECLR"],lw=0.5)

    def draw_arrows(self):
        ax=self.axis3d
        for arrow in self._arrow_bank:
            origin  = arrow["FROM"]
            vector  = arrow["TO"]
            clr     = arrow["CLR"]
            width   = arrow["WIDTH"]
            a = Arrow3D(*(zip(origin,vector)), mutation_scale=4,lw=width, arrowstyle="-|>", color=clr)
            ax.add_artist(a)


    def viewangle(self,elv=20,azim=75):
        self.axis3d.view_init(elv,azim)

    def plot(self):
        for points_dict in self._points_bank:
            x,y,z=numpy.transpose(points_dict["POSITION"])
            sz=points_dict["SIZE"]
            pc=points_dict["COLOR"]
            al=points_dict["ALPHA"]
            mark=points_dict["MARKER"]
            self.axis3d.scatter(x,y,z,s=sz,color=pc,ec=None,alpha=al,marker=mark)
        return self.axis3d

    def show(self,show=True):
        self.beautify_axis()
        self.plot()
        self.draw_annotate()
        self.draw_wire_sphere()
        self.draw_arrows()
        
        if show:plt.show()
        else:return self.axis3d

