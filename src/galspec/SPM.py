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


class _SPMPixel:
    def __init__(self,row:int=0,clm:int=0) -> None:
        self.row=row
        self.column=clm
        # STAR
        self.star_bank=[]
        self.grid=numpy.zeros((50,50,1))
        self.star_mass=0
        self.star_count=0
        # BH
        self.bh_bank=[]
        self.bh_mass=0
        self.bh_count=0

    def AddStar(self,mass,age,metallicity=0.02):
        self.star_bank.append((mass,age,metallicity))
        self.star_mass+=mass
        self.star_count+=1

    def AddBlackhole(self,mass):
        self.bh_bank.append((mass))
        self.bh_mass+=mass
        self.bh_count+=1

    def generate_grid(self):
        # TODO
        for mass,age,metallicitt in self.star_bank:
            if self.star_count==0:break
            m_bid = int((numpy.log10(mass)-6)/0.1)
            if age<1:T_bid=0
            else:T_bid = int((numpy.log10(age))/0.1)
            Z_bid = 0
            self.grid[m_bid,T_bid,Z_bid] +=1


        



class SpectroPhotoMetry:
    def __init__(self,snaps_path, snap_num):
        self.SnapPath = snaps_path
        self.SnapNum  = snap_num
        SNAPDIR = galspy.NavigationRoot(self.SnapPath)
        self._PART = SNAPDIR.PART(snap_num)
        self._PIG  = SNAPDIR.PIG(snap_num)

        self.contrast_exponent=1


    def target_region(self,x,y,z,size_in_kpc):
        self._target_location   = [x,y,z]
        self._target_size       = size_in_kpc
        self.gather_particles_in_region()

    def target_PIG_Group(self,pig_groupid,zoom=1):
        location = self._PIG.FOFGroups.MassCenterPosition()[pig_groupid]   
        pig_stars_pos = self._PIG.Star.Position()
        pig_stars_gid = self._PIG.Star.GroupID()
        target_group_mask = (pig_stars_gid==pig_groupid)
        target_group_star_pos = pig_stars_pos[target_group_mask]
        target_group_span_x = numpy.max(target_group_star_pos[:,0]) - numpy.min(target_group_star_pos[:,0])
        target_group_span_y = numpy.max(target_group_star_pos[:,1]) - numpy.min(target_group_star_pos[:,1])
        target_group_span_z = numpy.max(target_group_star_pos[:,2]) - numpy.min(target_group_star_pos[:,2])
        target_group_span   = max([target_group_span_x,target_group_span_y,target_group_span_z])
        size = target_group_span / zoom
        self.target_region(*location,size) 

    def gather_particles_in_region(self):
        # region lower and upper bounds
        XLB = (self._target_location[0] - (self._target_size/2))
        XUB = (self._target_location[0] + (self._target_size/2))

        YLB = (self._target_location[1] - (self._target_size/2))
        YUB = (self._target_location[1] + (self._target_size/2))

        ZLB = (self._target_location[2] - (self._target_size/2))
        ZUB = (self._target_location[2] + (self._target_size/2))


        # Read Star Fields
        part_star_pos   = self._PART.Star.Position()
        part_star_vel   = self._PART.Star.Velocity()
        part_star_mass  = self._PART.Star.Mass()
        part_star_metallicity = self._PART.Star.Metallicity()

        # bound mask
        mask_x = (XLB<=part_star_pos[:,0]) & (part_star_pos[:,0]<=XUB)
        mask_y = (YLB<=part_star_pos[:,1]) & (part_star_pos[:,1]<=YUB)
        mask_z = (ZLB<=part_star_pos[:,2]) & (part_star_pos[:,2]<=ZUB)
        mask = mask_x & mask_y & mask_z

        # Filter for within the bounds or target region
        self.target_star_pos    = part_star_pos[mask]
        self.target_star_vel    = part_star_vel[mask]
        self.target_star_mass   = part_star_mass[mask]
        self.target_star_metallicity = part_star_metallicity[mask]

        # Star age calulation
        snapshot_scale_factor        = self._PART.Header.Time()
        star_formation_scale_factor = self._PART.Star.StarFormationTime()[mask]

        snapshot_redshift        = (1/snapshot_scale_factor) -1
        star_formation_redshift = (1/star_formation_scale_factor) -1

        snapshot_lookback_time = cosmo.lookback_time(snapshot_redshift).value
        star_formation_lookback_time = cosmo.lookback_time(star_formation_redshift).value
        self.target_star_age_in_Myr = (star_formation_lookback_time - snapshot_lookback_time)*1000


        # Read BH Fields
        part_bh_pos     = self._PART.BlackHole.Position()
        part_bh_vel     = self._PART.BlackHole.Velocity()
        part_bh_mass    = self._PART.BlackHole.BlackholeMass()
        
        # bound mask
        mask_x = (XLB<=part_bh_pos[:,0]) & (part_bh_pos[:,0]<=XUB)
        mask_y = (YLB<=part_bh_pos[:,1]) & (part_bh_pos[:,1]<=YUB)
        mask_z = (ZLB<=part_bh_pos[:,2]) & (part_bh_pos[:,2]<=ZUB)
        mask = mask_x & mask_y & mask_z

        self.target_bh_pos      = part_bh_pos[mask]
        self.target_bh_vel      = part_bh_vel[mask]
        self.target_bh_mass     = part_bh_mass[mask]


        self.shift_origin()
        self.reorient()



    def shift_origin(self):
        self.target_star_pos = self.target_star_pos - self._target_location
        self.target_bh_pos = self.target_bh_pos - self._target_location

        # self.get_angular_momentum_direction()

        # plt.hist(self.target_star_pos[:,0],bins=100,label="X",alpha=0.5)
        # plt.hist(self.target_star_pos[:,1],bins=100,label="Y",alpha=0.5)
        # plt.hist(self.target_star_pos[:,2],bins=100,label="Z",alpha=0.5)
        
        # plt.yscale('log')
        # plt.legend()
        # plt.show()        

    def reorient(self):
        # TODO matrix logic
        # self.get_angular_momentum_direction()
        pass
        
        
        
    # def get_angular_momentum_direction(self):
    #     r   = self.target_star_pos
    #     v   = self.target_star_vel - self._PIG.FOFGroups.MassCenterVelocity()[0]
    #     m   = self.target_star_mass
    #     p   = numpy.array([m[i]*v[i] for i in range(len(m))])
    #     Ji  = numpy.cross(r,p,axis=1)
    #     J   = numpy.sum(Ji.T,axis=1)
    #     self.Jhat = J/numpy.linalg.norm(J)




    def show_region(self):
        cv=CubeVisualizer()
        cv.add_points(self.target_star_pos,points_size=5,points_color='r',points_alpha=0.1)
        cv.add_points(self.target_bh_pos,points_size=20,points_color='k',points_alpha=1)
        cv.show()



    def project_to_plane(self,theta=0,phi=0):
        self.proj_plane_theta=theta
        self.proj_plane_phi=phi
        # TODO : Project to (U,V) coordinate
        self._Up_star   = self.target_star_pos[:,0]
        self._Vp_star   = self.target_star_pos[:,1]
        self._Up_bh     = self.target_bh_pos[:,0]
        self._Vp_bh     = self.target_bh_pos[:,1]
    

    def show_projected_points(self):
        plt.plot(self._Up_star,self._Vp_star,'.r',ms=5,alpha=0.3)
        plt.plot(self._Up_bh,self._Vp_bh,'+k',ms=30,alpha=1)
        plt.axis('equal')
        # ----- Bring target to center of projected plane
        span_Up = numpy.max(self._Up_star) - numpy.min(self._Up_star)
        span_Vp = numpy.max(self._Vp_star) - numpy.min(self._Vp_star)
        span = max([span_Up,span_Vp])
        plt.xlim(-span/2,span/2)
        plt.ylim(-span/2,span/2)
        plt.gca().set_adjustable("box")
        plt.axvline(0,ls='--',color='k',lw=1)
        plt.axhline(0,ls='--',color='k',lw=1)
        # -----
        plt.show()



    def generate_pixelwise_grid(self,grid_resolution:tuple,mode=Literal["NGB","CIC"]):
        assert mode in ["NGB", "CIC"]

        span_Up_star = numpy.max(self._Up_star) - numpy.min(self._Up_star)
        span_Vp_star = numpy.max(self._Vp_star) - numpy.min(self._Vp_star)

        span_Up_bh = numpy.max(self._Up_bh) - numpy.min(self._Up_bh)
        span_Vp_bh = numpy.max(self._Vp_bh) - numpy.min(self._Vp_bh)

        span = max([span_Up_star,span_Vp_star,span_Up_bh,span_Vp_bh])

        span*=1.1 # To keep everything well inside field boundary
        #TODO:Better solution to fix slight offset of index. for (50,50) index should go to 0-49. case of 50.04
        #TODO:Else add this multiplier as class variable

        grid_drow = span/grid_resolution[0]
        grid_dclm = span/grid_resolution[1] 

        left_edge = -span/2
        upper_edge = +span/2

        prow_star = numpy.int32((upper_edge - self._Vp_star)/ grid_drow)
        pclm_star = numpy.int32((self._Up_star - left_edge)/ grid_dclm)

        prow_bh = numpy.int32((upper_edge - self._Vp_bh)/ grid_drow)
        pclm_bh = numpy.int32((self._Up_bh - left_edge)/ grid_dclm)

        # print(max(prow),max(pclm))

        mass    = self.target_star_mass*1e10
        age     = self.target_star_age_in_Myr
        Z       = self.target_star_metallicity

        # Grid of pixels
        grid=numpy.empty((grid_resolution[0]+1,grid_resolution[1]+1),dtype=object)  
        for row in range(grid_resolution[0]+1):
            for clm in range(grid_resolution[1]+1):
                grid[row, clm] = _SPMPixel(row,clm)

        # Distribute Stars
        for n in range(len(self.target_star_pos)):
            pixel:_SPMPixel=grid[prow_star[n],pclm_star[n]]
            pixel.AddStar(mass[n],age[n],Z[n])
        
        # Distribute BH
        for n in range(len(self.target_bh_pos)):
            pixel:_SPMPixel=grid[prow_bh[n],pclm_bh[n]]
            pixel.AddBlackhole(mass[n])
        
        
        # Pixelwise Generate grid
        for row in range(grid_resolution[0]):
            for clm in range(grid_resolution[1]):
                pixel:_SPMPixel=grid[row, clm]
                pixel.generate_grid()

        self.SPMGrid = grid



    def show_star_mass_map(self):
        mass_map = numpy.zeros(self.SPMGrid.shape)
        # print(mass_map.shape[0])
        for row in range(mass_map.shape[0]):
            for clm in range(mass_map.shape[1]):
                pixel:_SPMPixel=self.SPMGrid[row,clm]
                mass_map[row,clm]=pixel.star_mass
        
        img=plt.imshow(mass_map,cmap='grey')
        plt.colorbar(img)
        plt.show()




        
    
    # def show_interpolated_mass_grid_image(self):

    #     img=plt.imshow(self.grid_mass_interpolated.T**self.contrast_exponent,cmap='grey',origin='lower')
    #     plt.colorbar(img,label="$M_\odot$")
    #     plt.xlabel("kpc")
    #     plt.ylabel("kpc")
    #     plt.show()

    # def show_age_distribution(self):pass
    #     fig,axes = plt.subplots(1,2,figsize=(10, 5))
    #     ax1,ax2 = axes
    #     img=ax1.imshow(self.grid_mass_interpolated.T**self.contrast_exponent,cmap='grey',origin='lower')

    #     divider = make_axes_locatable(ax1)
    #     cax = divider.append_axes("right", size="5%", pad=0.1)
    #     cbar = fig.colorbar(img,cax=cax,label="$M_\odot$")

    #     # ax1.set_xlabel("kpc")
    #     # ax1.set_ylabel("kpc")

    #     def ShowHistogramForAges(ages):
    #         log10_ages=numpy.log10(ages)+6
    #         ax2.hist(log10_ages,bins=numpy.arange(6,10,0.1))
    #         ax2.set_xlabel("Myr")
    #         ax2.set_ylabel("count")


    #     def onclick(event):
    #         ix, iy = round(event.xdata), round(event.ydata)
    #         ages = self.grid_age_distributed[ix,iy]
    #         ax2.clear()
    #         ShowHistogramForAges(ages)
    #         fig.canvas.draw()


    #     fig.canvas.mpl_connect('button_press_event', onclick)
    #     plt.show()


    # def show_spectra(self):
    #     fig,axes = plt.subplots(1,2,figsize=(10, 5))
    #     ax1,ax2 = axes
    #     img=ax1.imshow(self.grid_mass_interpolated.T**self.contrast_exponent,cmap='grey',origin='lower')

    #     divider = make_axes_locatable(ax1)
    #     cax = divider.append_axes("right", size="5%", pad=0.1)
    #     cbar = fig.colorbar(img,cax=cax,label="$M_\odot$")

    #     # ax1.set_xlabel("kpc")
    #     # ax1.set_ylabel("kpc")

    #     def ShowPixelSpectra(ages,mass):
    #         log10_ages=numpy.log10(ages)+6
    #         bin_counts,age_bins=numpy.histogram(log10_ages,bins=numpy.arange(6,10,0.1))
            

    #         total_flux=0*FLUX.WL
    #         for a,c in zip(age_bins,bin_counts):
    #             if c==0:continue
    #             aflux=FLUX[str(numpy.round(a,1))]
    #             total_flux+=aflux

    #             # ax2.plot(FLUX.WL,aflux,'--')

    #         ax2.plot(FLUX.WL,total_flux,'k')
    #         ax2.set_yscale('log')
    #         ax2.set_xscale('log')



    #     def onclick(event):
    #         ix, iy = round(event.xdata), round(event.ydata)
    #         ages = self.grid_age_distributed[ix,iy]
    #         proj_mass = self.grid_mass_interpolated[ix,iy]
    #         ax2.clear()
    #         ShowPixelSpectra(ages,proj_mass)
    #         fig.canvas.draw()


    #     fig.canvas.mpl_connect('button_press_event', onclick)
    #     plt.show()
