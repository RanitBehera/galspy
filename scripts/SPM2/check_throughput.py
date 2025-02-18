import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d



torest = True
z=7

filter_name = "F115W"
FILTER_PATH = f"/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/module_scripts/bagpipes/filters/jwst/{filter_name}"
fl_wl,throuput = np.loadtxt(FILTER_PATH).T
if torest:
    fl_wl = fl_wl/(1+z)
throuput_interpolate_fun = interp1d(fl_wl,throuput,"linear",fill_value="extrapolate")

wl=np.array(range(1,3001))
throuput_interpolated    = throuput_interpolate_fun(wl) 


plt.plot(wl,throuput_interpolated)

plt.show()