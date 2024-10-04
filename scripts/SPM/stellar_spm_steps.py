import galspy
import numpy
import matplotlib.pyplot as plt
from galspec.SPM import SpectroPhotoMetry


MPGADGET_OUTPUT_DIR = "/mnt/home/student/cranit/Data/MP_Gadget/Nishi/L50N640"
MPGADGET_OUTPUT_DIR = "/mnt/home/student/cranit/NINJA/simulations/L150N2040/SNAPS"
SNAP_NUM = 43
GROUP_OFFSET = 0


root = galspy.NavigationRoot(MPGADGET_OUTPUT_DIR)
PIG = root.PIG(SNAP_NUM)

spm=SpectroPhotoMetry(MPGADGET_OUTPUT_DIR,SNAP_NUM)
spm.target_PIG_Group(1+GROUP_OFFSET,30)
# spm.show_region()
# spm.show_mass_metallicity_scatter()

spm.project_to_plane()
# spm.show_projected_points()

spm.generate_pixelwise_grid(grid_resolution=(30,30),mode="NGB")
# spm.show_star_mass_map()
# spm.show_pixelwise_histogram()
# spm.show_pixelwise_spectra()

spm.show_rgb_channels([1450,2500,4450],[100,100,100])





