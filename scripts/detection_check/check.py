import galspy
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from scipy.ndimage import maximum_filter


SNAPSPATH = "/mnt/home/student/cranit/NINJA/simulations/L150N2040/SNAPS/"
SNAPNUM=43
PIG = galspy.NavigationRoot(SNAPSPATH).PIG(SNAPNUM)
all_star_gid  = PIG.Star.GroupID()
all_star_mass = PIG.Star.Mass()
all_star_pos  = PIG.Star.Position()


def PostProcessImage(img):
    img=np.log10(1+img)
    img=(img/np.max(img))**0.5
    return img


def FindPeak(img):
    local_max = maximum_filter(img, size=10)
    peaks = (img == local_max)
    return np.array(np.nonzero(peaks)).T


delta = 165*(1+7)*0.6736

def CheckPIG(tgid):
    gmask = all_star_gid==tgid
    tpos = all_star_pos[gmask]
    x,y,z=tpos.T*1000
    x,y,z=x-np.min(x),y-np.min(y),z-np.min(z)
    sx,sy,sz=np.max(x),np.max(y),np.max(z)
    Nx,Ny,Nz=np.int64(sx/delta),np.int64(sy/delta),np.int64(sz/delta)

    hist, xedges, yedges = np.histogram2d(x, y, bins=(Nx,Ny))
    
    plt.figure("Count Projection",figsize=(5,5))
    plt.imshow(PostProcessImage(hist),cmap="gist_gray")
    plt.colorbar()

    # plt.figure("Count Projection with PSF",figsize=(5,5))
    # kernel = np.array([[0.25,0.25],[0.25,0.25]])
    # img = signal.convolve2d(hist,kernel,"same")
    # ppimg = PostProcessImage(img)
    # plt.imshow(ppimg,cmap="gist_gray")
    # # mask=np.int32(hist>1)
    # plt.colorbar()




    # p=FindPeak(ppimg)
    # plt.plot(*p.T,"+",ms=1)


    # X,Y=np.meshgrid(np.arange(0,ppimg.shape[1],1),np.arange(0,ppimg.shape[0],1))
    # plt.contour(X,Y,ppimg,levels=[0.7,0.8,0.9,0.99],colors='m')




    plt.show()    

CheckPIG(1)