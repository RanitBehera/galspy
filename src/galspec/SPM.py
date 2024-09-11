import galspy
from galspy.utility.visualization import CubeVisualizer
import numpy
import matplotlib.pyplot as plt
from typing import Literal
from mpl_toolkits.axes_grid1 import make_axes_locatable

from astropy.cosmology import FlatLambdaCDM
cosmo = FlatLambdaCDM(H0=67.36, Om0=0.3153)


class SpectroPhotoMetry:
    def __init__(self,snaps_path, snap_num):
        self.SnapPath = snaps_path
        self.SnapNum  = snap_num
        SNAPDIR = galspy.NavigationRoot(self.SnapPath)
        self._PART = SNAPDIR.PART(snap_num)
        self._PIG  = SNAPDIR.PIG(snap_num)


    # =========================
    # ===== TARGET REGION =====
    # =========================
    def target_region(self,x,y,z,size):
        # size in kpc
        self._target_location = [x,y,z]
        self._target_size = size
        self.gather_stars_in_region()

    def target_PIG_Group(self,pig_groupid,span_multiplier=1):
        location = self._PIG.FOFGroups.MassCenterPosition()[pig_groupid]     
        pig_stars_pos = self._PIG.Star.Position()
        pig_stars_gid = self._PIG.Star.GroupID()
        target_group_mask = (pig_stars_gid==pig_groupid)
        target_group_star_pos = pig_stars_pos[target_group_mask]
        target_group_span_x = numpy.max(target_group_star_pos[:,0]) - numpy.min(target_group_star_pos[:,0])
        target_group_span_y = numpy.max(target_group_star_pos[:,1]) - numpy.min(target_group_star_pos[:,1])
        target_group_span_z = numpy.max(target_group_star_pos[:,2]) - numpy.min(target_group_star_pos[:,2])
        target_group_span   = max([target_group_span_x,target_group_span_y,target_group_span_z])
        size = span_multiplier * target_group_span
        # print(size)
        self.target_region(*location,size)

    def gather_stars_in_region(self):
        part_star_pos = self._PART.Star.Position()
        mask_x = ((self._target_location[0] - (self._target_size/2)) <= part_star_pos[:,0]) & (part_star_pos[:,0] <=(self._target_location[0] + (self._target_size/2)))
        mask_y = ((self._target_location[1] - (self._target_size/2)) <= part_star_pos[:,1]) & (part_star_pos[:,1] <=(self._target_location[1] + (self._target_size/2)))
        mask_z = ((self._target_location[2] - (self._target_size/2)) <= part_star_pos[:,2]) & (part_star_pos[:,2] <=(self._target_location[2] + (self._target_size/2)))
        mask = mask_x & mask_y & mask_z
        
        self.target_star_pos    = part_star_pos[mask] - self._target_location
        self.target_star_mass   = self._PART.Star.Mass()[mask]

        snapshot_scale_factor        = self._PART.Header.Time()
        star_formation_scale_factor = self._PART.Star.StarFormationTime()[mask]

        snapshot_redshift        = (1/snapshot_scale_factor) -1
        star_formation_redshift = (1/star_formation_scale_factor) -1

        snapshot_lookback_time = cosmo.lookback_time(snapshot_redshift)

        print(snapshot_lookback_time)
        # self.target_star_age    = 


    def show_region(self):
        cv=CubeVisualizer()
        cv.add_points(self.target_star_pos,points_size=5,points_color='r',points_alpha=1)
        cv.beautify_axis()
        ax=cv.plot()
        ax.set_xlim(-self._target_size/2,self._target_size/2)
        ax.set_ylim(-self._target_size/2,self._target_size/2)
        ax.set_zlim(-self._target_size/2,self._target_size/2)
        plt.show()

    def projection_plane_orientation(self,theta=0,phi=0):
        self.proj_plane_theta=theta
        self.proj_plane_phi=phi
        # TODO : Project to (U,V) coordinate
        self._Up=self.target_star_pos[:,1]
        self._Vp=self.target_star_pos[:,2]
    

    def show_projected_points(self):
        plt.plot(self._Up,self._Vp,'.r',ms=5)
        plt.axis('equal')
        plt.show()

    def interpolate_mass_to_grid(self,grid_resolution:tuple,mode=Literal["NGB","CIC"]):
        assert mode in ["NGB", "CIC"]
        if mode=="NGB":
            grid_deltaX=self._target_size/(grid_resolution[0]-1)
            grid_deltaY=self._target_size/(grid_resolution[1]-1)
            
            grid_UV = numpy.zeros(grid_resolution)

            tmass=self.target_star_mass
            tUp=self._Up+(self._target_size/2)
            tVp=self._Vp+(self._target_size/2)

            for m,up,vp in zip(tmass,tUp,tVp):
                ind_u = int((up/grid_deltaX)+0.5)
                ind_v = int((vp/grid_deltaY)+0.5)
                grid_UV[ind_u,ind_v] += m
            
            MASS_UNIT=1e10  #<---- Hard coded
            self.interpolated_mass_grid=grid_UV*MASS_UNIT

            # print(self.interpolated_mass_grid)
        elif mode=="CIC":
            raise NotImplementedError()
        
    
    def show_interpolated_mass_grid_image(self):
        img=plt.imshow(self.interpolated_mass_grid.T,cmap='grey')
        plt.colorbar(img)
        plt.show()

    def show_age_distribution(self):
        fig,axes = plt.subplots(1,2,figsize=(10, 5))
        ax1,ax2 = axes
        img=ax1.imshow(self.interpolated_mass_grid.T,cmap='grey')

        divider = make_axes_locatable(ax1)
        cax = divider.append_axes("right", size="5%", pad=0.1)
        cbar = fig.colorbar(img,cax=cax)

        def onclick(event):
            ix, iy = round(event.xdata), round(event.ydata)

            print (f'x = {ix}, y = {iy}')


        fig.canvas.mpl_connect('button_press_event', onclick)
        plt.show()
