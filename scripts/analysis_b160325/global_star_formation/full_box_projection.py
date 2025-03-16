import galspy
import numpy as np
import matplotlib.pyplot as plt
import os
from galspy.utility.visualization import CubeVisualizer
from astropy.cosmology import FlatLambdaCDM
from matplotlib.patches import Rectangle
from scipy.ndimage import gaussian_filter



SNAPSPATH = "/mnt/home/student/cranit/NINJA/simulations/L150N2040/SNAPS/"
SNAPNUM=75

ROOT = galspy.NavigationRoot(SNAPSPATH)



TPART = ROOT.PART(SNAPNUM)
TPIG = ROOT.PIG(SNAPNUM)

# Get available previos snaps
snaps = sorted([c for c in os.listdir(SNAPSPATH) if c.startswith("PART") and os.path.isdir(os.path.join(SNAPSPATH, c))])
sn = np.array([int(s.split('_')[-1]) for s in snaps])
mask = sn<=SNAPNUM
sn = sn[mask]
sn=sn[4:]

BOXSIZE = 150000


for i,sni in enumerate(sn):
    if sni not in [75]:continue
    print(i+1,"/",len(sn),":",sni)
    PSNAP = ROOT.PART(int(sni))
    
    # ===== GLOBAL BOX
    pstar_ids = PSNAP.Star.ID()
    pstar_pos = PSNAP.Star.Position()
    pstar_ids = pstar_ids.astype(np.int64)

    x,y,z = pstar_pos.T

    plt.figure("FullBox",figsize=(5,5))
    hist,_,_ = np.histogram2d(x,y,bins=(4000,4000))
    hist = (hist/np.max(hist))**0.01
    plt.imshow(hist.T,cmap="gist_yarg",extent=(0,BOXSIZE/1000,0,BOXSIZE/1000),origin='lower')
    plt.xticks([])
    plt.yticks([])
    plt.tight_layout()

    # ===== ZOOM-1 REGION
    FX,FY = [98000,100000]
    R = 5000
    rect = Rectangle(((FX-R)/1000, (FY-R)/1000), 2*R/1000, 2*R/1000, linewidth=1, edgecolor='r', facecolor='none')
    plt.gca().add_patch(rect)

    maskx = (x>FX-R) & (x<FX+R)
    masky = (y>FY-R) & (y<FY+R)
    mask = maskx & masky
    mx,my,mz = x[mask]-(FX-R), y[mask]-(FY-R) , z[mask] 

    plt.figure("Zoom1",figsize=(5,5))
    hist,_,_ = np.histogram2d(mx,my,bins=(1000,1000))
    hist=np.log10(1+hist)
    hist = (hist/np.max(hist))**0.5
    plt.imshow(gaussian_filter(hist.T,sigma=0.2),cmap="gist_yarg",extent=(0,2*R/1000,0,2*R/1000),origin='lower')
    plt.xticks([])
    plt.yticks([])
    plt.tight_layout()



    # ===== ZOOM-2 REGIONS
    FX1,FY1 = [5000,6000]
    R1 = 1000
    rect1 = Rectangle(((FX1-R1)/1000, (FY1-R1)/1000), 2*R1/1000, 2*R1/1000, linewidth=1, edgecolor='r', facecolor='none')
    plt.gca().add_patch(rect1)

    FX2,FY2 = [2700,2100]
    R2 = 1000
    rect2 = Rectangle(((FX2-R2)/1000, (FY2-R2)/1000), 2*R2/1000, 2*R2/1000, linewidth=1, edgecolor='r', facecolor='none')
    plt.gca().add_patch(rect2)

    maskx1 = (mx>FX1-R1) & (mx<FX1+R1)
    masky1 = (my>FY1-R1) & (my<FY1+R1)
    mask1 = maskx1 & masky1
    mx1,my1,mz1 = mx[mask1]-FX1, my[mask1]-FY1 , mz[mask1] 

    maskx2 = (mx>FX2-R2) & (mx<FX2+R2)
    masky2 = (my>FY2-R2) & (my<FY2+R2)
    mask2 = maskx2 & masky2
    mx2,my2,mz2 = mx[mask2]-FX2, my[mask2]-FY2 , mz[mask2]


    plt.figure("Zoom2_1",figsize=(5,5))
    hist,_,_ = np.histogram2d(mx1,my1,bins=(512,512))
    hist=np.log10(1+hist)
    hist = (hist/np.max(hist))**0.5
    plt.imshow(gaussian_filter(hist.T,sigma=0.8),cmap="gist_yarg",extent=(0,2*R1/1000,0,2*R1/1000),origin='lower')
    plt.xticks([])
    plt.yticks([])
    plt.tight_layout()


    plt.figure("Zoom2_2",figsize=(5,5))
    hist,_,_ = np.histogram2d(mx2,my2,bins=(512,512))
    hist=np.log10(1+hist)
    hist = (hist/np.max(hist))**0.5
    plt.imshow(gaussian_filter(hist.T,sigma=0.8),cmap="gist_yarg",extent=(0,2*R2/1000,0,2*R2/1000),origin='lower')
    plt.xticks([])
    plt.yticks([])
    plt.tight_layout()






    plt.show()