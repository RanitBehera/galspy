import galspy
import numpy,os
import matplotlib.pyplot as plt
from galspec.SPM import SpectroPhotoMetry
from concurrent.futures import ThreadPoolExecutor

# MPGADGET_OUTPUT_DIR = "/mnt/home/student/cranit/Data/MP_Gadget/Nishi/L50N640"
MPGADGET_OUTPUT_DIR = "/mnt/home/student/cranit/NINJA/simulations/L150N2040/SNAPS"
SNAP_NUM = 43
GROUP_OFFSET = 0

print("SPM")

root = galspy.NavigationRoot(MPGADGET_OUTPUT_DIR)
PIG = root.PIG(SNAP_NUM)


def DoFor(GO):
    spm=SpectroPhotoMetry(MPGADGET_OUTPUT_DIR,SNAP_NUM)
    spm.target_PIG_Group(1+GO)
    # spm.target_PIG_Group(1+GROUP_OFFSET,100,[-43,-20,-30])
    # spm.target_PIG_Group(1+GROUP_OFFSET,1,[0,0,0])
    # spm.show_region()

    # spm.show_mass_metallicity_scatter()

    spm.project_to_plane()
    # spm.show_projected_points()

    spm.generate_pixelwise_grid(grid_resolution=(1,1),mode="NGB")
    # spm.generate_pixelwise_grid(grid_resolution=(1,1),mode="NGB")
    # spm.show_star_mass_map()
    # spm.show_pixelwise_histogram()
    # spm.show_pixelwise_spectra()

    # spm.show_rgb_channels([1450,2500,4450],[100,100,100])
    # spm.show_uv_channels(1200,2600)

    MAB_S,MAB_T=spm.get_MAB(1200,2600,1400)

    return MAB_S,MAB_T


# ===============
FILE = "/mnt/home/student/cranit/RANIT/Repo/galspy/study/LuvAB/MUVAB.txt"
with open(FILE, 'a') as f:
    f.write("#PIGID STAR TOTAL\n")

for g in range(0,10+1):
    # print("GID :",g)
    try:
        S,T = DoFor(g)
    except:
        S,T=0,0
    
    with open(FILE, 'a') as f:
        numpy.savetxt(f, numpy.column_stack((g,S,T)), fmt='%d %.02f %.02f')

