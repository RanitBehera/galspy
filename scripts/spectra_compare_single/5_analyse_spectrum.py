import numpy as np
import os
import matplotlib.pyplot as plt



DDIR = "/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/spectra_compare_single/data"
TGID=4

def Plot(filename,label):
    filepath = DDIR + os.sep + filename
    wl,spec= np.loadtxt(filepath).T
    plt.plot(wl,spec,label=label)

Plot(f"spec_st_L150N2040_z7p00_{TGID}.txt","Intrinsic Stellar")
Plot(f"spec_dec_L150N2040_z7p00_{TGID}.txt","Reddened (Central Star)")
Plot(f"spec_dei_L150N2040_z7p00_{TGID}.txt","Reddened (Individual Star)")


plt.xscale("log")
plt.yscale("log")
plt.xlim(800,5000)
plt.ylim(1e7,1e10)
plt.legend()
plt.show()

