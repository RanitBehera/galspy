import numpy as np
import matplotlib.pyplot as plt
from galspec.AGN import ThinDisk

TD1 = ThinDisk(1e8,1,3,30000,0)
# TD1 = ThinDisk(1e5,1e-6,3,30000,0)

freq=np.logspace(-2,20,1000)
L1 = TD1.SpectralLuminosity(freq)
SE = TD1.GetSoftExcess(freq,0.9)


# PLOT
fig,axs = plt.subplots(1,2)
ax1,ax2 =axs

ax1.plot(freq,L1*(1e7/1e24),'g--',label='Thin Disk',lw=1)
ax1.plot(freq,SE*(1e7/1e24),'r--',label='Soft Excess',lw=1)
ax1.plot(freq,(L1+SE)*(1e7/1e24),'k-',label="Total",lw=2)



# OBSERVED
z=4.66
from astropy.cosmology import FlatLambdaCDM
cosmo = FlatLambdaCDM(H0=67.36, Om0=0.3153)
DL=cosmo.luminosity_distance(z).value # In MPC
m_per_Mpc = 3.086e22
DL *= m_per_Mpc
Area = 4*np.pi*(DL**2)



L_nu = L1+SE
c=3e8
lam = c/freq
L_lam = ((freq**2)*L_nu)#/(c*(1+z))

lam=(lam/1e-10)#*(1+4.66)

L_lam_obs = L_lam/Area

# ax2.plot(lam,L_lam_obs/1e-26)
ax2.plot(lam,L_lam_obs*1e7)


ax1.set_xscale("log")
ax1.set_yscale("log")
ax1.set_ylim(1,1e7)
ax1.set_xlim(1e9,1e20)

ax2.axvspan(1000,3000,alpha=0.5)
ax2.set_xscale("log")
ax2.set_yscale("log")
# ax1.set_ylim(1,1e7)
# ax1.set_xlim(1e9,1e20)






plt.show()

