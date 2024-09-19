import galspy
from galspy.utility.visualization import CubeVisualizer
import numpy
import matplotlib.pyplot as plt
from typing import Literal
from mpl_toolkits.axes_grid1 import make_axes_locatable
import galspec.bpass as bp

from astropy.cosmology import FlatLambdaCDM
cosmo = FlatLambdaCDM(H0=67.36, Om0=0.3153)

BPASS = bp.BPASS("CHABRIER_UPTO_300M","Binary",0.02)
waves=[5e2,5e4]
FLUX=BPASS.Spectra.GetFlux(waves[0],waves[-1])


class SpectroPhotoMetry:
    def __init__(self,snaps_path, snap_num):
        self.SnapPath = snaps_path
        self.SnapNum  = snap_num
        SNAPDIR = galspy.NavigationRoot(self.SnapPath)
        self._PART = SNAPDIR.PART(snap_num)
        self._PIG  = SNAPDIR.PIG(snap_num)

        self.contrast_exponent=1

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
        # location += numpy.array([-30,0,-20])
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

        snapshot_lookback_time = cosmo.lookback_time(snapshot_redshift).value
        star_formation_lookback_time = cosmo.lookback_time(star_formation_redshift).value
        self.target_star_age_in_Myr = (star_formation_lookback_time - snapshot_lookback_time)*1000

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
        self._Up=self.target_star_pos[:,0]
        self._Vp=self.target_star_pos[:,2]
    

    def show_projected_points(self):
        plt.plot(self._Up,self._Vp,'.r',ms=5,alpha=0.3)
        plt.axis('equal')
        plt.show()

    def generate_grid(self,grid_resolution:tuple,mode=Literal["NGB","CIC"]):
        assert mode in ["NGB", "CIC"]
        grid_deltaX=self._target_size/(grid_resolution[0]-1)
        grid_deltaY=self._target_size/(grid_resolution[1]-1)

        grid_mass = numpy.zeros(grid_resolution)
        grid_age = numpy.empty(grid_resolution, dtype=object)
        for i in range(grid_resolution[0]):
            for j in range(grid_resolution[1]):
                grid_age[i, j] = []
        
        if mode=="NGB":    
            tmass=self.target_star_mass
            tUp=self._Up+(self._target_size/2)
            tVp=self._Vp+(self._target_size/2)
            tage=self.target_star_age_in_Myr
            for m,up,vp,ta in zip(tmass,tUp,tVp,tage):
                ind_u = int((up/grid_deltaX)+0.5)
                ind_v = int((vp/grid_deltaY)+0.5)
                grid_mass[ind_u,ind_v] += m
                grid_age[ind_u,ind_v].append(ta)
            
            MASS_UNIT=1e10  #<---- Hard coded
            self.grid_mass_interpolated=(grid_mass)*MASS_UNIT
            self.grid_age_distributed = grid_age



            # print(self.grid_mass_interpolated)
        elif mode=="CIC":
            raise NotImplementedError()
        
    
    def show_interpolated_mass_grid_image(self):

        img=plt.imshow(self.grid_mass_interpolated.T**self.contrast_exponent,cmap='grey',origin='lower')
        plt.colorbar(img,label="$M_\odot$")
        plt.xlabel("kpc")
        plt.ylabel("kpc")
        plt.show()

    def show_age_distribution(self):
        fig,axes = plt.subplots(1,2,figsize=(10, 5))
        ax1,ax2 = axes
        img=ax1.imshow(self.grid_mass_interpolated.T**self.contrast_exponent,cmap='grey',origin='lower')

        divider = make_axes_locatable(ax1)
        cax = divider.append_axes("right", size="5%", pad=0.1)
        cbar = fig.colorbar(img,cax=cax,label="$M_\odot$")

        # ax1.set_xlabel("kpc")
        # ax1.set_ylabel("kpc")

        def ShowHistogramForAges(ages):
            log10_ages=numpy.log10(ages)+6
            ax2.hist(log10_ages,bins=numpy.arange(6,10,0.1))
            ax2.set_xlabel("Myr")
            ax2.set_ylabel("count")


        def onclick(event):
            ix, iy = round(event.xdata), round(event.ydata)
            ages = self.grid_age_distributed[ix,iy]
            ax2.clear()
            ShowHistogramForAges(ages)
            fig.canvas.draw()


        fig.canvas.mpl_connect('button_press_event', onclick)
        plt.show()


    def show_spectra(self):
        fig,axes = plt.subplots(1,2,figsize=(10, 5))
        ax1,ax2 = axes
        img=ax1.imshow(self.grid_mass_interpolated.T**self.contrast_exponent,cmap='grey',origin='lower')

        divider = make_axes_locatable(ax1)
        cax = divider.append_axes("right", size="5%", pad=0.1)
        cbar = fig.colorbar(img,cax=cax,label="$M_\odot$")

        # ax1.set_xlabel("kpc")
        # ax1.set_ylabel("kpc")

        def ShowPixelSpectra(ages,mass):
            log10_ages=numpy.log10(ages)+6
            bin_counts,age_bins=numpy.histogram(log10_ages,bins=numpy.arange(6,10,0.1))
            

            total_flux=0*FLUX.WL
            for a,c in zip(age_bins,bin_counts):
                if c==0:continue
                aflux=FLUX[str(numpy.round(a,1))]
                total_flux+=aflux

                # ax2.plot(FLUX.WL,aflux,'--')

            ax2.plot(FLUX.WL,total_flux,'k')
            ax2.set_yscale('log')
            ax2.set_xscale('log')



        def onclick(event):
            ix, iy = round(event.xdata), round(event.ydata)
            ages = self.grid_age_distributed[ix,iy]
            proj_mass = self.grid_mass_interpolated[ix,iy]
            ax2.clear()
            ShowPixelSpectra(ages,proj_mass)
            fig.canvas.draw()


        fig.canvas.mpl_connect('button_press_event', onclick)
        plt.show()
