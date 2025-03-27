import numpy as np
import matplotlib.pyplot as plt
import pickle
from galspec.Utility import SlopeFinder, ContinnumFinder


with open("cache/cloudy_chab_300M_solar.in","rb") as fp:
    tspec:dict = pickle.load(fp)
WL = tspec["0.02"]["WL"]
flux = tspec["0.02"]["8.0"]

mask1 = WL>700
mask2 = WL<30000
mask = mask1 & mask2

WL = WL[mask]
flux = flux[mask]

plt.plot(WL,flux)


x,y,b = SlopeFinder(WL,flux,1300,2600,1400,-2)
# cx,cy,dx,ay = ContinnumFinder(np.log10(WL),np.log10(flux),np.log10(1300),np.log10(2600),30)
# plt.plot(10**cx,10**cy)
# print(cx,cy)
plt.plot(x,y)




plt.yscale("log")
plt.xscale("log")
plt.axvline(2460)
plt.axvline(1300)
plt.axvline(1400)

plt.show()