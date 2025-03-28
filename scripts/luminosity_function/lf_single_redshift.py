import matplotlib.pyplot as plt
import numpy as np
import galspy as gs
from matplotlib.gridspec import GridSpec
from load_observation import load_obs_to_axis
from load_lum_function import load_lf_to_axis

REDSHIFT = 7
load_obs_to_axis(plt.gca(),REDSHIFT,["Bouwens+21"])
load_lf_to_axis(plt.gca(),REDSHIFT,"/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/light_generation/data")

plt.yscale("log")
plt.legend()
plt.show()






