import bagpipes as pipes
import numpy as np
import matplotlib.pyplot as plt
import os
from pathlib import Path

# ----------------------------------------
exp = {}                                    # Tau model star formation history component
exp["age"] = 0.3                            #* Gyr
exp["tau"] = 0.75                           #* Gyr
exp["massformed"] = 9.                      # log_10(M*/M_solar)
exp["metallicity"] = 0.5                    # Confir. Seems in units of Z_Solar

# ----------------------------------------
nebular = {}
nebular["logU"] = -1                        #* Log_10 of the ionization parameter.

# ----------------------------------------
dust = {}
dust["type"] = "Calzetti"                   #* Attenuation law: "Calzetti", "Cardelli", "CF00" or "Salim"
dust["Av"] = 0.2                            #* Absolute attenuation in the V band: magnitudes

# ----------------------------------------
model_components = {}
model_components["redshift"] = 7.0          #* Observed redshift
model_components["exponential"] = exp
# model_components["nebular"] = nebular
model_components["dust"] = dust

# ----------------------------------------
myfilters=np.loadtxt("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/module_scripts/bagpipes/filters/myfilters.txt",dtype="str")

# ----------------------------------------
model = pipes.model_galaxy(model_components,
                           spec_wavs=np.arange(9730,45000,5),      # if both side cross thr filter max-&-min waves, gives error. The case is not considered
                           filt_list=myfilters)


# ----------------------------------------
_sfh    = model.sfh
swave,sflux     = model.spectrum.T
pwave,pflux     = model.filter_set.eff_wavs, model.photometry
pflux_err       = 0.05*pflux

# Plot -----------------------------------
if True:
    plt.plot(swave,sflux,c='tab:blue')
    # plt.plot(pwave,pflux,'.',ms=16,mfc='tab:orange',mec='tab:orange')
    # plt.errorbar(pwave,pflux,(pflux*((10**0.02)-1),pflux*(1-(10**-0.02))),fmt='.',ms=20,mfc='tab:orange',mec=None,capsize=4,color='k')
    plt.errorbar(pwave,pflux,pflux_err,fmt='.',ms=20,mfc='tab:orange',mec=None,capsize=4,color='k')

    plt.yscale("log")
    plt.xscale("log")
    plt.xlabel("Observed Wavelength $(\AA)$")
    plt.ylabel("$f_\lambda (ergs s^-1 cm^-2 \AA^-1)$")
    plt.show()


# Export to a file -----------------------
exit()
filedir = str(Path(__file__).parent.absolute())

filepath = filedir + os.sep + "data/demo_model.spec"
np.savetxt(filepath,
            np.column_stack((swave,sflux)),
            header=f'model redshift = {model_components["redshift"]}')
print("Saved To :",filepath)

filepath = filedir + os.sep + "data/demo_model.phot"
np.savetxt(filepath,
            np.column_stack((pflux,pflux_err)),
            header=f'model redshift = {model_components["redshift"]}\n' + "\n".join(myfilters))
print("Saved To :",filepath)



