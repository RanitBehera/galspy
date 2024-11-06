import numpy, galspy
import matplotlib.pyplot as plt

from galspy.MPGadget import _Sim

from galspy.utility.Figure.MainSequence import MainSequenceFigure
from galspy.utility.Figure.Beautification import SetMyStyle
SetMyStyle()



# --- SIMULATIONS
L150N2040   = galspy.NavigationRoot("/mnt/home/student/cranit/NINJA/simulations/L150N2040/SNAPS")
L250N2040   = galspy.NavigationRoot("/mnt/home/student/cranit/NINJA/simulations/L250N2040/SNAPS")


msfig = MainSequenceFigure(1,4)
msfig.Plot([L250N2040,L150N2040],[10,9,8,7])

msfig.Beautify()

plt.show()








# --- MAIN SEQUENCE PLOT
# fig, ax = plt.subplots(figsize=(10,8))
# # iax = ax.inset_axes([0.7,0.1,0.31,0.3])

# star_mass_min = 0
# star_mass_max = 0

# def PlotMS(BOX:_Sim,red,mask_lim,**kwargs):

#     # --- AUTO-FLAGS
#     SNAP        = BOX.PIG(BOX.SnapNumFromZ(red))
#     MASS_UNIT   = 10**10
#     HUBBLE      = 0.6736

#     # --- GET FIELDS
#     MHALO       = SNAP.FOFGroups.Mass() * MASS_UNIT / HUBBLE
#     MSTAR       = (SNAP.FOFGroups.MassByType().T)[4] * MASS_UNIT / HUBBLE
#     SFR         = SNAP.FOFGroups.StarFormationRate()

#     # --- MASK AND PLOT

#     mask1 = (MHALO>mask_lim)
#     mask2 = (MSTAR>0)
#     mask = mask1 & mask2
#     MSTAR = MSTAR[mask]
#     SFR = SFR[mask]

#     ax.plot(MSTAR,SFR,'.',ms=2,**kwargs)
#     # iax.plot(numpy.log10(MSTAR),numpy.log10(SFR/MSTAR),'.',ms=1,**kwargs)

#     # Update star mass for observation fitting
#     box_star_mass_min = min(MSTAR)
#     box_star_mass_max = max(MSTAR)

#     global star_mass_min
#     global star_mass_max

#     if (star_mass_min==0) or (box_star_mass_min<star_mass_min):
#         star_mass_min=box_star_mass_min
    
#     if (star_mass_max==0) or (box_star_mass_max>star_mass_max):
#         star_mass_max=box_star_mass_max
    

# PlotMS(L150N2040,7,1e11,color='m',label="L150N2040")
# # PlotMS(L150N2040,7.5,9e10,color='m',)
# # PlotMS(L150N2040,8.5,8e10,color='m',)
# # PlotMS(L150N2040,9.5,7e10,color='m',)

# PlotMS(L250N2040,7,1e11,color='c',label="L250N2040")
# # PlotMS(L250N2040,7.5,9e10,color='c')
# # PlotMS(L250N2040,8.5,8e10,color='c')
# # PlotMS(L250N2040,9.5,7e10,color='c')


# # --- OBSERVATION
# # ------------------------------------------------------
# # Calabro et al. (arXiv:2402.17829v1) 
# # Table 1 (3rd row) and Fig 4
# M_comp = numpy.array([star_mass_min,star_mass_max])
# def PlotCalabro(M,m,q,merr,qerr,**kwargs):
#     # Calabro
#     # x = log M*/M0
#     # y = log SFR/(M0/yr)
#     # y = m*x + q
#     x = numpy.log10(M)
#     y = m*x + q

#     # --- Fit plot
#     fitSFR = numpy.power(10,y)
#     ax.plot(M,fitSFR,'k-',**kwargs)
#     # iax.plot(numpy.log10(M),numpy.log10((10**q)*numpy.power(M,m-1)),'k-',**kwargs)
#     # iax.plot(numpy.log10(M),numpy.log10(fitSFR/M),'k-',**kwargs)

# # PlotCalabro(M_comp,0.55,-4.0,0.12,1,lw=1,label="Calabro et al. (2024)")
# PlotCalabro(M_comp,0.76,-6.0,0.07,0.6,lw=1,label="Calabro et al. (2024)")

# # ------------------------------------------------------
# # Schreiber et al. (https://arxiv.org/abs/1409.5433)
# # Equation 9
# def PlotSchreiber(M,z):
#     # Schreiber
#     m = numpy.log10(M/1e9) 
#     m0=0.5
#     a0=1.5
#     a1=0.3
#     m1=0.36
#     a2=2.5
#     r=numpy.log10(1+z)

#     def GetSFR(m):
#         return 10**(m - m0 + a0*r - a1*(numpy.max([0,m-m1-a2*r]))**2)

#     sfr_ms = numpy.array([GetSFR(mi) for mi in m])
#     plt.plot(M,sfr_ms,'-',c='r')


# # PlotSchreiber(M_comp,6)
# PlotSchreiber(M_comp,7)
# # PlotSchreiber(M_comp,8)
# # PlotSchreiber(M_comp,9)
# # ------------------------------------------------------


# # Speagle et.al (https://arxiv.org/pdf/1405.2041)
# # Abstract
# from astropy.cosmology import FlatLambdaCDM
# cosmo = FlatLambdaCDM(H0=67.36, Om0=0.3153)
# # atropy lookbacktime in in Gyrs
# lbt_inf = cosmo.lookback_time(999999)
# lbt_7 = cosmo.lookback_time(7)
# age = (lbt_inf -lbt_7).value

# def PlotSpeagle(M,age):
#     # t in Gyr
#     def GetSFR():
#         slope = 0.84 - 0.026*age
#         offset = 6.51 - 0.11*age
#         log_SFR = slope * numpy.log10(M) - offset
#         return 10**log_SFR
    
#     sfr_ms = GetSFR()
#     plt.plot(M,sfr_ms,'-',c='b')


# PlotSpeagle(M_comp,age)



















# # --- BEAUTIFY
# ax.set_xscale('log')
# ax.set_yscale('log')
# ax.set_xlabel("Stellar Mass $(M_{*}/M_{\odot})$",fontsize=20)
# ax.set_ylabel("Star Formation Rate $(M_{\odot} $yr$^{-1})$",fontsize=20)
# ax.tick_params(axis='both', which='major', labelsize=16)
# ax.tick_params(axis='both', which='minor', labelsize=12)

# # iax.set_xscale('log')
# # iax.set_yscale('log')
# # iax.set_xlabel("$\log(M_{*}/M_{\odot})$",fontsize=12,labelpad=0)
# # iax.set_ylabel("$\log$ sSFR $($yr$^{-1})$",fontsize=12,rotation=-90,labelpad=16)
# # iax.tick_params(axis='both', labelsize=6)
# # iax.yaxis.set_label_position("right")
# # iax.yaxis.tick_right()
# # iax.tick_params(axis='both', which='major', labelsize=8)
# # iax.tick_params(axis='both', which='minor', labelsize=8)

# # plt.legend(loc="upper left",fontsize=14,frameon=False,markerscale=4)
# # # plt.annotate(f"L150N2040",xy=(0.5,1),xytext=(0,-10),xycoords="axes fraction",textcoords="offset pixels",ha="center",va='top',fontsize=20)
# # # plt.title(f"MAIN SEQUENCE (z={numpy.round(REDSHIFT,2)})")


# # --- SAVE
# plt.show()