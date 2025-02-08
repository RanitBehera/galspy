import galspy
import numpy as np
import astropy
from scipy.signal import convolve2d
from typing import Literal
import matplotlib.pyplot as plt
import cv2 as cv
from typing import List

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

    def GetProjection(self,direction:Literal["XY","YZ","ZX"]="XY"):
        if direction not in ["XY","YZ","ZX"]:
            raise ValueError("Invalid Direction")

        x,y,z = self.position.T
        if direction=="XY": u,v = x,y
        elif direction=="YZ": u,v = y,z
        elif direction=="ZX": u,v = z,x

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

        height,uedges,vedges=np.histogram2d(u,v,bins=(bin_edges_u,bin_edges_v))
        return height


    def FindBlobs(self,img):
        # Foreground should be white and background should be black.
        TH_MIN_STAR_COUNT = 2
        img_th = np.where(img>=TH_MIN_STAR_COUNT,img,0)
        img_th  = img_th.astype(np.uint8)

        # ----- BINARY
        TH_BIN = 0
        _,binary = cv.threshold(img.astype(np.uint8),TH_BIN,255,cv.THRESH_BINARY)
        _,binary_th = cv.threshold(img_th,TH_BIN,255,cv.THRESH_BINARY)

        # ----- MORPHOLOGICAL TRANSFORMATIONS
        # CLOSING - (dilation followed by erosion) : Black dots gets erased
        kernel = np.ones((2,2),np.uint8)
        closed = cv.morphologyEx(binary_th, cv.MORPH_CLOSE, kernel)
        # OPENING - (erosion followed by dilation) : White dots gets erased
        kernel = np.ones((3,3),np.uint8)
        opened = cv.morphologyEx(closed, cv.MORPH_OPEN, kernel)
        # DILATION - Nearby mini-islands gets connected
        kernel = np.ones((10,10),np.uint8)
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


        # ----- OVERLAY
        overlay_blob = cv.cvtColor(target_img,cv.COLOR_GRAY2BGR)
        overlay_img = cv.cvtColor(binary_th,cv.COLOR_GRAY2BGR)
        for key in keypoints:
            key:cv.KeyPoint
            center,diameter,angle = key.pt,key.size,key.angle
            center = (int(center[0]), int(center[1]))
            radius = int(diameter/2)+2
            cv.circle(overlay_blob,center,radius,(255,0,0),1,cv.LINE_AA)
            cv.circle(overlay_img,center,radius,(255,0,0),1,cv.LINE_AA)

        
        return {
            "INPUT_IMG"     : img,
            "BINARY_IMG"    : binary,
            "BINARY_TH_IMG" : binary_th,
            "MORPH_CLOSED"  : closed,
            "MORPH_OPENED"  : opened,
            "MORPH_DILATED" : dilated,
            "OVERLAY_BLOB"   : overlay_blob,
            "OVERLAY_IMG"   : overlay_img,
            # "LABEL_IMG"     : label_img,
            # ---
            "BLOB_COUNT"    : len(keypoints),
            "TH_MIN_STAR_COUNT" : TH_MIN_STAR_COUNT
        }
            




    def OpenCVPostProcessOld(self,img):
        # Foreground should be white and background should be black.
        TH_MIN_STAR_COUNT = 2
        img_th = np.where(img>=TH_MIN_STAR_COUNT,img,0)

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
        label_img = -1*np.ones(binary.shape, dtype=int)
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
                    label_img[y,x]=ellipse_index

            ellipse_index += 1

            # Draw Overlays
            cv.ellipse(overlay_img, center,axes,-angle, 0,365,(0, 0, 255), 1)
            cv.line(overlay_img, center, (major_axis_end), (0, 255, 0), 1)
            cv.line(overlay_img, center, (minor_axis_end), (255, 0, 0), 1)
            cv.rectangle(overlay_img,(min_x,min_y),(max_x,max_y),(255,255,255),1)



        overlay_img = cv.cvtColor(overlay_img,cv.COLOR_BGR2RGB)


        return {
            "INPUT_IMG"     : img,
            "BINARY_IMG"    : binary,
            "BINARY_TH_IMG" : binary_th,
            "MORPH_CLOSED"  : closed,
            "MORPH_OPENED"  : opened,
            "MORPH_DILATED" : dilated,
            "OVERLAY_IMG"   : overlay_img,
            "LABEL_IMG"     : label_img,
            # ---
            "BLOB_COUNT"    : ellipse_index,
            "TH_MIN_STAR_COUNT" : TH_MIN_STAR_COUNT
        }
    

    def ShowOpenCVPipeline(self,cvout=None,mode:Literal["all","major"]="major"):
        if cvout==None:
            mg = cm.GetProjection()
            cvout = cm.OpenCVPostProcess(img)
        
        if mode=="all":
            fig,axs = plt.subplots(2,4,figsize=(9,6),sharex=True, sharey=True)
            axs:np.ndarray
            axs=axs.flatten()
        elif mode=="major":
            fig,axs = plt.subplots(1,3,figsize=(9,6),sharex=True, sharey=True)

        iter_axs=iter(axs)
        def next_ax():
            return next(iter_axs)
        
        if mode in ["all"]:
            ax:plt.Axes=next_ax()    
            ax.imshow(cvout["INPUT_IMG"].T,origin='lower',cmap="grey")
            ax.set_title("Projection Original")

        if mode in ["all","major"]:
            ax=next_ax()    
            ax.imshow(cvout["BINARY_IMG"].T,origin='lower',cmap="grey")
            ax.set_title(f"Binary")

        if mode in ["all","major"]:
            ax=next_ax()    
            ax.imshow(cvout["BINARY_TH_IMG"].T,origin='lower',cmap="grey")
            ax.set_title(f"Binary Thresold : S={cvout['TH_MIN_STAR_COUNT']}")

        if mode in ["all"]:
            ax=next_ax()    
            ax.imshow(cvout["MORPH_CLOSED"].T,origin='lower',cmap="grey")
            ax.set_title(f"Morphological (Closed)")
        
        if mode in ["all"]:
            ax=next_ax()    
            ax.imshow(cvout["MORPH_OPENED"].T,origin='lower',cmap="grey")
            ax.set_title(f"Morphological (Opened)")

        if mode in ["all"]:
            ax=next_ax()    
            ax.imshow(cvout["MORPH_DILATED"].T,origin='lower',cmap="grey")
            ax.set_title(f"Morphological (Dilation)")

        if mode in ["all"]:
            ax=next_ax()    
            ax.imshow(np.transpose(cvout["OVERLAY_BLOB"],(1,0,2)),origin='lower')
            ax.set_title(f"Overlay : N={cvout['BLOB_COUNT']}")
        
        if mode in ["all","major"]:
            ax=next_ax()    
            ax.imshow(np.transpose(cvout["OVERLAY_IMG"],(1,0,2)),origin='lower')
            ax.set_title(f"Overlay : N={cvout['BLOB_COUNT']}")


        for ax in axs:
            ax.set_axis_off()


        # plt.tight_layout()
        plt.show()



SNAPSPATH = "/mnt/home/student/cranit/NINJA/simulations/L150N2040/SNAPS/"
SNAPNUM = 43

stellar_mass = galspy.NavigationRoot(SNAPSPATH).PIG(SNAPNUM).FOFGroups.MassByType().T[4]


##%%
for i in range(1,100):
    if i not in [1,7]:continue
    print(i)
    st_mass = stellar_mass[i-1]
    print("  ","Stellar Mass :",st_mass,"e10")


    cm = ClumpManager(SNAPSPATH,SNAPNUM,i)
    img = cm.GetProjection()
    cvout = cm.FindBlobs(img)
    cm.ShowOpenCVPipeline(cvout,"major")
    # cm.ShowCube()



    # PLOT
    

