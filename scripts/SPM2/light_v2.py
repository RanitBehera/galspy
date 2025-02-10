import galspy
import numpy as np
import astropy
from scipy.signal import convolve2d
from typing import Literal
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import cv2 as cv
from typing import List
import pickle
from galspy.utility.visualization import CubeVisualizer

class ClumpManager:
    def __init__(self,snapspath:str,snapnum:int,gid:int):
        self.snapspath = snapspath
        self.snapnum = snapnum
        self.gid = gid 
        if gid<1:
            raise ValueError("Group ID must be greter than or equal to 1.")

        PIG=galspy.NavigationRoot(snapspath).PIG(int(snapnum))
        self.PIG = PIG

        star_gid        = PIG.Star.GroupID()
        target_mask     = star_gid==gid

        self.position   = PIG.Star.Position()[target_mask]
        self.mass       = PIG.Star.Mass()[target_mask]
        self.ids        = PIG.Star.ID()[target_mask]
        self.stellar_mass = np.sum(self.mass) 

        self.pixel_resolution = self._GetPixelResolution(PIG.Header.Redshift())


    def _GetPixelResolution(self,z):
        RB = 0.031          #arcsecond per pixel : JWST 
        RB *= 1/3600        #degree per pixel
        RB *= np.pi/180     #radian per pixel
        sim = galspy.NavigationRoot(self.snapspath)
        cosmo=sim.GetAstropyFlatLCDM()
        DA=cosmo.angular_diameter_distance(z).value #in Mpc
        DA*=1000 #To Kpc
        res = DA * RB   #pKpc per pixel
        res *=(1+z)*self.PIG.Header.HubbleParam()   #cKpc per pixel
        return res
    
    def ShowCube(self):
        cv=CubeVisualizer()
        cv.add_points(self.position)
        cv.show(False)

    def GetProjection(self,direction:Literal["XY","YZ","ZX"]="XY",mode:Literal["count","mass"]="count"):
        self._projection_mode=mode
        if direction not in ["XY","YZ","ZX"]:
            raise ValueError("Invalid Direction")

        x,y,z = self.position.T
        if direction=="XY": u,v = x,y
        elif direction=="YZ": u,v = y,z
        elif direction=="ZX": u,v = z,x
        self._u = u
        self._v = v

        begin_u,begin_v = np.min(u),np.min(v)
        end_u,end_v = np.max(u),np.max(v)
        # span_u,span_v = end_u-begin_u,end_v-begin_v

        pr = self.pixel_resolution
        bin_edges_u = np.arange(begin_u-0.5*pr,end_u+0.5*pr,pr)
        if bin_edges_u[-1]<end_u+0.5*pr:
            np.append(bin_edges_u,bin_edges_u[-1]+pr)
        bin_edges_v = np.arange(begin_v-0.5*pr,end_v+0.5*pr,pr)
        if bin_edges_v[-1]<end_v+0.5*pr:
            np.append(bin_edges_v,bin_edges_v[-1]+pr)
        if mode=="count":
            height,uedges,vedges=np.histogram2d(u,v,bins=(bin_edges_u,bin_edges_v))
        elif mode=="mass":
            height,uedges,vedges=np.histogram2d(u,v,bins=(bin_edges_u,bin_edges_v),weights=self.mass)
        
        self._uedges = uedges
        self._vedges = vedges

        return height,uedges,vedges


    def FindBlobs(self,img):
        # Foreground should be white and background should be black.
        if self._projection_mode=="count":
            THRESOLD = 2
            img_th = np.where(img>=THRESOLD,img,0)
        elif self._projection_mode=="mass":
            THRESOLD = 0.9
            MassUnit=self.PIG.Header.MassTable()[4]
            img_th = np.where(img>=THRESOLD*MassUnit,img,0)
            img_th = 255*(img_th/np.max(img_th))

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
        RADIUS_EXPAND = 2   #by this much pixel
        for key in keypoints:
            key:cv.KeyPoint
            center,diameter,angle = key.pt,key.size,key.angle
            center = (int(center[0]), int(center[1]))
            radius = int(diameter/2)+RADIUS_EXPAND
            BLOB_CENTER.append(center)
            BLOB_RADIUS.append(radius)

        # ----- LABLE MAP
        # Initialise to -1
        lable = -1*np.ones(mask.shape, dtype=int)
        # If mask is positive, initialise to 0, so that outside pixels get lable 0

        for row in range(0,lable.shape[0]):
            for clm in range(0,lable.shape[1]):
                if mask_th[row,clm]>0:lable[row,clm]=0
        
        for i,(C,R) in enumerate(zip(BLOB_CENTER,BLOB_RADIUS)):
            minx,maxx=C[0]-R,C[0]+R
            miny,maxy=C[1]-R,C[1]+R
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
        overlay_img = cv.cvtColor(mask_th,cv.COLOR_GRAY2BGR)
        for center,radius in zip(BLOB_CENTER,BLOB_RADIUS):
            # Center +
            cv.line(overlay_blob, (center[0] - 2, center[1]), (center[0] + 2, center[1]), (255,0,0), 1)
            cv.line(overlay_blob, (center[0], center[1] - 2), (center[0], center[1] + 2), (255,0,0), 1)
            # Perimeter
            cv.circle(overlay_blob,center,radius,(255,0,0),1,cv.LINE_AA)

        
        return {
            "INPUT_IMG"     : img,
            "MASK_BIN"      : mask,
            "MASK_THRESOLD" : mask_th,
            "MORPH_CLOSED"  : closed,
            "MORPH_OPENED"  : opened,
            "MORPH_DILATED" : dilated,
            "OVERLAY_BLOB"  : overlay_blob,
            "OVERLAY_IMG"   : overlay_img,
            "LABLE_IMG"     : lable,
            # --- Pipeline Configuration
            "THRESOLD"              : THRESOLD,
            "CLOSING_KERNEL_SIZE"   : CLOSING_KERNEL_SIZE,
            "OPENING_KERNEL_SIZE"   : OPENING_KERNEL_SIZE,
            "DILATION_KERNEL_SIZE"  : DILATION_KERNEL_SIZE,
            "BLOB_COUNT"            : len(keypoints),
            "BLOB_CENTER"           : BLOB_CENTER,
            "BLOB_RADIUS"           : BLOB_RADIUS,
            "RADIUS_EXPAND"           : RADIUS_EXPAND,
            # --- Mass Fraction After Various Steps
            "MFRAC_MASK_THR" : np.sum(img*np.where(mask_th>0,1,0))/np.sum(img),
            "MFRAC_LABLE" : np.sum(img*np.where(lable>0,1,0))/np.sum(img)
        }
            




    def OpenCVPostProcessOld(self,img:np.ndarray):
        # Foreground should be white and background should be black.
        THRESOLD = 1e-5
        img_th = np.where(img>=THRESOLD,img,0)

        

        # Datatype Cast
        # img     = img.astype(np.uint8)
        img_th  = img_th.astype(np.uint8)

        # Binary
        TH_BIN = 0
        _,binary = cv.threshold(img.astype(np.uint8),TH_BIN,255,cv.THRESH_BINARY)
        _,binary_th = cv.threshold(img_th,TH_BIN,255,cv.THRESH_BINARY)

        # Morphological Operations
        # CLOSING - (dilation followed by erosion) : Black dots gets erased
        kernel = np.ones((2,2),np.uint8)
        closed = cv.morphologyEx(binary_th, cv.MORPH_CLOSE, kernel)
        # OPENING - (erosion followed by dilation) : White dots gets erased
        kernel = np.ones((3,3),np.uint8)
        opened = cv.morphologyEx(closed, cv.MORPH_OPEN, kernel)
        # DILATION - Nearby mini-islands gets connected
        kernel = np.ones((10,10),np.uint8)
        dilated = cv.dilate(opened, kernel,iterations=1)
            


        # Ellipse Fitting
        fit_img = dilated
        overlay_img = cv.cvtColor(binary_th,cv.COLOR_GRAY2BGR)

        contours, hierarchy = cv.findContours(fit_img,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
        lable_img = -1*np.ones(binary.shape, dtype=int)
        ellipse_index = 0
        for contour in contours:
            # Minimum 5 points are required to fit an ellipse
            if len(contour)<5:continue
            ellipse = cv.fitEllipse(contour)
            
            # Extract ellipse parameters
            center, axes, angle = ellipse
            center = (int(center[0]), int(center[1]))
            axes = (int(axes[0]/2 ), int(axes[1]/2 ))
            angle = -angle

            major_axis_end = (int(center[0] + (axes[0])*np.cos(np.deg2rad(angle))),int(center[1] - (axes[0])*np.sin(np.deg2rad(angle))))
            minor_axis_end = (int(center[0] - (axes[1])*np.sin(np.deg2rad(angle))),int(center[1] - (axes[1])*np.cos(np.deg2rad(angle))))


            # Get the bounding box of the ellipse
            max_axis=max(axes)

            min_x = center[0] - max_axis - 4
            max_x = center[0] + max_axis + 4
            min_y = center[1] - max_axis - 4
            max_y = center[1] + max_axis + 4
            
            # Loop over the bounding box and check if the pixel is inside the box
            for y in range(min_y, max_y):
                for x in range(min_x, max_x):
                    lable_img[y,x]=ellipse_index

            ellipse_index += 1

            # Draw Overlays
            cv.ellipse(overlay_img, center,axes,-angle, 0,365,(0, 0, 255), 1)
            cv.line(overlay_img, center, (major_axis_end), (0, 255, 0), 1)
            cv.line(overlay_img, center, (minor_axis_end), (255, 0, 0), 1)
            cv.rectangle(overlay_img,(min_x,min_y),(max_x,max_y),(255,255,255),1)



        overlay_img = cv.cvtColor(overlay_img,cv.COLOR_BGR2RGB)


        return {
            "INPUT_IMG"     : img,
            "MASK_BIN"    : binary,
            "MASK_THRESOLD" : binary_th,
            "MORPH_CLOSED"  : closed,
            "MORPH_OPENED"  : opened,
            "MORPH_DILATED" : dilated,
            "OVERLAY_IMG"   : overlay_img,
            "LABEL_IMG"     : lable_img,
            # ---
            "BLOB_COUNT"    : ellipse_index,
            "THRESOLD" : THRESOLD
        }
    

    def ShowOpenCVPipeline(self,cvout=None,mode:Literal["all","major"]="major"):
        if cvout==None:
            img = self.GetProjection()
            cvout = self.FindBlobs(img)

        if mode=="all":
            fig,axs = plt.subplots(2,4,figsize=(9,6),sharex=True, sharey=True)
            fig.canvas.manager.set_window_title(f'GroupID {self.gid}')
            fig.subplots_adjust(bottom=0.05)
            axs:np.ndarray
            axs=axs.flatten()
        elif mode=="major":
            fig,axs = plt.subplots(1,3,figsize=(9,6),sharex=True, sharey=True)

        iter_axs=iter(axs)
        def next_ax():
            return next(iter_axs)
        
        _FONTSIZE=12


        if mode in ["all"]:
            ax:plt.Axes=next_ax()    
            ax.imshow((np.log10(1+cvout["INPUT_IMG"].T)/np.max(np.log10(1+cvout["INPUT_IMG"].T)))**0.2,origin='lower',cmap="grey")
            JUST=16
            info="Star Count".ljust(JUST) + ":" + f"{len(self.mass)}\n"
            info+="Stellar Mass".ljust(JUST) + ":" + f"{self.stellar_mass:.02f}"+"$\\times 10^{10}\ M_\odot$/h\n"
            info+="Projection Mode".ljust(JUST) + ":" + f"{self._projection_mode}" + "(DRE)"
            ax.set_title(info,fontsize=_FONTSIZE,loc='left',fontname='monospace')

        if mode in ["all","major"]:
            ax=next_ax()    
            ax.imshow(cvout["MASK_BIN"].T,origin='lower',cmap="grey",interpolation='none')
            ax.set_title(f"Binary Mask",fontsize=_FONTSIZE,loc='left',fontname='monospace')

        if mode in ["all","major"]:
            ax=next_ax()    
            ax.imshow(cvout["MASK_THRESOLD"].T,origin='lower',cmap="grey",interpolation='none')
            JUST=16
            info="Thresold Mask\n"
            info+=("Thresold "+self._projection_mode.capitalize()).ljust(JUST) + ":" + f"{cvout['THRESOLD']}\n"
            info+="Mass Fraction".ljust(JUST) + ":" + f"{cvout['MFRAC_MASK_THR']*100:.01f}%"
            ax.set_title(info,fontsize=_FONTSIZE,loc='left',fontname='monospace')

        if mode in ["all"]:
            ax=next_ax()    
            ax.imshow(cvout["MORPH_CLOSED"].T,origin='lower',cmap="grey",interpolation='none')
            JUST=16
            info="Morphological".ljust(JUST) + ":" + "Closed\n"
            info+="Kernel Size".ljust(JUST)+":"+f"{cvout['CLOSING_KERNEL_SIZE']}"
            ax.set_title(info,fontsize=_FONTSIZE,loc='left',fontname='monospace')
        
        if mode in ["all"]:
            ax=next_ax()    
            ax.imshow(cvout["MORPH_OPENED"].T,origin='lower',cmap="grey",interpolation='none')
            JUST=16
            info="Morphological".ljust(JUST) + ":" + "Opened\n"
            info+="Kernel Size".ljust(JUST)+":"+f"{cvout['OPENING_KERNEL_SIZE']}"
            ax.set_title(info,fontsize=_FONTSIZE,loc='left',fontname='monospace')

        if mode in ["all"]:
            ax=next_ax()    
            ax.imshow(cvout["MORPH_DILATED"].T,origin='lower',cmap="grey",interpolation='none')
            JUST=16
            info="Morphological".ljust(JUST) + ":" + "Dilation\n"
            info+="Kernel Size".ljust(JUST)+":"+f"{cvout['DILATION_KERNEL_SIZE']}"
            ax.set_title(info,fontsize=_FONTSIZE,loc='left',fontname='monospace')

        if mode in ["all"]:
            ax=next_ax()    
            ax.imshow(np.transpose(cvout["OVERLAY_BLOB"],(1,0,2)),origin='lower',interpolation='none')
            JUST=16
            info="Blobs Detected".ljust(JUST) + ":" + f"{cvout['BLOB_COUNT']}\n"
            info+="Radius Expansion".ljust(JUST) + ":" + f"{cvout['RADIUS_EXPAND']}px"
            ax.set_title(info,fontsize=_FONTSIZE,loc='left',fontname='monospace')
        
        if mode in ["all","major"]:
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

        # plt.show()

    def ShowBlobwiseSpectra(self,label_map):
        num_blobs = np.max(label_map)
        num_specs = num_blobs+1 #One extra for stray stars

        # Get bin/pixel coordinate
        u_coords = np.digitize(self._u, self._uedges) - 1
        v_coords = np.digitize(self._v, self._vedges) - 1
        u_coords = np.clip(u_coords, 0, len(self._uedges) - 2)
        v_coords = np.clip(v_coords, 0, len(self._vedges) - 2)
        pixel_coords = np.column_stack((u_coords,v_coords))

        with open("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/SPM2/cache/specs.list","rb") as fp:
            specs = pickle.load(fp)
        
        uvspec = specs[:,1400]

        with open("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/SPM2/cache/specindex.dict","rb") as fp:
            specindex = pickle.load(fp)

        tspecindex = [specindex[tsid] for tsid in self.ids]

        light_img = np.zeros_like(label_map)

        for (uc,vc),ti in zip(pixel_coords,tspecindex):
            light_img[uc,vc] += uvspec[ti]

        plt.figure()
        plt.imshow(np.log10(1+light_img).T,cmap="gray",origin="lower")
        plt.show() 


SNAPSPATH = "/mnt/home/student/cranit/NINJA/simulations/L150N2040/SNAPS/"
SNAPNUM = 43

stellar_mass = galspy.NavigationRoot(SNAPSPATH).PIG(SNAPNUM).FOFGroups.MassByType().T[4]


##%%
for i in range(1,100):
    if i not in [1,2]:continue
    print(i)
    st_mass = stellar_mass[i-1]
    print("  ","Stellar Mass :",st_mass,"e10")


    cmgr = ClumpManager(SNAPSPATH,SNAPNUM,i)
    img,ue,ve = cmgr.GetProjection("XY","mass")
    cvout = cmgr.FindBlobs(img)
    cmgr.ShowOpenCVPipeline(cvout,"all")
    # cmgr.ShowCube()
    cmgr.ShowBlobwiseSpectra(cvout["LABLE_IMG"])
    plt.show()


    

