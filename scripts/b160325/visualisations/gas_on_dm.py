import galspy
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

from galspy.utility.visualization import CubeVisualizer



SNAPSPATH = "/mnt/home/student/cranit/NINJA/simulations/L150N2040/SNAPS/"
SNAPNUM=75
PIG = galspy.NavigationRoot(SNAPSPATH).PIG(SNAPNUM)
print("Reading ...")
all_star_gid  = PIG.Star.GroupID()
all_star_mass = PIG.Star.Mass()
all_star_pos  = PIG.Star.Position()


DM=False

all_dm_gid  = PIG.DarkMatter.GroupID()
all_dm_mass = PIG.DarkMatter.Mass()
all_dm_pos  = PIG.DarkMatter.Position()
print("Done")


# delta = 0.165*(1+7)*0.6736
delta=0.5


def PostProcess(img,convolve=True,mask_count=1):
    if convolve:
        kernel = np.array([[0.25,0.25],[0.25,0.25]])
        img = signal.convolve2d(img,kernel,"same")

    # img = np.where(img>mask_count,img,0)

    img=np.log10(1+img)
    img=(img/np.max(img))**0.5
    
    return img #+ np.maximum(np.random.normal(0.1,0.04,img.shape),0)


def GetImage(tgid):
    tdm_pos = all_dm_pos[all_dm_gid==tgid]
    x,y,z=tdm_pos.T
    ox,oy,oz = np.min(x),np.min(y),np.min(z)
    x,y,z=x-ox,y-oy,z-oz

    sx,sy,sz=np.max(x),np.max(y),np.max(z)
    Nx,Ny,Nz=np.int64(sx/delta),np.int64(sy/delta),np.int64(sz/delta)

    XE = np.linspace(0,sx,Nx)
    YE = np.linspace(0,sy,Ny)
    XM,YM = np.meshgrid(XE,YE)




    tstar_pos = all_star_pos[all_star_gid==tgid]
    ts_x,ts_y,ts_z = tstar_pos.T
    ts_x,ts_y,ts_z = ts_x-ox,ts_y-oy,ts_z-oz


    hist, xedges, yedges = np.histogram2d(x, y, bins=(XE,YE))
    hist_s, xedges_s, yedges_s = np.histogram2d(ts_x, ts_y, bins=(XE,YE))


    dm_img = PostProcess(hist)
    dm_star = PostProcess(hist_s)


    plt.clf()

    SAVEPATH = "/mnt/home/student/cranit/RANIT/Repo/galspy/temp/share_fund/dm_and_stars"
    plt.imshow(dm_img,cmap="gist_grayl")
    plt.xticks([])
    plt.yticks([])
    plt.tight_layout()
    plt.savefig(f"{SAVEPATH}/PIG{SNAPNUM}_GID{tgid}_pxy_dm.png")

    plt.imshow(dm_star,cmap="gist_gray")
    plt.xticks([])
    plt.yticks([])
    plt.tight_layout()
    plt.savefig(f"{SAVEPATH}/PIG{SNAPNUM}_GID{tgid}_pxy_star.png")
    
    plt.close()



for i in range(1,50):
    print(i)
    try:
        GetImage(i)
    except:
        print("Error")




