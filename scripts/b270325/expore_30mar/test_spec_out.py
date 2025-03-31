import numpy as np
import matplotlib.pyplot as plt


DDIR = "/mnt/home/student/cranit/RANIT/Repo/galspy/temp/share_anand/img_and_spec/"


def PlotFile(file):
    filepath = DDIR + file

    wl,spec=np.loadtxt(filepath).T
    plt.plot(wl,spec,label=file)


PlotFile("L150N2040_WIND_WEAK_z7p0_stnb_gid2.txt")
PlotFile("L150N2040_WIND_WEAK_z7p0_st_gid2.txt")
PlotFile("L150N2040_z7p0_stnb_gid2.txt")
PlotFile("L150N2040_z7p0_st_gid2.txt")


plt.xscale("log")
plt.yscale("log")
plt.legend()
plt.show()