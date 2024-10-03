import galspec.bpass as bp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.gridspec import GridSpec

fig = plt.figure(figsize=(12, 6))
gs = GridSpec(3, 3, figure=fig, width_ratios=[10,10,1],wspace=0.4)

ax1 = fig.add_subplot(gs[0,1])
ax2 = fig.add_subplot(gs[1,1])
ax3 = fig.add_subplot(gs[2,1])
ax4 = fig.add_subplot(gs[:,0])
ax_cbar = fig.add_subplot(gs[:,2]) 

def SaveTableFor(Z):
    BPASS = bp.BPASS("CHABRIER_UPTO_300M","Binary",Z)
    BAND1=BPASS.Spectra.GetFlux(1400,1500).to_numpy()
    BAND2=BPASS.Spectra.GetFlux(2450,2550).to_numpy()
    BAND3=BPASS.Spectra.GetFlux(4400,4500).to_numpy()

    lam1,flx1 = BAND1[:,0],BAND1[:,1:].T
    lam2,flx2 = BAND2[:,0],BAND2[:,1:].T
    lam3,flx3 = BAND3[:,0],BAND3[:,1:].T

    # ----- See all age flux
    ages = np.arange(6,11.1,0.1).round(1)

    cmap = plt.get_cmap('viridis', len(ages))
    norm = colors.Normalize(vmin=6, vmax=11)
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)

    for i in range(len(ages)):
        ax1.plot(lam1,flx1[i,:],color=cmap(i))
        ax2.plot(lam2,flx2[i,:],color=cmap(i))
        ax3.plot(lam3,flx3[i,:],color=cmap(i))

    cbar = fig.colorbar(sm, cax=ax_cbar, ticks=[6, 11],)
    cbar.ax.set_yticklabels(['1 Million', '100 Billion'])
    cbar.set_label('$Log_{10}Age$')

    for ax in [ax1,ax2,ax3]:
        ax.set_yscale("log")
        ax.set_xlabel("Wavelength ($\AA$)")
        ax.set_ylabel("Flux")
        
    ax1.axvline(0.5*(lam1[0]+lam1[-1]),ls='--',color='k')
    ax1.set_xlim(lam1[0],lam1[-1])

    ax2.axvline(0.5*(lam2[0]+lam2[-1]),ls='--',color='k')
    ax2.set_xlim(lam2[0],lam2[-1])

    ax3.axvline(0.5*(lam3[0]+lam3[-1]),ls='--',color='k')
    ax3.set_xlim(lam3[0],lam3[-1])

    # ----- Mean Flux
    avg_flx1 = np.log10(np.mean(flx1,axis=1))
    avg_flx2 = np.log10(np.mean(flx2,axis=1))
    avg_flx3 = np.log10(np.mean(flx3,axis=1))
    
    # if False:
    #     for i in range(len(ages)-1):
    #         age_seg     = (ages[i],ages[i+1])
    #         flux_seg    = (avg_flux[i],avg_flux[i+1])
    #         ax1.plot(age_seg,flux_seg,color=cmap(i))

    ax4.plot(ages,avg_flx1,label=f"{int(lam1[0])}$\AA$ - {int(lam1[-1])}$\AA$")
    ax4.plot(ages,avg_flx2,label=f"{int(lam2[0])}$\AA$ - {int(lam2[-1])}$\AA$")
    ax4.plot(ages,avg_flx3,label=f"{int(lam3[0])}$\AA$ - {int(lam3[-1])}$\AA$")

    ax4.legend(title=f"Z={Z}")
    ax4.set_xlabel("$Log_{10}(Age)$")
    ax4.set_ylabel("$Log_{10}(\\overline{Flux})$")

    if True:
        np.savetxt("temp/age_flux_Z002.txt",np.column_stack((ages,avg_flx1,avg_flx2,avg_flx3)),"%04f",header="Z=0.002\nAge F(1400,1500) F(2450,2550) F(4400,4500)")

# SaveTableFor(0.002)

plt.show()
# plt.savefig("temp/fit.png")


