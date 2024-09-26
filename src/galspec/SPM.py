import galspy
from galspy.utility.visualization import CubeVisualizer
import numpy
import matplotlib.pyplot as plt
from typing import Literal
from mpl_toolkits.axes_grid1 import make_axes_locatable
import galspec.bpass as bp
from matplotlib.gridspec import GridSpec
from matplotlib.ticker import MaxNLocator

# from multiprocessing import Pool
from multiprocessing.pool import ThreadPool as Pool


from astropy.cosmology import FlatLambdaCDM
cosmo = FlatLambdaCDM(H0=67.36, Om0=0.3153)



class _SPMPixel:
    _spec_cache=None
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
            self.grid[m_ind,T_ind,Z_ind] +=1


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
    
    def CacheSpectras():
        print("Caching Spectras...")
        _SPMPixel._spec_cache={}
        Z_foots=[1e-5,1e-4,1e-3,2e-3,3e-3,4e-3,6e-3,8e-3,1e-2,1.4e-2,2e-2,3e-2,4e-2]

        for i,Z in enumerate(Z_foots):
            print(i+1,"/",len(Z_foots),"...",end=" ",flush=True)
            BPASS = bp.BPASS("CHABRIER_UPTO_300M","Binary",Z)
            FLUX=BPASS.Spectra.GetFlux(500,10000)
            _SPMPixel._spec_cache[i]=FLUX
            print("Done")


    def GetSpectra(self):
        if _SPMPixel._spec_cache==None:
            _SPMPixel.CacheSpectras()

        pick_age = lambda ind:str(numpy.round(self.T_foots[ind],1))        

        TOTAL_FLUX = 0*numpy.array(len(_SPMPixel._spec_cache[0][pick_age(0)]))
        for zi,_ in enumerate(self.Z_foots):
            for ti,_ in enumerate(self.T_foots):
                for mi,_ in enumerate(self.M_foots):
                    FLUX_ALL=_SPMPixel._spec_cache[zi]
                    FLUX = FLUX_ALL[pick_age(ti)]
                    mass = self.M_foots[mi]
                    cell_count = self.grid[mi,ti,zi]
                    mass_factor = 10**(mass-6)
                    TOTAL_FLUX = TOTAL_FLUX + cell_count * mass_factor * FLUX
        
        return _SPMPixel._spec_cache[0].WL,TOTAL_FLUX
            



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



    def show_star_mass_map(self):
        # TODO : Transpose
        img=plt.imshow(self.mass_map,cmap='grey')
        plt.colorbar(img)
        plt.show()


    def show_pixelwise_histogram(self):
        fig = plt.figure(figsize=(10,5))
        gs = GridSpec(3,2,figure=fig)

        ax1 = fig.add_subplot(gs[:,0])

        ax2 = fig.add_subplot(gs[0,1])
        ax3 = fig.add_subplot(gs[1,1])
        ax4 = fig.add_subplot(gs[2,1])


        img=ax1.imshow(self.mass_map**self.contrast_exponent,cmap='grey',origin='upper')

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
            ax3.set_xlabel("Metallicity")

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

        divider = make_axes_locatable(ax1)
        cax = divider.append_axes("top", size="5%", pad=0.1)
        cbar = fig.colorbar(img,cax=cax,label="$M_\odot$",orientation="horizontal",location="top")

        _SPMPixel.CacheSpectras()

        def ShowPixelSpectra(pixel:_SPMPixel):
            x,y=pixel.GetSpectra()
            ax2.plot(x,y)
            ax2.set_yscale('log')
            ax2.set_xscale('log')
   

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


    def show_rgb_channels(self):
        fig = plt.figure(figsize=(10,5))
        gs = GridSpec(2,2,figure=fig)

        axR = fig.add_subplot(gs[0,0])
        axG = fig.add_subplot(gs[0,1])
        axB = fig.add_subplot(gs[1,0])
        axRGB = fig.add_subplot(gs[1,1])
        
        red=0*self.mass_map
        green=0*self.mass_map
        blue=0*self.mass_map

        print("Getting Pixelwise channels ...")
        for row in range(self.resolution[0]):
            for clm in range(self.resolution[1]):
                pixel:_SPMPixel=self.SPMGrid[row,clm]
                wave,spec=pixel.GetSpectra()
                red[row,clm]=spec[3500]
                green[row,clm]=spec[1500]
                blue[row,clm]=spec[1200]

        axR.imshow(red,cmap="grey")
        axG.imshow(green,cmap="grey")
        axB.imshow(blue,cmap="grey")


        red = red/numpy.max(red)
        green = green/numpy.max(green)
        blue = blue/numpy.max(blue)

        clr_img = numpy.stack((red, green, blue), axis=-1)

        axRGB.imshow(clr_img)

        plt.show()
