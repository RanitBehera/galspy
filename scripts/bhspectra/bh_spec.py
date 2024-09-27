import numpy as np
import matplotlib.pyplot as plt
from galspec.AGN import ThinDisk

TD1 = ThinDisk(1e8,1,3,30000,0)

freq=np.logspace(-2,20,1000)
L1 = TD1.SpectralLuminosity(freq)
SE = TD1.GetSoftExcess(freq,0.9)

plt.plot(freq,L1*(1e7/1e24),'g--',label='Thin Disk',lw=1)
plt.plot(freq,SE*(1e7/1e24),'r--',label='Soft Excess',lw=1)
plt.plot(freq,(L1+SE)*(1e7/1e24),'k-',label="Total",lw=2)


plt.xscale("log")
plt.yscale("log")
plt.ylim(1,1e7)
plt.xlim(1e9,1e20)
plt.show()

