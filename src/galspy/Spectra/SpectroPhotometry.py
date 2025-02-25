import numpy as np
import astropy
from scipy.signal import convolve2d
from typing import Literal
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import cv2 as cv
from typing import List
import pickle
from galspy.Utility import Cube3D
from scipy.interpolate import interp1d
from galspy.MPGadget import _PIG
from galspy.Spectra import SpectralTemplates
from astropy.cosmology import FlatLambdaCDM

class BlobFinder:
    def __init__(self,img):
        self.target_img = img


    def show_image(self,img,label=""):
        plt.imshow(img.T**0.02,origin="lower")
        plt.gca().set_aspect("equal")
        plt.show()

    def opencv_blobfinder(self,thresold=0):
        img=self.target_img

        print("max=",np.max(img))

        # Foreground should be white and background should be black.
        THRESOLD = thresold
        img_th = np.where(img>=THRESOLD,img,0)
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

        
        return {
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
        




class PIGSpectrophotometry:
    _specs_stellar = None
    _specs_total = None
    _phot_F115W_stellar = None
    _phot_F115W_nebular = None

    def __init__(self,PIG:_PIG):
        self.PIG = PIG
        self.all_stars_gid = PIG.Star.GroupID()
        self.all_star_position = PIG.Star.Position()
        self.all_star_mass = PIG.Star.Mass()
        self.all_star_ids = PIG.Star.ID()

        self._specs_template_index = PIG.GetStarsSpecIndex()

        if PIGSpectrophotometry._specs_stellar is None:
            PIGSpectrophotometry._specs_stellar = SpectralTemplates.GetStellarTemplates("CHABRIER_UPTO_300M","Binary")

        if PIGSpectrophotometry._specs_total is None:
            _specs_nebular = SpectralTemplates.GetNebularTemplates("CHABRIER_UPTO_300M","Binary")
            PIGSpectrophotometry._specs_total = PIGSpectrophotometry._specs_stellar + _specs_nebular
            PIGSpectrophotometry._specs_total[0] = _specs_nebular[0]

        self.pixel_resolution = self._get_pixel_resolution()

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

        return binheight,uedges,vedges



    def get_spectrum_dict(self,target_gids):
        if isinstance(target_gids, int) and target_gids > 0:
            target_gids=[target_gids]
        elif isinstance(target_gids, list) and all(isinstance(i, int) and i > 0 for i in target_gids): pass
        else: raise ValueError("Either int or List[int] are valid as target group id with id>0.")

        for tgid in target_gids:
            target_mask = (self.all_stars_gid==tgid)

            target_stars_gid = self.all_stars_gid[target_mask]
            target_star_position = self.all_star_position[target_mask]
            target_star_mass = self.all_star_mass[target_mask]
            target_star_ids = self.all_star_ids[target_mask]

            image,_,_ = self._get_projection_img(target_star_position,target_star_mass,"XY","mass")
            finder = BlobFinder(image)
            cvout = finder.opencv_blobfinder()

            print(cvout["MFRAC_LABLE"])




