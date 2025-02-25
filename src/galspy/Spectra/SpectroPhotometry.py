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

    def opencv_blobfinder(self):




class PIGSpectrophotometry:
    _specs_stellar = None
    _specs_total = None
    _phot_F115W_stellar = None
    _phot_F115W_nebular = None

    def __init__(self,PIG:_PIG):
        self.PIG = PIG
        self.all_stars_gid = PIG.Star.GroupID()
        self.all_star_position = PIG.Star.Position()
        self.all_star_mass = PIG.Star.Position()
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
            binheight,uedges,vedges=np.histogram2d(u,v,bins=(bin_edges_u,bin_edges_v),weights=mass,density=False)
        
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


            image,_,_ = self._get_projection_img(target_star_position,target_star_mass)
            finder = BlobFinder(image)




