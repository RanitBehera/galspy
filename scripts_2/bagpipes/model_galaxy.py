import bagpipes as pipes
import numpy as np
import matplotlib.pyplot as plt
import os
from pathlib import Path

# ----------------------------------------
exp = {}                                    # Tau model star formation history component
exp["age"] = 3.                             #* Gyr
exp["tau"] = 0.75                           #* Gyr
exp["massformed"] = 9.                      # log_10(M*/M_solar)
exp["metallicity"] = 0.5                    # Z/Z_oldsolar

# ----------------------------------------
nebular = {}
nebular["logU"] = -1                        #* Log_10 of the ionization parameter.

# ----------------------------------------
dust = {}
dust["type"] = "Calzetti"                   #* Attenuation law: "Calzetti", "Cardelli", "CF00" or "Salim"
dust["Av"] = 0.2                            #* Absolute attenuation in the V band: magnitudes

# ----------------------------------------
model_components = {}
model_components["redshift"] = 1.0          #* Observed redshift
model_components["exponential"] = exp
# model_components["nebular"] = nebular
model_components["dust"] = dust

# ----------------------------------------
model = pipes.model_galaxy(model_components,spec_wavs=np.arange(1e2,1e5,5))
_sfh    = model.sfh
_spec   = model.spectrum
wave,flux = _spec.T

# Plot -----------------------------------
# plt.plot(wave,flux)
# plt.yscale("log")
# plt.xscale("log")
# plt.show()


# Export to a file -----------------------
filedir = str(Path(__file__).parent.absolute())
np.savetxt(filedir + os.sep + "data/demo_model.spec",np.column_stack((wave,flux)))

