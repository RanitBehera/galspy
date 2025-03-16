import numpy as np
import bagpipes as pipes
import matplotlib.pyplot as plt
import os


# ------------------------------------
def load_data(ID:str):
    # Temporary now
    # Later relate to sim gid
    photometry = np.loadtxt("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/module_scripts/bagpipes/data/demo_model.phot")
    return photometry


# ------------------------------------
filt_list = np.loadtxt("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/module_scripts/bagpipes/filters/myfilters.txt", dtype="str")

# phot_units to 'ergscma' is important as default is myJy and it messes the input values
galaxy = pipes.galaxy("17433", load_data, spectrum_exists=False, filt_list=filt_list,phot_units="ergscma")
pwave,pflux,pflux_err = galaxy.photometry.T

galaxy.plot()
# ------------------------------------
# FIT INSTRUCTIONS
# ------------------------------------
exp = {}
exp["age"] = (0.1, 0.5)
exp["tau"] = (0.5, 1.0)
exp["massformed"] = (7, 11.)
exp["metallicity"] = (0., 2.5)

dust = {}
dust["type"] = "Calzetti"
dust["Av"] = (0., 2.)

fit_instructions = {}
fit_instructions["redshift"] = (5, 10.)
fit_instructions["exponential"] = exp   
fit_instructions["dust"] = dust


# ------------------------------------
fit = pipes.fit(galaxy, fit_instructions)
fit.fit(verbose=False)


# ------------------------------------
fig = fit.plot_spectrum_posterior(save=False, show=True)
fig = fit.plot_sfh_posterior(save=False, show=True)
fig = fit.plot_corner(save=False, show=True)

















