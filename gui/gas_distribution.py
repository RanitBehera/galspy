import galspy as gs
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.widgets import LassoSelector
from galspy.Utility.Visualization import Cube3D
from matplotlib.collections import PathCollection


SIM=gs.NavigationRoot(gs.NINJA.L150N2040_WIND_WEAK)
PIG=SIM.PIG(z=7.0)

class SelectFromCollection:
    def __init__(self, ax_ps:plt.Axes, ax_c3d:plt.Axes=None):
        self.ax_ps = ax_ps
        self.col_ps = ax_ps.collections[0]
        self.fc_ps = self.col_ps.get_facecolors()
        self.xys_ps = self.col_ps.get_offsets()

        self.ACTIVE_COLOR=(1,0,0)
        self.INACTIVE_COLOR=(0.8,0.8,0.8)

        
        if len(self.fc_ps) == 0:
            raise ValueError('Collection must have a facecolor')
        elif len(self.fc_ps) == 1:
            self.fc_ps = np.tile(self.fc_ps, (len(self.xys_ps), 1))


        self.ax_c3d=ax_c3d
        if self.ax_c3d is not None:
            self.col_c3d = [col for col in ax_c3d.collections if isinstance(col,PathCollection)][0]
            self.fc_c3d = self.col_c3d.get_facecolors()
            self.xyzs_c3d = self.col_c3d.get_offsets()
        
            if len(self.fc_c3d) == 0:
                raise ValueError('Collection must have a facecolor')
            elif len(self.fc_c3d) == 1:
                self.fc_c3d = np.tile(self.fc_c3d, (len(self.xyzs_c3d), 1))




        LINE_PROP={'c':'k','ls':'--','lw':1}
        self.lasso = LassoSelector(ax_ps, onselect=self.onselect,props=LINE_PROP)
        self.ind = []

    def onselect(self, verts):
        path = Path(verts)
        self.ind = np.nonzero(path.contains_points(self.xys_ps))[0]
        # ----
        self.fc_ps[:, :-1] = self.INACTIVE_COLOR
        self.fc_ps[self.ind, :-1] = self.ACTIVE_COLOR
        self.col_ps.set_facecolor(self.fc_ps)
        
        if self.ax_c3d is not None:
            self.fc_c3d[:, :-1] = self.INACTIVE_COLOR
            self.fc_c3d[self.ind, :-1] = self.ACTIVE_COLOR
            self.col_c3d.set_edgecolor(self.fc_c3d)

            ms_c3d = np.ones(len(self.xyzs_c3d))
            ms_c3d[self.ind] = 2
            self.col_c3d.set_sizes(ms_c3d)


        self.ax_ps.figure.canvas.draw_idle()
        if self.ax_c3d is not None:
            self.ax_c3d.figure.canvas.draw_idle()
        
        

    def disconnect(self):
        self.lasso.disconnect_events()
        self.fc_ps[:, :-1] = (1,0,0)
        self.col_ps.set_facecolors(self.fc_ps)

        if self.ax_c3d is not None:
            self.fc_c3d[:, :-1] = (1,0,0)
            self.col_c3d.set_facecolors(self.fc_c3d)
        
        
        self.ax_ps.figure.canvas.draw_idle()
        
        if self.ax_c3d is not None:
            self.ax_c3d.figure.canvas.draw_idle()


print("READING","-"*32)
gid = PIG.Gas.GroupID()
rho = PIG.Gas.Density()
ie = PIG.Gas.InternalEnergy()
nebynh = PIG.Gas.ElectronAbundance()
vel = PIG.Gas.Velocity()

gid_star =PIG.Star.GroupID()
gid_bh = PIG.BlackHole.GroupID()
pos_star = PIG.Star.Position()
pos_bh = PIG.BlackHole.Position()

UNITS=PIG.Header.Units

def Target(tgid):
    tmask = gid==tgid
    trho = rho[tmask]
    tie = ie[tmask]
    tnebynh = nebynh[tmask]
    tvel = vel[tmask] 
    dens,temp = PIG.Gas.GetDensityAndTemperature(trho,tie,tnebynh,UNITS)

    tpos = PIG.Gas.Position()[tmask]

    tpos_star = pos_star[gid_star==tgid]
    tpos_bh = pos_bh[gid_bh==tgid]

    # --------------
    c3d = Cube3D()
    c3d.add_points(tpos,points_size=1,points_color='r')
    # c3d.add_points(tpos_star,points_size=4,points_color='c',points_marker='*')
    # c3d.add_points(tpos_bh,points_size=1000,points_color='k',points_marker='+')
    ax_c3d=c3d.show(False)

    # --------------
    plt.figure("Phase Space")
    plt.scatter(dens/1e-24,temp,s=1,c='r')
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Comoving Number Density (cm-3)")
    plt.ylabel("Temperature (K)")
    ax_ps=plt.gca()
    fig=plt.gcf()
    selector = SelectFromCollection(ax_ps,ax_c3d)

    plt.show()

print("Enter GID else 'q' to exit.")

T=input("TGID = ")
while T.lower() not in ['q']:
    Target(int(T))
    T=input("TGID = ")

