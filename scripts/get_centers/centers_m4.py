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
all_star_gid  = PIG.Star.GroupID()
all_star_mass = PIG.Star.Mass()
all_star_pos  = PIG.Star.Position()
all_star_vel  = PIG.Star.Velocity()
all_star_gen  = PIG.Star.Generation()
all_star_sft  = PIG.Star.StarFormationTime()
all_star_sml  = PIG.Star.SmoothingLength()


class PointSet:
    def __init__(self,gid,mass,pos,vel=None,gen=None,sft=None,sml=None):
        self.gid=gid
        self.mass=mass
        self.pos=pos
        self.vel=vel
        self.gen=gen
        self.sft=sft
        self.sml=sml

    def Get_SubSet(self,mask):
        return PointSet(self.gid[mask],self.mass[mask],self.pos[mask],self.vel[mask],self.gen[mask],self.sft[mask],self.sml[mask])

def PointSetFromGID(target_gid):
    gmask = (all_star_gid==target_gid)
    gid  = all_star_gid[gmask]
    mass = all_star_mass[gmask]  
    pos  = all_star_pos[gmask] 
    vel  = all_star_vel[gmask] 
    gen  = all_star_gen[gmask] 
    sft  = all_star_sft[gmask] 
    sml  = all_star_sml[gmask]
    return PointSet(gid,mass,pos,vel,gen,sft,sml)


def Show_PointSet(ps:PointSet):
    plt.figure()
    cv=CubeVisualizer()
    cv.add_points(ps.pos,points_color='k')
    return cv.show(False)
    
def Get_SpreadAxis(ps:PointSet):
    x,y,z=ps.pos.T
    return np.int32(np.argmax([np.std(x),np.std(y),np.std(z)]))

def Get_Span(ps:PointSet):
    x,y,z=ps.pos.T
    return np.ptp(x),np.ptp(y),np.ptp(z)

def Get_Edge(ps:PointSet,axisno=None,bins=None,apply_log10=True):
    if axisno==None:
        axisno=int(Get_SpreadAxis(ps))
        
    data=ps.pos.T[axisno]
    
    if bins==None:
        BINSIZE=0.5#ckpc
        bins=int(np.ptp(data)/BINSIZE)
    
    hist, bin_edges = np.histogram(data,bins=bins)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    signal = hist
    
    if apply_log10:
        signal = np.log10(signal+1)

    signal = gaussian_filter(signal, sigma=2)
    digital=np.where(signal<0.4,0,1)

    sobel_filter = np.array([-1, 0, 1])
    edge_triggers = np.abs(np.convolve(digital, sobel_filter, mode='same'))
    edges = np.average(bin_centers[edge_triggers>0].reshape(-1,2),axis=1)
    edge_pairs = edges.reshape(-1,2)

    return edge_pairs,axisno

def Get_Blocks(ps:PointSet,axisno=None,bins=None,apply_log10=True):
    ep,ax = Get_Edge(ps,axisno,bins,apply_log10)
    cdn = ps.pos.T[ax]
    blocks=[]
    for (l,r) in ep:
        mask=(cdn>l)&(cdn<r)
        new_ps = ps.Get_SubSet(mask)
        blocks.append(new_ps)
    return blocks


# def Get_ProjectedHistogram(ps:PointSet,axisno=None,bins=None,apply_log10=True):
#     if axisno==None:
#         axisno=int(Get_SpreadAxis(ps))
        
#     data=ps.pos.T[axisno]
    
#     if bins==None:
#         BINSIZE=0.5#ckpc
#         bins=int(np.ptp(data)/BINSIZE)
    

#     hist, bin_edges = np.histogram(data,bins=bins)
#     bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
#     signal = hist
    
#     if apply_log10:
#         signal = np.log10(signal+1)

#     signal = gaussian_filter(signal, sigma=2)
#     signal=np.where(signal<0.5,0,1)

#     # peaks_idx,_ = find_peaks(signal,prominence=0.3)
#     # peaks = bin_centers[peaks_idx]
#     # return bin_centers,signal,peaks
#     return bin_centers,signal

# def Show_ProjectedHistogram(bin_center,bin_count,peaks=None):
#     plt.figure("Projection")
#     plt.plot(bin_center,bin_count)
    # for p in peaks:
        # pass
        # plt.axvline(p,color='k',lw=1)


# =====================================================
TID = 1
ps= PointSetFromGID(TID)
Show_PointSet(ps)
blocks=Get_Blocks(ps)

for nps in blocks:
    Show_PointSet(nps)


# Get_ProjectedHistogram(ps)

plt.show()



