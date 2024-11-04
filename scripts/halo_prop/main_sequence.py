import numpy, galspy
import matplotlib.pyplot as plt

from galspy.MPGadget import _Sim


# --- SIMULATIONS
L150N2040   = galspy.NavigationRoot("/mnt/home/student/cranit/NINJA/simulations/L150N2040/SNAPS")
L250N2040   = galspy.NavigationRoot("/mnt/home/student/cranit/NINJA/simulations/L250N2040/SNAPS")


# --- MAIN SEQUENCE PLOT
fig, ax = plt.subplots(figsize=(10,8))
iax = ax.inset_axes([0.7,0.1,0.31,0.3])

star_mass_min = 0
star_mass_max = 0

def PlotMS(BOX:_Sim,red,mask_lim,**kwargs):

    # --- AUTO-FLAGS
    SNAP        = BOX.PIG(BOX.SnapNumFromZ(red))
    MASS_UNIT   = 10**10
    HUBBLE      = 0.6736

    # --- GET FIELDS
    MHALO       = SNAP.FOFGroups.Mass() * MASS_UNIT / HUBBLE
    MSTAR       = (SNAP.FOFGroups.MassByType().T)[4] * MASS_UNIT / HUBBLE
    SFR         = SNAP.FOFGroups.StarFormationRate()

    # --- MASK AND PLOT

    mask1 = (MHALO>mask_lim)
    mask2 = (MSTAR>0)
    mask = mask1 & mask2
    MSTAR = MSTAR[mask]
    SFR = SFR[mask]

    ax.plot(MSTAR,SFR,'.',ms=2,**kwargs)
    iax.plot(numpy.log10(MSTAR),numpy.log10(SFR/MSTAR),'.',ms=1,**kwargs)

    # Update star mass for observation fitting
    box_star_mass_min = min(MSTAR)
    box_star_mass_max = max(MSTAR)

    global star_mass_min
    global star_mass_max

    if (star_mass_min==0) or (box_star_mass_min<star_mass_min):
        star_mass_min=box_star_mass_min
    
    if (star_mass_max==0) or (box_star_mass_max>star_mass_max):
        star_mass_max=box_star_mass_max
    
    



PlotMS(L150N2040,6.5,1e11,color='m',label="L150N2040")
PlotMS(L150N2040,7.5,9e10,color='m',)
PlotMS(L150N2040,8.5,8e10,color='m',)
PlotMS(L150N2040,9.5,7e10,color='m',)

PlotMS(L250N2040,6.5,1e11,color='c',label="L250N2040")
PlotMS(L250N2040,7.5,9e10,color='c')
PlotMS(L250N2040,8.5,8e10,color='c')
PlotMS(L250N2040,9.5,7e10,color='c')





# --- OBSERVATION
# Calabro et al. (arXiv:2402.17829v1) 
# Table 1 (3rd row) and Fig 4
M_comp = numpy.array([star_mass_min,star_mass_max])
def GetObs(M,m,q,merr,qerr,**kwargs):
    # x = log M*/M0
    # y = log SFR/(M0/yr)
    # y = m*x + q
    x = numpy.log10(M)
    y = m*x + q

    # --- Fit plot
    fitSFR = numpy.power(10,y)
    ax.plot(M,fitSFR,'k-',**kwargs)
    # iax.plot(numpy.log10(M),numpy.log10((10**q)*numpy.power(M,m-1)),'k-',**kwargs)
    iax.plot(numpy.log10(M),numpy.log10(fitSFR/M),'k-',**kwargs)

    # --- Error plot
    # xl = x[0] #left
    # xr = x[-1] #right
    # mp,mn=m+merr,m-merr #positive,negative
    # qp,qn=q+qerr,q-qerr

    # yl_max = max(mp*xl+qp, mp*xl+qn, mn*xl+qp, mn*xl+qn)
    # yl_min = min(mp*xl+qp, mp*xl+qn, mn*xl+qp, mn*xl+qn)
    # yr_max = max(mp*xr+qp, mp*xr+qn, mn*xr+qp, mn*xr+qn)
    # yr_min = min(mp*xr+qp, mp*xr+qn, mn*xr+qp, mn*xr+qn)

    # fitSFR_err_max = numpy.power(10,[yl_max,yr_max])
    # fitSFR_err_min = numpy.power(10,[yl_min,yr_min])

    # ax.fill_between(M,fitSFR_err_max,fitSFR_err_min,color='k',alpha=0.05,ec=None)
    # iax.fill_between(numpy.log10(M),numpy.log10(fitSFR_err_max/M),numpy.log10(fitSFR_err_min/M),color='k',alpha=0.05,ec=None)

    x_range     = numpy.linspace(x[0],x[-1],100)
    yerr_up     = 0*x_range
    yerr_down   = 0*x_range
    mp,mn=m+merr,m-merr #positive,negative
    qp,qn=q+qerr,q-qerr
    for i,xi in enumerate(x_range):
        y1 = mp*xi + qp 
        y2 = mp*xi + qn
        y3 = mn*xi + qp
        y4 = mn*xi + qn
        maxy = max([y1,y2,y3,y4])
        miny = min([y1,y2,y3,y4])
        yerr_up[i] = maxy
        yerr_down[i] = miny



    ax.fill_between(10**x_range,10**yerr_down,10**yerr_up,color='k',alpha=0.05,ec=None)
    # iax.fill_between(numpy.log10(x_range),yerr_down,yerr_up,color='k',alpha=0.05,ec=None)

# GetObs(M_comp,0.55,-4.0,0.12,1,lw=1,label="Calabro et al. (2024)")
GetObs(M_comp,0.76,-6.0,0.07,0.6,lw=1,label="Calabro et al. (2024)")





# --- BEUTIFY
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlabel("Stellar Mass $(M_{*}/M_{\odot})$",fontsize=20)
ax.set_ylabel("Star Formation Rate $(M_{\odot} $yr$^{-1})$",fontsize=20)
ax.tick_params(axis='both', which='major', labelsize=16)
ax.tick_params(axis='both', which='minor', labelsize=12)

# iax.set_xscale('log')
# iax.set_yscale('log')
iax.set_xlabel("$\log(M_{*}/M_{\odot})$",fontsize=12,labelpad=0)
iax.set_ylabel("$\log$ sSFR $($yr$^{-1})$",fontsize=12,rotation=-90,labelpad=16)
iax.tick_params(axis='both', labelsize=6)
iax.yaxis.set_label_position("right")
iax.yaxis.tick_right()
iax.tick_params(axis='both', which='major', labelsize=8)
iax.tick_params(axis='both', which='minor', labelsize=8)

plt.legend(loc="upper left",fontsize=14,frameon=False,markerscale=4)
# plt.annotate(f"L150N2040",xy=(0.5,1),xytext=(0,-10),xycoords="axes fraction",textcoords="offset pixels",ha="center",va='top',fontsize=20)
# plt.title(f"MAIN SEQUENCE (z={numpy.round(REDSHIFT,2)})")


# --- SAVE
plt.show()
# plt.savefig(SAVE_PATH,dpi=300)
# plt.savefig("temp/plots/main_seq.png",dpi=300)