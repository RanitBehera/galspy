import numpy as np
import astropy
from scipy.signal import convolve2d
from typing import Literal
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import cv2 as cv
from typing import List
import pickle
from galspy.Utility.Visualization import Cube3D
from galspy.MPGadget import _PIG
from galspy.Spectra import SpectralTemplates
from astropy.cosmology import FlatLambdaCDM
from galspy.Spectra.jwst import get_NIRCam_filter
from galspy.Spectra.jwst import _AVAIL_JWST_FILTERS_HINT



def show_image(img,label=""):
    plt.imshow(img.T**0.02,origin="lower")
    plt.gca().set_aspect("equal")
    plt.show()


class BlobFinder:
    def __init__(self,img):
        self.target_img = img



    def opencv_findblobs(self,thresold=0):
        img=self.target_img

        # Foreground should be white and background should be black.
        THRESOLD = thresold
        img_th = np.where(img>=THRESOLD,img,0)
        img_th = 255*(img_th/np.max(img_th))    #Normalise to unity and then scale to 255

        # ----- MASKS
        bin_mask = np.int32(np.where(img>0,255,0))
        th_mask = np.int32(np.where(img_th>0,255,0))

        _,mask = cv.threshold(bin_mask.astype(np.uint8),0,255,cv.THRESH_BINARY)
        _,mask_th = cv.threshold(th_mask.astype(np.uint8),0,255,cv.THRESH_BINARY)

        # ----- MORPHOLOGICAL TRANSFORMATIONS
        # CLOSING - (dilation followed by erosion) : Black dots gets erased
        CLOSING_KERNEL_SIZE=2
        kernel = np.ones((CLOSING_KERNEL_SIZE,CLOSING_KERNEL_SIZE),np.uint8)
        closed = cv.morphologyEx(mask_th, cv.MORPH_CLOSE, kernel)
        # OPENING - (erosion followed by dilation) : White dots gets erased
        OPENING_KERNEL_SIZE=3
        kernel = np.ones((OPENING_KERNEL_SIZE,OPENING_KERNEL_SIZE),np.uint8)
        opened = cv.morphologyEx(closed, cv.MORPH_OPEN, kernel)
        DILATION_KERNEL_SIZE=4
        # DILATION - Nearby mini-islands gets connected
        kernel = np.ones((DILATION_KERNEL_SIZE,DILATION_KERNEL_SIZE),np.uint8)
        dilated = cv.dilate(opened, kernel,iterations=1)

        
        # ----- BLOB DETECTION
        target_img = dilated
        params = cv.SimpleBlobDetector_Params()

        params.filterByColor = True
        params.blobColor = 255
        params.filterByArea = True
        params.minArea = 1
        # params.maxArea = 5000
        params.filterByCircularity = False
        params.minCircularity = 0.1
        params.filterByConvexity = False
        params.minConvexity = 0.8
        params.filterByInertia = False
        params.minInertiaRatio = 0.5

        detector = cv.SimpleBlobDetector_create(params)
        keypoints = detector.detect(target_img)


        # ----- CENTERS and RADIUS
        BLOB_CENTER = []
        BLOB_RADIUS = []
        for key in keypoints:
            key:cv.KeyPoint
            center,diameter,angle = key.pt,key.size,key.angle
            center = (int(center[0]), int(center[1]))
            radius = int(diameter/2)
            BLOB_CENTER.append(center)
            BLOB_RADIUS.append(radius)

        # Grow radius by a factor if they don't collide
        RADIUS_GROWTH_FACTOR=2
        BLOB_RADIUS_EXPANDED = RADIUS_GROWTH_FACTOR*np.array(BLOB_RADIUS)
        # Check for collision and shrink
        for i,(ci,ri) in enumerate(zip(BLOB_CENTER,BLOB_RADIUS_EXPANDED)):
            for j,(cj,rj) in enumerate(zip(BLOB_CENTER,BLOB_RADIUS_EXPANDED)):
                if j<=i:continue
                c2c_distance = np.linalg.norm(np.array(ci)-np.array(cj))
                r2r_distance = ri+rj
                if r2r_distance<c2c_distance:continue
                over_by_factor = r2r_distance/c2c_distance
                BLOB_RADIUS_EXPANDED[i]/=over_by_factor
                BLOB_RADIUS_EXPANDED[j]/=over_by_factor

        BLOB_RADIUS_EXPANDED = list(BLOB_RADIUS_EXPANDED)        

        # ----- LABLE MAP
        # Initialise to -1
        lable = -1*np.ones(mask.shape, dtype=int)
        # If mask is positive, initialise to 0, so that outside pixels get lable 0

        for row in range(0,lable.shape[0]):
            for clm in range(0,lable.shape[1]):
                if mask_th[row,clm]>0:lable[row,clm]=0
        
        for i,(C,R) in enumerate(zip(BLOB_CENTER,BLOB_RADIUS_EXPANDED)):
            minx,maxx=C[0]-R,C[0]+R
            miny,maxy=C[1]-R,C[1]+R

            if minx<0:minx=0
            if miny<0:miny=0
            if maxx>lable.shape[1]: maxx=lable.shape[1]
            if maxy>lable.shape[0]: maxy=lable.shape[0]

            for y in range(miny,maxy):#row
                for x in range(minx,maxx):#clm
                    dx=x-C[0]
                    dy=y-C[1]
                    r=(dx**2+dy**2)**0.5
                    if r>R:continue
                    if mask_th[y,x]==0:continue
                    lable[y,x]=i+1


        # ----- OVERLAY
        overlay_blob = cv.cvtColor(target_img,cv.COLOR_GRAY2BGR)
        for center,radius,radius_expanded in zip(BLOB_CENTER,BLOB_RADIUS,BLOB_RADIUS_EXPANDED):
            # Center +
            cv.line(overlay_blob, (center[0] - 2, center[1]), (center[0] + 2, center[1]), (255,0,0), 1)
            cv.line(overlay_blob, (center[0], center[1] - 2), (center[0], center[1] + 2), (255,0,0), 1)
            # Perimeter
            cv.circle(overlay_blob,center,radius,(255,0,0),1,cv.LINE_AA)
            cv.circle(overlay_blob,center,radius_expanded,(255,255,0),1,cv.LINE_AA)
        
        cvout = {
            "INPUT_IMG"     : img,
            "MASK_BIN"      : mask,
            "MASK_THRESOLD" : mask_th,
            "MORPH_CLOSED"  : closed,
            "MORPH_OPENED"  : opened,
            "MORPH_DILATED" : dilated,
            "OVERLAY_BLOB"  : overlay_blob,
            "LABLE_IMG"     : lable,
            # --- Pipeline Configuration
            "THRESOLD"              : THRESOLD,
            "CLOSING_KERNEL_SIZE"   : CLOSING_KERNEL_SIZE,
            "OPENING_KERNEL_SIZE"   : OPENING_KERNEL_SIZE,
            "DILATION_KERNEL_SIZE"  : DILATION_KERNEL_SIZE,
            "BLOB_COUNT"            : len(keypoints),
            "BLOB_CENTER"           : BLOB_CENTER,
            "BLOB_RADIUS"           : BLOB_RADIUS,
            "RADIUS_GROWTH_FACTOR"  : RADIUS_GROWTH_FACTOR,
            # --- Mass Fraction After Various Steps
            "MFRAC_MASK_THR" : np.sum(img*np.where(mask_th>0,1,0))/np.sum(img),
            "MFRAC_LABLE" : np.sum(img*np.where(lable>0,1,0))/np.sum(img)
        }

        return cvout
        

    def show_opencv_pipeline(self, cvout, show=False):
        fig,axs = plt.subplots(2,4,figsize=(9,6),sharex=True, sharey=True)
        fig.canvas.manager.set_window_title(f"Group ID {cvout['TARGET_GID']}")
        fig.subplots_adjust(bottom=0.05)
        axs:np.ndarray
        axs=axs.flatten()

        iter_axs=iter(axs)
        def next_ax(): return next(iter_axs)

        _FONTSIZE=12

        ax:plt.Axes=next_ax()    
        ax.imshow((np.log10(1+cvout["INPUT_IMG"].T)/np.max(np.log10(1+cvout["INPUT_IMG"].T)))**0.2,origin='lower',cmap="grey")
        JUST=16
        info="Star Count".ljust(JUST) + ":" + f"{cvout['TARGET_STAR_COUNT']}\n"
        info+="Stellar Mass".ljust(JUST) + ":" + f"{cvout['TARGET_STAR_MASS']:.02f}"+"$\\times 10^{10}\ M_\odot$/h\n"
        info+="Projection Mode".ljust(JUST) + ":" + f"{cvout['PROJECTION_MODE']}" + "(DRE)"
        ax.set_title(info,fontsize=_FONTSIZE,loc='left',fontname='monospace')


        ax=next_ax()    
        ax.imshow(cvout["MASK_BIN"].T,origin='lower',cmap="grey",interpolation='none')
        ax.set_title(f"Binary Mask",fontsize=_FONTSIZE,loc='left',fontname='monospace')


        ax=next_ax()    
        ax.imshow(cvout["MASK_THRESOLD"].T,origin='lower',cmap="grey",interpolation='none')
        JUST=16
        info="Thresold Mask\n"
        info+=("Thresold "+cvout["PROJECTION_MODE"].capitalize()).ljust(JUST) + ":" + f"{cvout['THRESOLD']}\n"
        info+="Mass Fraction".ljust(JUST) + ":" + f"{cvout['MFRAC_MASK_THR']*100:.01f}%"
        ax.set_title(info,fontsize=_FONTSIZE,loc='left',fontname='monospace')


        ax=next_ax()    
        ax.imshow(cvout["MORPH_CLOSED"].T,origin='lower',cmap="grey",interpolation='none')
        JUST=16
        info="Morphological".ljust(JUST) + ":" + "Closed\n"
        info+="Kernel Size".ljust(JUST)+":"+f"{cvout['CLOSING_KERNEL_SIZE']}"
        ax.set_title(info,fontsize=_FONTSIZE,loc='left',fontname='monospace')


        ax=next_ax()    
        ax.imshow(cvout["MORPH_OPENED"].T,origin='lower',cmap="grey",interpolation='none')
        JUST=16
        info="Morphological".ljust(JUST) + ":" + "Opened\n"
        info+="Kernel Size".ljust(JUST)+":"+f"{cvout['OPENING_KERNEL_SIZE']}"
        ax.set_title(info,fontsize=_FONTSIZE,loc='left',fontname='monospace')

        ax=next_ax()    
        ax.imshow(cvout["MORPH_DILATED"].T,origin='lower',cmap="grey",interpolation='none')
        JUST=16
        info="Morphological".ljust(JUST) + ":" + "Dilation\n"
        info+="Kernel Size".ljust(JUST)+":"+f"{cvout['DILATION_KERNEL_SIZE']}"
        ax.set_title(info,fontsize=_FONTSIZE,loc='left',fontname='monospace')


        ax=next_ax()    
        ax.imshow(np.transpose(cvout["OVERLAY_BLOB"],(1,0,2)),origin='lower',interpolation='none')
        JUST=16
        info="Blobs Detected".ljust(JUST) + ":" + f"{cvout['BLOB_COUNT']}\n"
        info+="Radius Expansion".ljust(JUST) + ":" + f"$\\times${cvout['RADIUS_GROWTH_FACTOR']}"
        ax.set_title(info,fontsize=_FONTSIZE,loc='left',fontname='monospace')

        ax=next_ax()    
        lable_img= cvout["LABLE_IMG"]
        unq_lables = np.unique(lable_img)
        bounds = 0.5*(unq_lables[:-1]+unq_lables[1:])
        bounds = np.insert(bounds,0,2*unq_lables[0]-bounds[0])
        bounds = np.append(bounds,2*unq_lables[-1]-bounds[-1])
        max_val = np.max(unq_lables)
        colormap = plt.colormaps["tab10"]
        colors = ['black','white'] + [colormap(i) for i in range(max_val)]
        cmap = mcolors.ListedColormap(colors)
        norm = mcolors.BoundaryNorm(bounds, cmap.N)
        ax.imshow(lable_img.T,origin='lower',cmap=cmap, norm=norm,interpolation='none')
        info="Lable Map\n"
        info+="Mass Fraction".ljust(JUST) + ":" + f"{cvout['MFRAC_LABLE']*100:.01f}%"
        ax.set_title(info,fontsize=_FONTSIZE,loc='left',fontname='monospace')

        for ax in axs:
            ax.set_axis_off()

        if show:
            plt.show()


