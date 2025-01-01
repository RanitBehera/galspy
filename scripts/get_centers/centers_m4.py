import galspy
import numpy as np
import matplotlib.pyplot as plt
from galspy.utility.visualization import CubeVisualizer
import galspy.MPGadget
from matplotlib.gridspec import GridSpec
from scipy.spatial import KDTree
from scipy.ndimage import gaussian_filter
from scipy.signal import find_peaks



SNAPSPATH = "/mnt/home/student/cranit/NINJA/simulations/L150N2040/SNAPS/"
SNAPNUM=43
PIG = galspy.NavigationRoot(SNAPSPATH).PIG(SNAPNUM)
all_star_gid = PIG.Star.GroupID()
all_star_pos = PIG.Star.Position()
all_star_vel = PIG.Star.Velocity()
all_star_gen = PIG.Star.Generation()
all_star_sft = PIG.Star.StarFormationTime()
all_star_sml = PIG.Star.SmoothingLength()

class GalFind:
    def __init__(self,target_gig):
        gmask = (all_star_gid==target_gig)
        self.gid = all_star_gid[gmask] 
        self.pos = all_star_pos[gmask] 
        self.vel = all_star_vel[gmask] 
        self.gen = all_star_gen[gmask] 
        self.sft = all_star_sft[gmask] 
        self.sml = all_star_sml[gmask]
    


def Show_PIGStars(pos):
    plt.figure()
    cv=CubeVisualizer()
    cv.add_points(pos,points_color='k')
    return cv.show(False)
    
def Get_SpreadAxis(pos):
    x,y,z=pos.T
    sig_x = np.std(x)
    sig_y = np.std(y)
    sig_z = np.std(z)
    return np.argmax([sig_x,sig_y,sig_z])

def Get_Span(pos):
    x,y,z=pos.T
    sx,sy,sz=np.ptp(x),np.ptp(y),np.ptp(z)
    return sx,sy,sz

def Get_LowSmoothingLength(pos,sml,sml_cut):
    mask=sml<=sml_cut
    return pos[mask]

def Get_ProjectedHistogram(pos,axisno,bins,apply_log10=True):
    data=pos.T[axisno]
    hist, bin_edges = np.histogram(data,bins=bins)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    signal = hist
    if apply_log10:
        signal = np.log10(signal+1)
    signal = gaussian_filter(signal, sigma=2,mode="constant")
    peaks_idx,_ = find_peaks(signal,prominence=0.2)
    peaks = bin_centers[peaks_idx]
    return bin_centers,signal,peaks

def Show_ProjectedHistogram(bin_center,bin_count,peaks):
    plt.figure("Projection")
    plt.plot(bin_center,bin_count)
    for p in peaks:
        plt.axvline(p,color='k',lw=1)


# =====================================================
TID = 1
g = GalFind(TID)

Show_PIGStars(g.pos)
sa=Get_SpreadAxis(g.pos)
print(sa)
cen,count,peak = Get_ProjectedHistogram(g.pos,sa,1000)
Show_ProjectedHistogram(cen,count,peak)
print(Get_Span(g.pos))

# ------------------
# spos=Get_LowSmoothingLength(g.pos,g.sml,np.sort(g.sml)[int(0.95*len(g.sml))])
# sa=Get_SpreadAxis(spos)
# print(sa)
# cen,count,peak =Get_ProjectedHistogram(spos,sa,500)
# Show_ProjectedHistogram(cen,count,peak)
# Show_PIGStars(spos)

plt.show()