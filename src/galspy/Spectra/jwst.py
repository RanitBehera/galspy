from typing import Literal
import numpy as np
from scipy.interpolate import interp1d

_AVAIL_JWST_FILTERS = [
        "F150W2","F322W2",
        "F070W","F090W","F115W","F150W","F200W","F277W","F356W","F444W",
        "F140M","F162M","F182M","F210M","F250M","F300M","F335M","F360M","F410M","F430M","F460M","F480M",
        "F164N","F187N","F212N","F323N","F405N","F466N","F470N"
    ]

_AVAIL_JWST_FILTERS_HINT = Literal[
        "F150W2","F322W2",
        "F070W","F090W","F115W","F150W","F200W","F277W","F356W","F444W",
        "F140M","F162M","F182M","F210M","F250M","F300M","F335M","F360M","F410M","F430M","F460M","F480M",
        "F164N","F187N","F212N","F323N","F405N","F466N","F470N"
    ]

FILTERS_DIR="/mnt/home/student/cranit/RANIT/Repo/galspy/cache/filters/jwst"

def get_NIRCam_filter(wl,filter_name:_AVAIL_JWST_FILTERS_HINT="F115W",normalise=True):
    FILTER_PATH = f"{FILTERS_DIR}/{filter_name}"
    fl_wl,throuput = np.loadtxt(FILTER_PATH).T
    throuput_interpolate_fun = interp1d(fl_wl,throuput,"linear",fill_value="extrapolate")
    throuput_interpolated    = throuput_interpolate_fun(wl) 
    
    if normalise:
        dlam=np.diff(wl)
        throuput_interpolated /=np.sum(throuput_interpolated[:-1]*dlam)
    
    return throuput_interpolated
    # Although cloudy resampling gives dlam~1e9 for last bin, the flux is 1e20 order of magnitude less.
    # Hence the last bin area is 10 order or magnitude less
    # So we can neglect the area contribution from the last bin 