class PIGSpectrophotometry:
    _template_specs_stellar = None
    _template_specs_with_nebular = None

    def __init__(self,PIG:_PIG):
        self.PIG = PIG
        self.all_stars_gid = PIG.Star.GroupID()
        self.all_star_position = PIG.Star.Position()
        self.all_star_mass = PIG.Star.Mass()
        self.all_star_ids = PIG.Star.ID()

        self._specs_template_index = PIG.GetStarsSpecIndex()

        if PIGSpectrophotometry._template_specs_stellar is None:
            PIGSpectrophotometry._template_specs_stellar = SpectralTemplates.GetStellarTemplates("CHABRIER_UPTO_300M","Binary")

        if PIGSpectrophotometry._template_specs_with_nebular is None:
            _template_specs_nebular = SpectralTemplates.GetNebularTemplates("CHABRIER_UPTO_300M","Binary")
            PIGSpectrophotometry._template_specs_with_nebular = PIGSpectrophotometry._template_specs_stellar + _template_specs_nebular
            PIGSpectrophotometry._template_specs_with_nebular[0] = _template_specs_nebular[0]

        self.luminosity_distance_Mpc = None     # Will get assigned in _get_observer_frame_dilution_factor
        self.pixel_resolution = self._get_pixel_resolution()
        self.observer_dilution = self._get_observer_frame_dilution_factor()



    def _get_pixel_resolution(self):
        h=self.PIG.Header.HubbleParam()
        Om0=self.PIG.Header.Omega0()
        z=self.PIG.Header.Redshift()  

        RB = 0.031          #arcsecond per pixel : JWST 
        RB *= 1/3600        #degree per pixel
        RB *= np.pi/180     #radian per pixel

        cosmo = FlatLambdaCDM(H0=h*100,Om0=Om0)
        DA=cosmo.angular_diameter_distance(z).value #in Mpc
        DA*=1000 #To Kpc
        res = DA * RB   #pKpc per pixel
        res *=(1+z)*h   #cKpc per pixel
        return res

    def _get_observer_frame_dilution_factor(self):
        h=self.PIG.Header.HubbleParam()
        Om0=self.PIG.Header.Omega0()
        z=self.PIG.Header.Redshift()  

        cosmo = FlatLambdaCDM(H0=h*100,Om0=Om0)
        DL = cosmo.luminosity_distance(z).value #in Mpc
        self.luminosity_distance_Mpc = DL
        DL *= 3.086e+24 # MPC to cm

        Area = 4*np.pi*(DL**2)
        dilution = 1/(Area*(1+z)) # Extra (1+z) due to wavelength

        return dilution
    
    # def _get_absolute_frame_dilution_factor(self):
    #     z=self.PIG.Header.Redshift()  

    #     D = 10 #pc
    #     D *= 3.086e+18 # pc to cm

    #     Area = 4*np.pi*(D**2)
    #     dilution = 1/(Area*(1+z)) # Extra (1+z) due to wavelength

    #     return dilution




    def _get_projection_img(self,position,mass,direction:Literal["XY","YZ","ZX"]="XY",mode:Literal["count","mass"]="count"):
        if direction not in ["XY","YZ","ZX"]:
            raise ValueError("Invalid Direction")

        x,y,z = position.T
        if direction=="XY": u,v = x,y
        elif direction=="YZ": u,v = y,z
        elif direction=="ZX": u,v = z,x

        begin_u,begin_v = np.min(u),np.min(v)
        end_u,end_v = np.max(u),np.max(v)

        pr = self.pixel_resolution

        bin_edges_u = np.arange(begin_u-0.5*pr,end_u+0.5*pr,pr)
        if bin_edges_u[-1]<end_u+0.5*pr:
            np.append(bin_edges_u,bin_edges_u[-1]+pr)
        
        bin_edges_v = np.arange(begin_v-0.5*pr,end_v+0.5*pr,pr)
        if bin_edges_v[-1]<end_v+0.5*pr:
            np.append(bin_edges_v,bin_edges_v[-1]+pr)
        
        if mode=="count":
            binheight,uedges,vedges=np.histogram2d(u,v,bins=(bin_edges_u,bin_edges_v))
        elif mode=="mass":
            binheight,uedges,vedges=np.histogram2d(u,v,bins=(bin_edges_u,bin_edges_v),weights=mass)
        
        self._uedges = uedges
        self._vedges = vedges

        return binheight,uedges,vedges, mode, u, v


    def _get_mass_factor_scaling(self,target_star_mass):
        # Mass scaling for spectrums as BPASS is for 10^6 M_solar
        # Common function so that changes are reflected in both gather_spectrum() and get_image()
        mass_factor = (target_star_mass/self.PIG.Header.HubbleParam())/1e-4
        mass_scale = 1*mass_factor  # Right now twice the mass means twice the light
        return mass_scale
    

    def gather_spectrum(self,lable_map,u,v,uedges,vedges,target_star_ids,target_star_mass):
        #u,v are either x,y or x,z or y,z depending on projection direction 

        num_blobs = np.max(lable_map)
        num_specs = num_blobs+1 #One extra for stray stars

        # Get bin/pixel coordinate of each source
        u_coords = np.digitize(u, uedges) - 1
        v_coords = np.digitize(v, vedges) - 1
        u_coords = np.clip(u_coords, 0, len(uedges) - 2)
        v_coords = np.clip(v_coords, 0, len(vedges) - 2)
        pixel_coords = np.column_stack((u_coords,v_coords))

        # Reference templates with short variable names
        tmp_specs_stellar=PIGSpectrophotometry._template_specs_stellar
        tmp_specs_with_nebular=PIGSpectrophotometry._template_specs_with_nebular

        # spectrum template index for target  
        specindex = self._specs_template_index
        tspecindex = [specindex[tsid] for tsid in target_star_ids]

        mass_scale = self._get_mass_factor_scaling(target_star_mass)

        # Initialse to gather
        wl_stellar = tmp_specs_stellar[0]
        blobspecs_stellar = np.zeros((num_specs,len(wl_stellar)))

        wl_with_nebular = tmp_specs_with_nebular[0]
        blobspecs_with_nebular = np.zeros((num_specs,len(wl_with_nebular)))

        blobwise_stellar_mass = np.zeros(num_specs)

        for (uc,vc),ti,ms,mstar in zip(pixel_coords,tspecindex,mass_scale,target_star_mass):
            l = lable_map[uc,vc]
            blobspecs_stellar[l]+=ms*tmp_specs_stellar[ti]
            blobspecs_with_nebular[l]+=ms*tmp_specs_with_nebular[ti]
            blobwise_stellar_mass[l] += mstar

        specout = {
            "WAVELENGTH_STELLAR" : wl_stellar, 
            "WAVELENGTH_WITH_NEBULAR" : wl_with_nebular,
            "BLOBWISE_SPECTRA_STELLAR" : blobspecs_stellar,  
            "BLOBWISE_SPECTRA_WITH_NEBULAR" : blobspecs_with_nebular,  
            "BLOBWISE_STELLAR_MASS" : blobwise_stellar_mass
        }

        return specout



    def _load_filter(self,wl):
       if getattr(self,"NC_F070W",None) is None: 
            self.NC_F070W = get_NIRCam_filter(wl,"F070W")

       if getattr(self,"NC_F090W",None) is None: 
            self.NC_F090W = get_NIRCam_filter(wl,"F090W")

       if getattr(self,"NC_F115W",None) is None: 
            self.NC_F115W = get_NIRCam_filter(wl,"F115W")

       if getattr(self,"NC_F150W",None) is None: 
            self.NC_F150W = get_NIRCam_filter(wl,"F150W")
       
       if getattr(self,"NC_F200W",None) is None: 
            self.NC_F200W = get_NIRCam_filter(wl,"F200W")

       if getattr(self,"NC_F270W",None) is None: 
            self.NC_F277W = get_NIRCam_filter(wl,"F277W")

       if getattr(self,"NC_F356W",None) is None: 
            self.NC_F356W = get_NIRCam_filter(wl,"F356W")

       if getattr(self,"NC_F444W",None) is None: 
            self.NC_F444W = get_NIRCam_filter(wl,"F444W")


    def _transfer_to_observer_frame(self,wl_rest,spec_rest):
        spec_obs=spec_rest
        z=self.PIG.Header.Redshift()
        wl_obs = wl_rest*(1+z)
        spec_obs*=self.observer_dilution
        return wl_obs,spec_obs

    def _get_spec_properties_observed(self,wl_rest,spec_rest):
        # L : Luminosity
        # f : flux
        OUTDICT={}

        c=3e8*1e10  # A Hz
        LSOL=3.846e33 #erg s-1
        z=self.PIG.Header.Redshift()
        PC2CM = 3.086e18 # cm per parsec

        # ===== REST FRAME PROPERTIES
        lam_rest = wl_rest
        L_lam_rest = spec_rest * LSOL
        lam_uv = 1500 #A
        lam_uv_ind = np.argmin(np.abs(lam_rest-lam_uv) )
        lam_uv_ind_n = np.argmin(np.abs(lam_rest-(lam_uv-100)))
        lam_uv_ind_p = np.argmin(np.abs(lam_rest-(lam_uv+100)))
        rf_L_lam_UV =  np.mean(L_lam_rest[lam_uv_ind_n:lam_uv_ind_p])
        rf_f_lam_UV =  rf_L_lam_UV / (4*np.pi*((10*PC2CM)**2))
        rf_f_nu_UV =  rf_f_lam_UV * (lam_uv**2)/c
        rf_MAB_UV = -2.5*np.log10(rf_f_nu_UV)-48.6
        OUTDICT["RF_L_LAM_UV"]=rf_L_lam_UV
        OUTDICT["RF_F_LAM_UV"]=rf_f_lam_UV
        OUTDICT["RF_F_NU_UV"]=rf_f_nu_UV
        OUTDICT["RF_MAB_UV"]=rf_MAB_UV


        # ===== OBSERVED FRAME PROPERTIES
        lam_obs,f_lam_obs = self._transfer_to_observer_frame(lam_rest,L_lam_rest)
        dlam_obs = np.diff(lam_obs)
        lam_obs,f_lam_obs=lam_obs[:-1],f_lam_obs[:-1]
        self._load_filter(lam_obs)  # This loads the throughput, already normalised
        f_lam_obs_dlam_obs = f_lam_obs*dlam_obs
        of_f_lam_F070W = np.sum(f_lam_obs_dlam_obs*self.NC_F070W)
        of_f_lam_F090W = np.sum(f_lam_obs_dlam_obs*self.NC_F090W)
        of_f_lam_F115W = np.sum(f_lam_obs_dlam_obs*self.NC_F115W)
        of_f_lam_F150W = np.sum(f_lam_obs_dlam_obs*self.NC_F150W)
        of_f_lam_F200W = np.sum(f_lam_obs_dlam_obs*self.NC_F200W)
        of_f_lam_F277W = np.sum(f_lam_obs_dlam_obs*self.NC_F277W)
        of_f_lam_F356W = np.sum(f_lam_obs_dlam_obs*self.NC_F356W)
        of_f_lam_F444W = np.sum(f_lam_obs_dlam_obs*self.NC_F444W)
        OUTDICT["OF_F_LAM_F070W"]=of_f_lam_F070W
        OUTDICT["OF_F_LAM_F090W"]=of_f_lam_F090W
        OUTDICT["OF_F_LAM_F115W"]=of_f_lam_F115W
        OUTDICT["OF_F_LAM_F150W"]=of_f_lam_F150W
        OUTDICT["OF_F_LAM_F200W"]=of_f_lam_F200W
        OUTDICT["OF_F_LAM_F277W"]=of_f_lam_F277W
        OUTDICT["OF_F_LAM_F356W"]=of_f_lam_F356W
        OUTDICT["OF_F_LAM_F444W"]=of_f_lam_F444W
        
        



        # ===== INFERED REST FRAME PROPERTIES
        
        
        
        return OUTDICT

     





    
    def _get_spec_properties_observed_log(self,wl_rest,spec_rest):
        c=3e8*1e10  # A Hz
        LSOL=3.846e33 #erg s-1
        z=self.PIG.Header.Redshift()

        # np.savetxt("/mnt/home/student/cranit/RANIT/Repo/galspy/temp/share_anand/spectrum.txt",np.column_stack((wl_rest,spec_rest)),
        #            header="Rest frame spectral luminosity at z=7\nUsing Cloudy resampling of BPASS templates.\nLuminosity Distance at z=7 : DL(z=7)=70498.47 Mpc\nCosmology : Om=0.3153; h=0.6736; FlatLCDM\nWavelength (lam) in Angstrom.\nSpectral Luminosity (L_lam) in Solar Luminosity per Angstrom.\nlam L_lam")


        lam_rest = wl_rest
        L_lam_rest = spec_rest

        lam_obs,f_lam_obs = self._transfer_to_observer_frame(lam_rest,L_lam_rest)

        # plt.plot(lam_rest,L_lam_rest,label="Rest")
        # x,y=np.loadtxt("/mnt/home/student/cranit/RANIT/Repo/galspy/temp/share_anand/spectrum.txt").T
        # plt.plot(x,y,label="Shared",lw=0.8)

        # plt.xscale("log")
        # plt.yscale("log")
        # plt.axvline(1437.5)
        # plt.xlabel("Wavelength")
        # plt.ylabel("Spectral Luminosity (erg s-1 A-1)")
        # plt.legend()

        # plt.figure()
        # plt.plot(lam_obs,f_lam_obs,label="Obs")
        # plt.xscale("log")
        # plt.yscale("log")
        # plt.xlabel("Wavelength")
        # plt.ylabel("Spectral flux (erg s-1 cm-2 A-1)")
        # plt.axvline(11500)
        # plt.legend()

        # plt.show()

        print("\nOBSERVER FRAME",'='*32)
        print(f"- Filter : F115W -> 1.15um corresponds to 1437.5A (rest) for z={z:.02f}")
        self._load_filter(lam_obs)
        T_lam_obs = self.NC_F115W

        f_lam_obs_avg = np.sum(f_lam_obs[:-1]*T_lam_obs[:-1]*np.diff(lam_obs))
        print(f"- Filter Flux : {f_lam_obs_avg:.02e} erg s-1 cm-2 A-1")
        f_nu_obs_avg = f_lam_obs_avg / (c/(11500**2)) 
        print(f"- Filter Flux : {f_nu_obs_avg:.02e} erg s-1 cm-2 Hz-1 (Method 1)")

        nu_obs=c/lam_obs        
        f_nu_obs = f_lam_obs*((lam_obs**2)/c)
        T_nu_obs = T_lam_obs
        f_nu_obs_avg_2 = np.sum(f_nu_obs[:-1]*T_nu_obs[:-1]*np.diff(nu_obs))/np.sum(T_nu_obs[:-1]*np.diff(nu_obs))
        print(f"- Filter Flux : {f_nu_obs_avg_2:.02e} erg s-1 cm-2 Hz-1 (Method 2)")

        m_AB_obs = -2.5*np.log10(f_nu_obs_avg)-48.60
        print(f"- Apparent AB Magnitude (Observer Frame) : m_AB = {m_AB_obs:.02f}")

        DL=self.luminosity_distance_Mpc
        print(f"- Luminosity Distance : DL = {DL:0.2f} Mpc for z=7")
        M_AB_obs = m_AB_obs - 5*(np.log10(DL*1e6)-1) + 2.5*np.log10(1+z)
        print(f"- Absolute AB Magnitude (Observer Frame) : M_AB = {M_AB_obs:0.2f}")
        lum_rest_expexted = 4*np.pi*((DL*3.086e24)**2)*(1+z)*f_lam_obs_avg
        print(f"- Expected rest frame luminosity : L = {lum_rest_expexted:0.2e} erg s-1 A-1")


        print("\nRest FRAME",'='*32)
        ind = np.argmin(np.abs(lam_rest-1437.5))
        print(f"- Wavelength : {lam_rest[ind]:.02f}A (rest) [{lam_rest[ind-5]:.02f}A <---> {lam_rest[ind+5]:.02f}A]")
        LSOL=3.846e33 #erg s-1
        mean_lum_lam = np.mean(L_lam_rest[ind-5:ind+5])*LSOL
        print(f"- Mean Luminosity : {mean_lum_lam:0.02e} erg s-1 A-1")
        mean_flux_lam = mean_lum_lam/(4*np.pi*((10*(3.08e18))**2))
        print(f"- Mean Flux (10pc) : {mean_flux_lam:0.02e} erg s-1 cm-2 A-1")
        mean_flux_nu = mean_flux_lam/(c/(1437.5**2))
        print(f"- Mean Flux (10pc): {mean_flux_nu:0.02e} erg s-1 cm-2 Hz-1")
        M_AB_rest = -2.5*np.log10(mean_flux_nu)-48.60
        print(f"- Absolute AB Magnitude (Rest Frame) : M_AB = {M_AB_rest:.02f}")


        pass





    def show_spectrum(self,wl,spec,photo=None,show=False):
        plt.plot(wl,spec)

        if photo is not None:
            for p in photo:
                plt.errorbar(p[0],p[1],capsize=4,fmt='.',ms=10,color='r')
        
        plt.xscale("log")
        plt.yscale("log")
        plt.xlim(1e3,1e5)
        plt.ylim(1e-20,1e-15)
        # plt.legend()

        if show:
            plt.show()



    def get_photometry_images(self,target_gid):
        if not (isinstance(target_gid, int) and target_gid > 0):
            raise ValueError("Integerer greather than zero needed")

        tgid = target_gid

        print(f"TGID = {tgid}")
        target_mask = (self.all_stars_gid==tgid)

        target_stars_gid = self.all_stars_gid[target_mask]
        target_star_position = self.all_star_position[target_mask]
        target_star_mass = self.all_star_mass[target_mask]
        target_star_ids = self.all_star_ids[target_mask]

        # Get bin/pixel coordinate of each source
        image,uedges,vedges,pr_mode,u,v = self._get_projection_img(target_star_position,target_star_mass,"XY","mass")
        u_coords = np.digitize(u, uedges) - 1
        v_coords = np.digitize(v, vedges) - 1
        u_coords = np.clip(u_coords, 0, len(uedges) - 2)
        v_coords = np.clip(v_coords, 0, len(vedges) - 2)
        pixel_coords = np.column_stack((u_coords,v_coords))

        # Reference templates with short variable names
        tmp_specs_stellar=PIGSpectrophotometry._template_specs_stellar
        tmp_specs_with_nebular=PIGSpectrophotometry._template_specs_with_nebular

        # spectrum template index for target  
        specindex = self._specs_template_index
        tspecindex = [specindex[tsid] for tsid in target_star_ids]

        mass_scale = self._get_mass_factor_scaling(target_star_mass)  # Right now twice the mass means twice the light

        # To observer frame
        spec_obs = tmp_specs_with_nebular*self.observer_dilution
        wl_obs = tmp_specs_with_nebular[0]*(1+self.PIG.Header.Redshift())

        LSOL=3.846e33 #erg s-1
        spec_obs *=LSOL
        self._load_filter(wl_obs)

        # Template Photometry
        tp_F070W = np.sum(spec_obs*self.NC_F070W,axis=1)
        tp_F090W = np.sum(spec_obs*self.NC_F090W,axis=1)
        tp_F115W = np.sum(spec_obs*self.NC_F115W,axis=1)
        tp_F150W = np.sum(spec_obs*self.NC_F150W,axis=1)
        tp_F200W = np.sum(spec_obs*self.NC_F200W,axis=1)
        tp_F277W = np.sum(spec_obs*self.NC_F277W,axis=1)
        tp_F356W = np.sum(spec_obs*self.NC_F356W,axis=1)
        tp_F444W = np.sum(spec_obs*self.NC_F444W,axis=1)

        # Initialise the images
        img_F070W = np.zeros_like(image)
        img_F090W = np.zeros_like(image)
        img_F115W = np.zeros_like(image)
        img_F150W = np.zeros_like(image)
        img_F200W = np.zeros_like(image)
        img_F277W = np.zeros_like(image)
        img_F356W = np.zeros_like(image)
        img_F444W = np.zeros_like(image)

        for (uc,vc),ti,ms in zip(pixel_coords,tspecindex,mass_scale):
            img_F070W[uc,vc] += ms*tp_F070W[ti]
            img_F090W[uc,vc] += ms*tp_F090W[ti]
            img_F115W[uc,vc] += ms*tp_F115W[ti]
            img_F150W[uc,vc] += ms*tp_F150W[ti]
            img_F200W[uc,vc] += ms*tp_F200W[ti]
            img_F277W[uc,vc] += ms*tp_F277W[ti]
            img_F356W[uc,vc] += ms*tp_F356W[ti]
            img_F444W[uc,vc] += ms*tp_F444W[ti]

        return {
            "F070W":img_F070W,
            "F090W":img_F090W,
            "F115W":img_F115W,
            "F150W":img_F150W,
            "F200W":img_F200W,
            "F277W":img_F277W,
            "F356W":img_F356W,
            "F444W":img_F444W
        }



    def get_light_dict(self,target_gids):
        if isinstance(target_gids, int) and target_gids > 0:
            target_gids=[target_gids]
        if isinstance(target_gids, np.uint32) and target_gids > 0:
            target_gids=[target_gids]
        elif isinstance(target_gids, list) and all(isinstance(g, int) and g > 0 for g in target_gids): pass
        elif isinstance(target_gids, np.ndarray) and all(isinstance(g, np.int64) and g > 0 for g in target_gids): pass
        elif isinstance(target_gids, np.ndarray) and all(isinstance(g, np.uint32) and g > 0 for g in target_gids): pass
        else: raise ValueError("Either int or List[int] are valid as target group id with id>0.")


        # DUMP PURPOSE
        #-------------------------------------------------------
        sfr = self.PIG.FOFGroups.StarFormationRate()

        KUV=1.15e-28  #Msol yr-1 erg S-1 Hz-1
        LUV = sfr/KUV
        PC2CM = 3.086e18
        D = 10*PC2CM  # In cm

        fUV = LUV/(4*np.pi*D**2)+1e-300
        mAB = -2.5*np.log10(fUV)-48.6
        M_AB = mAB #as distance was 10pc
        #-------------------------------------------------------


        DUMP=True
        if DUMP:
            outfile_fp = open(f"/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/SPM3/data/out_{self.PIG.sim_name}_z{str(np.round(self.PIG.Header.Redshift(),2)).replace('.','p')}_N8.csv",'w')

        for rownum,tgid in enumerate(target_gids):
            print(f"TGID = {tgid} ({rownum+1}/{len(target_gids)})")
            target_mask = (self.all_stars_gid==tgid)

            target_stars_gid = self.all_stars_gid[target_mask]
            target_star_position = self.all_star_position[target_mask]
            target_star_mass = self.all_star_mass[target_mask]
            target_star_ids = self.all_star_ids[target_mask]

            # LABLE MAP
            image,uedges,vedges,pr_mode,u,v = self._get_projection_img(target_star_position,target_star_mass,"XY","mass")
            finder = BlobFinder(image)
            cvout = finder.opencv_findblobs()
            cvout["TARGET_GID"] = tgid
            cvout["TARGET_STAR_COUNT"] = len(target_stars_gid)
            cvout["TARGET_STAR_MASS"] = np.sum(target_star_mass)
            cvout["PROJECTION_MODE"] = pr_mode
            # finder.show_opencv_pipeline(cvout)

            # print(cvout["MFRAC_LABLE"])


            # GATHER SPECTRUM
            lable_map = cvout["LABLE_IMG"]
            specout = self.gather_spectrum(lable_map,u,v,uedges,vedges,target_star_ids,target_star_mass)
            


            # BLOBWISE
            # for i,spec in enumerate(specout["BLOBWISE_SPECTRA_WITH_NEBULAR"]):
            #     propout.append(self._get_spec_properties_obs(specout["WAVELENGTH_WITH_NEBULAR"]))
            
            # self.show_spectrum(specout,propout)
            

            # if DUMP:
            #     for so,po in zip(specout,propout):
            #         np.savetxt(outfile_fp,
            #                    np.column_stack([
            #                        tgid,propout["PHOTO"]["M_AB_F115W"]
            #                        ]),
            #                    fmt="%d %.4f")
            #         pass
                    
            #         outfile_fp.flush()






            # SUMMED
            wl_rest = specout["WAVELENGTH_WITH_NEBULAR"]
            summed_spec = np.zeros_like(wl_rest)
            for i,spec in enumerate(specout["BLOBWISE_SPECTRA_WITH_NEBULAR"]):
                # propout.append(self._get_spec_properties_obs(specout["WAVELENGTH_WITH_NEBULAR"]))
                # if i==0:continue
                summed_spec += spec
            
            
            propout=self._get_spec_properties_observed(wl_rest,summed_spec)
            
            # print(f"\nLuminosity from MD : {LUV[tgid-1]:.02e} erg s-1 Hz-1 *")
            # print(f"Flux from MD : {fUV[tgid-1]:.02e}  erg s-1 cm-2 Hz-1 *")
            # print(f"AB Magnitude from MD : {M_AB[tgid-1]:.02f}")

            # self.show_spectrum(wl_obs,spec_obs,
            #                    [
            #                        propout["PHOTO"]["F070W"],
            #                        propout["PHOTO"]["F090W"],
            #                        propout["PHOTO"]["F115W"],
            #                        propout["PHOTO"]["F150W"],
            #                        propout["PHOTO"]["F200W"],
            #                        propout["PHOTO"]["F277W"],
            #                        propout["PHOTO"]["F356W"],
            #                        propout["PHOTO"]["F444W"]
            #                     ])

            # print(propout["PHOTO"]["M_AB_F115W"])
            # print("MD",M_AB[tgid-1])

            if DUMP:
                if rownum==0:
                    outfile_fp.write("# RF : REST FRAME\n# OF : OBSERVED FRAME\n# IRF : INFERED REST FRAME\n")
                    outfile_fp.write("# TGID "+" ".join(propout.keys())+"\n")

                rowval = [rownum+1,tgid] + [v for v in propout.values()]
                fmt = "%d %d %.4e %.4e %.4e %.4f %.4e %.4e %.4e %.4e %.4e %.4e %.4e %.4e"
                
                np.savetxt(outfile_fp,np.column_stack(rowval),fmt=fmt)
                outfile_fp.flush()




        if DUMP:
            outfile_fp.close()
