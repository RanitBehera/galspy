import galspy
from galspy.utility.visualization import CubeVisualizer
import numpy
import matplotlib.pyplot as plt
from typing import Literal
from mpl_toolkits.axes_grid1 import make_axes_locatable
import galspec.bpass as bp
from matplotlib.gridspec import GridSpec
from matplotlib.ticker import MaxNLocator
import matplotlib.colors as mcolors
import time
import os
import pickle
from galspec.Utility import LuminosityToABMagnitude


from astropy.cosmology import FlatLambdaCDM
cosmo = FlatLambdaCDM(H0=67.36, Om0=0.3153)

class _SPMPixel:
    _spec_cache_stellar=None
    _spec_cache_nebular=None
    # _spec_tube=None
    def __init__(self,row:int=0,clm:int=0) -> None:
        self.row=row
        self.column=clm
        # STAR
        self.star_bank=[]
        self.star_mass=0
        self.star_count=0
        # BH
        self.bh_bank=[]
        self.bh_mass=0
        self.bh_count=0

        # Foots
        self.M_foots = numpy.linspace(5,8,31)   # in log space
        self.T_foots = numpy.arange(6,11.1,0.1)  # Mathc with BAPSS: in log space : 1Myr to 100Byr
        self.Z_foots = numpy.log10([1e-5,1e-4,1e-3,2e-3,3e-3,4e-3,6e-3,8e-3,1e-2,1.4e-2,2e-2,3e-2,4e-2])
        # TODO: T_foots other than BPASS: Interpolation

    def AddStar(self,mass,age,metallicity):
        self.star_bank.append((mass,age,metallicity))
        self.star_mass+=mass
        self.star_count+=1

    def AddBlackhole(self,mass):
        self.bh_bank.append((mass))
        self.bh_mass+=mass
        self.bh_count+=1

    def generate_grid(self):
        # Bin Width
        M_bw = self.M_foots[1]-self.M_foots[0]
        T_bw = self.T_foots[1]-self.T_foots[0]

        #Bin Edges
        self._M_edges = numpy.array([self.M_foots[0]-M_bw/2]+[0.5*(self.M_foots[i]+self.M_foots[i+1]) for i in range(len(self.M_foots)-1)]+[self.M_foots[-1]+M_bw/2])
        self._T_edges = numpy.array([self.T_foots[0]-T_bw/2]+[0.5*(self.T_foots[i]+self.T_foots[i+1]) for i in range(len(self.T_foots)-1)]+[self.T_foots[-1]+T_bw/2])
        self._Z_edges = numpy.array([2*self.Z_foots[0]-self.Z_foots[1]]+
                              [0.5*(self.Z_foots[i]+self.Z_foots[i+1]) for i in range(len(self.Z_foots)-1)]+
                              [2*self.Z_foots[-1]-self.Z_foots[-2]])

        # Number of Bins
        num_Mbin,num_Tbin,num_Zbin=len(self._M_edges)-1,len(self._T_edges)-1,len(self._Z_edges)-1
        
        # Initialise Grid
        self.grid=numpy.zeros((num_Mbin,num_Tbin,num_Zbin))
        self.flux_weight_grid=numpy.zeros((num_Mbin,num_Tbin,num_Zbin))

        # Find Bin Index (BID)
        # TODO : Overflow and undeflow bins
        # TODO : Z interplotatio, this will make binning easier
         # To avoid -inf in numpy: RuntimeWarning: divide by zero encountered in log10 add a small number
        self.star_bank=numpy.array(self.star_bank)+(1e-35)
        for log10_M,log10_T,log10_Z in numpy.log10(self.star_bank):
            # Mass
            m_ind = int((log10_M-self._M_edges[0])/M_bw)

            # Age : in units of Myr : log10T=0=>TMyr=1=>T=10^6yr
            if log10_T<0:T_ind=0    # For just spawned stars
            else:T_ind = int((6+log10_T-self._T_edges[0])/T_bw)

            # Metallicity
            if log10_Z<=self._Z_edges[0]:Z_ind=0
            elif log10_Z>=self._Z_edges[-1]:Z_ind=len(self._Z_edges)-2
            # Two less : one for edges to bins, another for 0 based bin index 
            else:           
                for i in range(len(self._Z_edges)):
                    if self._Z_edges[i]<log10_Z:
                        continue
                    else:
                        Z_ind=i-1
                        break

            # Populate grid
            self.grid[m_ind,T_ind,Z_ind] += 1
            # self.flux_weight_grid[m_ind,T_ind,Z_ind] += 10**(self._M_edges[m_ind]-6)


    def GetHistogram(self,hist_for=Literal["Age","Mass","Metallicity"]):
        assert hist_for in ["Age","Mass","Metallicity"]
        
        if hist_for=="Mass":
            hist_x = self.M_foots
            hist_y = numpy.array([numpy.sum(self.grid[i,:,:]) for i in range(len(hist_x))])
        elif hist_for=="Age":
            hist_x = self.T_foots
            hist_y = numpy.array([numpy.sum(self.grid[:,i,:]) for i in range(len(hist_x))])
        elif hist_for=="Metallicity":
            hist_x = self.Z_foots
            hist_y = numpy.array([numpy.sum(self.grid[:,:,i]) for i in range(len(hist_x))])
            
        return hist_x,hist_y
    

    def GetSpectra(self):
        if _SPMPixel._spec_cache_stellar is None:
            with open("cache/cloudy_chab_300M.in","rb") as fp:
                _SPMPixel._spec_cache_stellar = pickle.load(fp)

        if _SPMPixel._spec_cache_nebular is None:
            with open("cache/cloudy_chab_300M.out","rb") as fp:
                _SPMPixel._spec_cache_nebular = pickle.load(fp)        

        WL = _SPMPixel._spec_cache_stellar["0.00001"]["WL"]
        TOTAL_FLUX_STELLAR = numpy.zeros(len(WL))
        TOTAL_FLUX_NEBULAR = numpy.zeros(len(WL))

        # s=time.time()
        for Zi,Z in enumerate(self.Z_foots):
            Z_KEY = f"{10**Z:.5f}".rstrip('0')
            FLUX_ALL_STELLAR=_SPMPixel._spec_cache_stellar[Z_KEY]
            FLUX_ALL_NEBULAR=_SPMPixel._spec_cache_nebular[Z_KEY]
            for Ti,T in enumerate(self.T_foots):
                FLUX_STELLAR = FLUX_ALL_STELLAR[str(numpy.round(T,1))]
                FLUX_NEBULAR = FLUX_ALL_NEBULAR[str(numpy.round(T,1))]
                # How to get the mass factor is collapse
                # Only multiplying by count assumes all star to have same mass
                # However B pass is only for 10^6 mass
                cell_counts = self.grid[:,Ti,Zi]
                TOTAL_FLUX_STELLAR = TOTAL_FLUX_STELLAR + numpy.sum((cell_counts * (10**(self.M_foots-6)))) * FLUX_STELLAR
                TOTAL_FLUX_NEBULAR = TOTAL_FLUX_NEBULAR + numpy.sum((cell_counts * (10**(self.M_foots-6)))) * FLUX_NEBULAR
                    # Works however 10 times more masives doesn't mean 10 times more flux. Surface brighness??
        # e=time.time()
        # print("Method 1",e-s)
        

        # This Method is slower compared to first, find out why
        # if _SPMPixel._spec_tube is None:
        #     print("Generating Tube")            
        #     tube = numpy.zeros((13,51,len(_SPMPixel._spec_cache["0.00001"]["WL"])))
        #     for Zi,Z in enumerate(self.Z_foots):
        #         Z_KEY = f"{10**Z:.5f}".rstrip('0')
        #         FLUX_ALL=_SPMPixel._spec_cache[Z_KEY]
        #         for Ti,T in enumerate(self.T_foots):
        #             FLUX = FLUX_ALL[str(numpy.round(T,1))]
        #             tube[Zi,Ti,:]=FLUX
            
        #     _SPMPixel._spec_tube = tube
        #     print("Done")    


        # if True:
        #     # cap
        #     cap = numpy.sum(self.flux_weight_grid,axis=0).T
        #     s=time.time()
        #     cap_on_tube = cap[:,:,numpy.newaxis]*_SPMPixel._spec_tube
        #     TOTAL_FLUX2 = cap_on_tube.sum(axis=(0,1))
        # e=time.time()
        # print("Method 2",e-s)

        # dif = TOTAL_FLUX - TOTAL_FLUX2
        # print(dif)
        # print(numpy.unique(numpy.clip(dif,1e-10,None)))


        return WL,TOTAL_FLUX_STELLAR,TOTAL_FLUX_NEBULAR
            



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

        if False:
            offset=numpy.array([-5,-4,1])
            self._target_location=self._target_location+offset

        self.gather_particles_in_region()

    def target_PIG_Group(self,pig_groupid,zoom=1,offset=[0,0,0]):
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

        x,y,z = location
        xo,yo,zo = offset

        self.target_region(x+xo,y+yo,z+zo,size) 

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


    def show_mass_metallicity_scatter(self):
        MINIMUM_AGE = 0
        mask = (self.target_star_age_in_Myr>MINIMUM_AGE)
        MASS_UNIT=1e10 # TODO : Remove Hardcoded mass unit below
        plt.plot(self.target_star_mass[mask]*MASS_UNIT,self.target_star_metallicity[mask],'.',ms=2)
        plt.xscale('log')
        plt.yscale('log')
        plt.xlabel("Mass")
        plt.ylabel("Metallicity")
        plt.title(f"Age>{MINIMUM_AGE}Myr")
        plt.axvline(self._PIG.Header.MassTable()[4]*MASS_UNIT,color='k',ls='--',lw=1)
        plt.axhline(0.02,color='k',ls='--',lw=1)
        plt.show()


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
        self.resolution=grid_resolution

        span_Up_star = numpy.max(self._Up_star) - numpy.min(self._Up_star)
        span_Vp_star = numpy.max(self._Vp_star) - numpy.min(self._Vp_star)

        span_Up_bh = numpy.max(self._Up_bh) - numpy.min(self._Up_bh)
        span_Vp_bh = numpy.max(self._Vp_bh) - numpy.min(self._Vp_bh)

        span = max([span_Up_star,span_Vp_star,span_Up_bh,span_Vp_bh])

        span*=2 # To keep everything well inside field boundary
        #TODO:Better solution to fix slight offset of index. for (50,50) index should go to 0-49. case of 50.04
        #TODO:Else add this multiplier as class variable

        grid_drow = span/grid_resolution[0]
        grid_dclm = span/grid_resolution[1] 

        # TODO: drow and dclm
        self._grid_drow = grid_drow

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

        mass_map = numpy.zeros(self.SPMGrid.shape)
        for row in range(mass_map.shape[0]):
            for clm in range(mass_map.shape[1]):
                pixel:_SPMPixel=self.SPMGrid[row,clm]
                mass_map[row,clm]=pixel.star_mass
        
        self.mass_map = mass_map 


    def _show_scale(self,ax:plt.Axes):
        ax.plot([2,5],[2,2],'white',lw=1)
        ax.plot([2,2],[2-0.2,2+0.2],'white',lw=1)
        ax.plot([5,5],[2-0.2,2+0.2],'white',lw=1)
        ax.annotate(f"{3*self._grid_drow:.01f}kpc",xy=(3.5,2),xytext=(0,5),
                    xycoords='data',textcoords="offset pixels",
                    color='white',ha='center')

    def show_star_mass_map(self):
        # TODO : Transpose
        img=plt.imshow(self.mass_map,cmap='grey')
        plt.colorbar(img)
        self._show_scale(plt.gca())
        plt.show()

    


    def show_pixelwise_histogram(self):
        fig = plt.figure(figsize=(10,5))
        gs = GridSpec(3,2,figure=fig)

        ax1 = fig.add_subplot(gs[:,0])

        ax2 = fig.add_subplot(gs[0,1])
        ax3 = fig.add_subplot(gs[1,1])
        ax4 = fig.add_subplot(gs[2,1])


        img=ax1.imshow(self.mass_map**self.contrast_exponent,cmap='grey',origin='upper')
        self._show_scale(ax1)


        divider = make_axes_locatable(ax1)
        cax = divider.append_axes("top", size="5%", pad=0.1)
        cbar = fig.colorbar(img,cax=cax,label="$M_\odot$",orientation="horizontal",location="top")
    

        def ShowHistogram(pixel:_SPMPixel):
            hist_x,hist_y=pixel.GetHistogram("Mass")
            ax2.bar(hist_x,hist_y,width=0.08,align='center')
            
            hist_x,hist_y=pixel.GetHistogram("Age")
            ax3.bar(hist_x,hist_y,width=0.08,align='center')
           
            hist_x,hist_y=pixel.GetHistogram("Metallicity")
            ax4.bar(hist_x,hist_y,width=0.08,align='center')
            
            ax2.set_xlabel("Mass")
            ax3.set_xlabel("Age (Myr)")
            ax4.set_xlabel("Metallicity")

            for ax in [ax2,ax3,ax4]:
                ax.yaxis.set_major_locator(MaxNLocator(integer=True))



        def onclick(event):
            if not event.inaxes == ax1: return
            ix, iy = round(event.xdata), round(event.ydata)
            [p.remove() for p in ax1.patches]
            rect = plt.Rectangle((ix-0.5, iy-0.5), 1, 1, edgecolor='red', facecolor='none')
            ax1.add_patch(rect)
            
            for ax in [ax2,ax3,ax4]: ax.clear()
            pixel = self.SPMGrid[iy,ix]
            ShowHistogram(pixel)
            
            fig.canvas.draw()



        fig.canvas.mpl_connect('button_press_event', onclick)

        ax1.set_xlabel("Pixel Index")
        ax1.set_ylabel("Pixel Index")

        ax2.set_xlabel("Mass")
        ax3.set_xlabel("Age (Myr)")
        for ax in [ax2,ax3,ax4]:
            ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        plt.show()

    

    def show_pixelwise_spectra(self):
        fig,axes = plt.subplots(1,2,figsize=(10, 5))
        ax1,ax2 = axes

        img=ax1.imshow(self.mass_map**self.contrast_exponent,cmap='grey',origin='upper')
        self._show_scale(ax1)

        divider = make_axes_locatable(ax1)
        cax = divider.append_axes("top", size="5%", pad=0.1)
        cbar = fig.colorbar(img,cax=cax,label="$M_\odot$",orientation="horizontal",location="top")

        def ShowPixelSpectra(pixel:_SPMPixel):
            wl,st,nb=pixel.GetSpectra()
            ax2.plot(wl,st,label="Stellar")
            ax2.plot(wl,nb,label="Nebular")
            ax2.plot(wl,st+nb,label="Total")
            ax2.set_yscale('log')
            ax2.set_xscale('log')
            ax2.legend()
            # ax2.set_xlim(500,8000)
            # ax2.set_ylim(max(y)/1e3,10*max(y))
   

        def onclick(event):
            if not event.inaxes == ax1: return
            ix, iy = round(event.xdata), round(event.ydata)
            [p.remove() for p in ax1.patches]
            rect = plt.Rectangle((ix-0.5, iy-0.5), 1, 1, edgecolor='red', facecolor='none')
            ax1.add_patch(rect)
            
            ax2.clear()
            pixel = self.SPMGrid[iy,ix]
            ShowPixelSpectra(pixel)
            
            fig.canvas.draw()


        fig.canvas.mpl_connect('button_press_event', onclick)
        ax1.set_xlabel("Pixel Index")
        ax1.set_ylabel("Pixel Index")
        plt.show()


    def show_rgb_channels(self,band_center:list[int,int,int],band_width=list[int,int,int]):
        band_center = numpy.int32(band_center)
        band_low = numpy.int32(numpy.array(band_center)-0.5*numpy.array(band_width))
        band_high = numpy.int32(numpy.array(band_center)+0.5*numpy.array(band_width))
        
        
        
        fig = plt.figure(figsize=(10,5))
        gs = GridSpec(2,4,figure=fig)

        axR = fig.add_subplot(gs[0,0])
        axG = fig.add_subplot(gs[0,1])
        axB = fig.add_subplot(gs[0,2])
        axRGB = fig.add_subplot(gs[0,3])

        axSpec = fig.add_subplot(gs[1,:])
        
        red=0*self.mass_map
        green=0*self.mass_map
        blue=0*self.mass_map

        print("Getting Pixelwise channels ...")
        for row in range(self.resolution[0]):
            for clm in range(self.resolution[1]):
                print(row*self.resolution[1]+clm)
                pixel:_SPMPixel=self.SPMGrid[row,clm]
                wave,spec_st,spec_nb=pixel.GetSpectra()
                spec_tot = spec_st + spec_nb

                red[row,clm]=numpy.mean(spec_st[band_low[0]:band_high[0]])
                green[row,clm]=numpy.mean(spec_st[band_low[1]:band_high[1]])
                blue[row,clm]=numpy.mean(spec_st[band_low[2]:band_high[2]])

        cmap_red = mcolors.LinearSegmentedColormap.from_list('custom_red', ['black', 'red'])
        cmap_green = mcolors.LinearSegmentedColormap.from_list('custom_green', ['black', 'green'])
        cmap_blue = mcolors.LinearSegmentedColormap.from_list('custom_blue', ['black', 'blue'])




        max_r = numpy.max(red)
        max_g = numpy.max(green)
        max_b = numpy.max(blue)
        max_rgb = numpy.max(numpy.row_stack((red,green,blue)))

        # red = red/max_r
        # green = green/max_g
        # blue = blue/max_b

        axR.imshow(red,cmap=cmap_red)
        axG.imshow(green,cmap=cmap_green)
        axB.imshow(blue,cmap=cmap_blue)

        
        clr_img = numpy.stack((red, green, blue), axis=-1)
        clr_img = clr_img / numpy.max(clr_img)
        axRGB.imshow(clr_img)

        self._show_scale(axR)
        self._show_scale(axG)
        self._show_scale(axB)
        self._show_scale(axRGB)

        # axR.contour(red, levels=4, colors='white', linewidths=0.5,alpha=0.5)
        # axG.contour(green, levels=4, colors='white', linewidths=0.5,alpha=0.5)
        # axB.contour(blue, levels=4, colors='white', linewidths=0.5,alpha=0.5)




        def ShowPixelSpectra(pixel:_SPMPixel):
            wl,st,nb=pixel.GetSpectra()
            axSpec.plot(wl,st,label="Stellar")
            axSpec.plot(wl,nb,label="Nebular")
            axSpec.plot(wl,st+nb,label="Total")
            # import numpy as np
            # np.savetxt(f"/mnt/home/student/cranit/RANIT/Repo/galspy/study/hpc_proposal/pixel_{self.ix}_{self.iy}.txt",np.column_stack([x,y]))
            axSpec.set_yscale('log')
            axSpec.legend()
            # axSpec.set_xscale('log')
            axSpec.set_xlim(500,8000)
            axSpec.set_ylim(max(st+nb)/1e3,10*max(y))
            axSpec.axvspan(band_low[0],band_high[0],fc='r',ec=None,alpha=0.1)
            axSpec.axvspan(band_low[1],band_high[1],fc='g',ec=None,alpha=0.1)
            axSpec.axvspan(band_low[2],band_high[2],fc='b',ec=None,alpha=0.1)

        def onclick(event):
            if not event.inaxes in [axR,axG,axB,axRGB]: return
            ix, iy = round(event.xdata), round(event.ydata)
            [[p.remove() for p in ax.patches] for ax in [axR,axG,axB,axRGB]]
            rectR = plt.Rectangle((ix-0.5, iy-0.5), 1, 1, ec='white', fc='none')
            rectG = plt.Rectangle((ix-0.5, iy-0.5), 1, 1, ec='white', fc='none')
            rectB = plt.Rectangle((ix-0.5, iy-0.5), 1, 1, ec='white', fc='none')
            rectRGB = plt.Rectangle((ix-0.5, iy-0.5), 1, 1, ec='white', fc='none')
            axR.add_patch(rectR)
            axG.add_patch(rectG)
            axB.add_patch(rectB)
            axRGB.add_patch(rectRGB)
            
            axSpec.clear()
            pixel = self.SPMGrid[iy,ix]
            # self.ix=ix
            # self.iy=iy
            ShowPixelSpectra(pixel)
            
            fig.canvas.draw()

        fig.canvas.mpl_connect('button_press_event', onclick)

        plt.show()

    def show_uv_channels(self,ang_start,ang_stop):
        fig = plt.figure(figsize=(10,5))
        gs = GridSpec(2,2,figure=fig)

        ax_UVSt     = fig.add_subplot(gs[0,0])
        ax_UVTot    = fig.add_subplot(gs[0,1])
        axSpec   = fig.add_subplot(gs[1,:])

        uv_stellar = 0*self.mass_map
        uv_total = 0*self.mass_map

        wls,_,_ = self.SPMGrid[0,0].GetSpectra()
        mask1 = wls>ang_start
        mask2 = wls<ang_stop
        mask = mask1 & mask2


        print("Getting Pixelwise channels ...")
        for row in range(self.resolution[0]):
            for clm in range(self.resolution[1]):
                print(row*self.resolution[1]+clm)
                pixel:_SPMPixel=self.SPMGrid[row,clm]
                wave,spec_st,spec_nb=pixel.GetSpectra()
                spec_tot = spec_st + spec_nb

                uv_stellar[row,clm] = numpy.mean(spec_st[mask])
                uv_total[row,clm]= numpy.mean(spec_tot[mask])


        cmap_grey = mcolors.LinearSegmentedColormap.from_list('custom_red', ['black', 'white'])        

        ax_UVSt.imshow(uv_stellar,cmap=cmap_grey)
        ax_UVTot.imshow(uv_total,cmap=cmap_grey)





        def ShowPixelSpectra(pixel:_SPMPixel):
            wl,st,nb=pixel.GetSpectra()
            axSpec.plot(wl,st,label="Stellar")
            axSpec.plot(wl,nb,label="Nebular")
            axSpec.plot(wl,st+nb,label="Total")
            # import numpy as np
            # np.savetxt(f"/mnt/home/student/cranit/RANIT/Repo/galspy/study/hpc_proposal/pixel_{self.ix}_{self.iy}.txt",np.column_stack([x,y]))
            axSpec.set_yscale('log')
            axSpec.legend()
            # axSpec.set_xscale('log')
            axSpec.set_xlim(500,8000)
            axSpec.set_ylim(max(st+nb)/1e5,10*max(st+nb))
            axSpec.axvspan(ang_start,ang_stop,fc='k',ec=None,alpha=0.1)


        def onclick(event):
            if not event.inaxes in [ax_UVSt,ax_UVTot]: return
            ix, iy = round(event.xdata), round(event.ydata)
            [[p.remove() for p in ax.patches] for ax in [ax_UVSt,ax_UVTot]]
            rectR = plt.Rectangle((ix-0.5, iy-0.5), 1, 1, ec='white', fc='none')
            rectG = plt.Rectangle((ix-0.5, iy-0.5), 1, 1, ec='white', fc='none')
            rectB = plt.Rectangle((ix-0.5, iy-0.5), 1, 1, ec='white', fc='none')
            rectRGB = plt.Rectangle((ix-0.5, iy-0.5), 1, 1, ec='white', fc='none')
            ax_UVSt.add_patch(rectR)
            ax_UVTot.add_patch(rectG)
            
            axSpec.clear()
            pixel = self.SPMGrid[iy,ix]
            # self.ix=ix
            # self.iy=iy
            ShowPixelSpectra(pixel)
            
            fig.canvas.draw()

        fig.canvas.mpl_connect('button_press_event', onclick)

        plt.show()



    def get_MAB(self,start,stop,lrepr):
        uv_stellar = 0*self.mass_map
        uv_total = 0*self.mass_map

        wls,_,_ = self.SPMGrid[0,0].GetSpectra()
        mask1 = wls>start
        mask2 = wls<stop
        mask = mask1 & mask2


        print("Getting Pixelwise channels ...")
        for row in range(self.resolution[0]):
            for clm in range(self.resolution[1]):
                print(row*self.resolution[1]+clm)
                pixel:_SPMPixel=self.SPMGrid[row,clm]
                wave,spec_st,spec_nb=pixel.GetSpectra()
                spec_tot = spec_st + spec_nb

                uv_stellar[row,clm] = numpy.mean(spec_st[mask])
                uv_total[row,clm]= numpy.mean(spec_tot[mask])


        LUV_S = numpy.sum(uv_stellar)
        LUV_T = numpy.sum(uv_total)

        MAB_S = LuminosityToABMagnitude(LUV_S,lrepr)
        MAB_T = LuminosityToABMagnitude(LUV_T,lrepr)


        return MAB_S,MAB_T





























