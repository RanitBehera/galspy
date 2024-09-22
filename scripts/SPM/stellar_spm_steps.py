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
spm.target_PIG_Group(1+GROUP_OFFSET,1)
# spm.show_region()


spm.project_to_plane()
spm.show_projected_points()

# spm.generate_grid(grid_resolution=(50,50),mode="NGB")
# spm.show_interpolated_masni Vs_grid_image()
# spm.show_age_distribution()
# spm.show_spectra()







