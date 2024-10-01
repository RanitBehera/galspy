import galspec.bpass as bp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from scipy.optimize import curve_fit


BPASS = bp.BPASS("CHABRIER_UPTO_300M","Binary",0.02)
FLUX=BPASS.Spectra.GetFlux(1400,1500).to_numpy()

lams = FLUX[:,0]
flux = FLUX[:,1:].T

# print(FLUX.shape)

# ----- See all age flux
ages = np.arange(6,11.1,0.1).round(1)

cmap = plt.get_cmap('viridis', len(ages))
fig, axs = plt.subplots(1,2,figsize=(12, 6))
ax1,ax2 = axs
norm = colors.Normalize(vmin=6, vmax=11)
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
for i in range(len(ages)):
    ax2.plot(lams,flux[i,:],color=cmap(i))

cbar = fig.colorbar(sm, ax=ax2, ticks=[6, 11],)
cbar.ax.set_yticklabels(['1 Million', '100 Billion'])
cbar.set_label('$Log_{10}Age$')

ax2.set_yscale("log")
ax2.set_xlabel("Wavelength ($\AA$)")
ax2.set_ylabel("Flux")
ax2.axvline(1450,ls='--',color='k')
ax2.set_xlim(1400,1500)

# Mean and Fit
avg_flux = np.log10(np.mean(flux,axis=1))
# ax1.plot(ages,avg_flux)
for i in range(len(ages)-1):
    age_seg     = (ages[i],ages[i+1])
    flux_seg    = (avg_flux[i],avg_flux[i+1])
    ax1.plot(age_seg,flux_seg,color=cmap(i))


# Fit
ORDER = 6
def FitFun(t,a0,a1,a2,a3,a4,a5,a6):
    a=[a0,a1,a2,a3,a4,a5,a6]
    return np.sum([a[i]*t**i for i in range(ORDER+1)])

popt,pcov = curve_fit(FitFun,ages,avg_flux,p0=(1,-1,-1,-1,-1,-1,-1))

t_hr=np.linspace(6,11,100)
f_hr=[FitFun(t,*popt) for t in t_hr]
ax1.plot(t_hr,f_hr)


plt.show()


