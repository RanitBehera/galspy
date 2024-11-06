import numpy
from galspy.MPGadget import _PIG,_Sim
from galspy.utility.Figure.Beautification import SetMyStyle

import matplotlib
import matplotlib.axes
import matplotlib.axis
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
from matplotlib.lines import Line2D

from astropy.cosmology import FlatLambdaCDM

# ===========================================
# =========== OBSERVATIONAL FITS ============
# ===========================================
# Calabro et al. (2024)
# https://arxiv.org/abs/2402.17829v1
# Table 1 (3rd row) and Figure 4
def Calabro2024_Fit(M):
    m=0.76
    q=-6.0
    log_M = numpy.log10(M)
    x=log_M
    y = m*x + q
    log_SFR = y
    SFR = 10**log_SFR
    return M,SFR

# -------------------------------------------
# Schreiber et al. (2014)
# https://arxiv.org/abs/1409.5433
# Equation 9
def Schreiber2014_Fit(M,z):
    M=numpy.array(M)
    m = numpy.log10(M/1e9) 
    m0=0.5
    a0=1.5
    a1=0.3
    m1=0.36
    a2=2.5
    r=numpy.log10(1+z)

    def Fit(m):
        return (m - m0 + a0*r - a1*(numpy.max([0,m-m1-a2*r]))**2)
    
    log_SFR = numpy.array([Fit(mi) for mi in m])
    SFR = 10**log_SFR
    return M,SFR



# -------------------------------------------
# Speagle et al. (2014)
# https://arxiv.org/abs/1405.2041
# Abstract
def Speagle2014_Fit(M,t):
    # t in Gyr
    slope = 0.84 - 0.026*t
    offset = 6.51 - 0.11*t
    log_SFR = slope * numpy.log10(M) - offset
    SFR = 10**log_SFR
    return M,SFR


# ================================================



class MainSequenceFigure:
    def __init__(self,nrow:int=2,nclm:int=3):
        fig = plt.figure(figsize=(14,4))

        gs = GridSpec(nrow,nclm)

        # TODO : Improve
        ax00=fig.add_subplot(gs[0,0])
        ax01=fig.add_subplot(gs[0,1])
        ax02=fig.add_subplot(gs[0,2])
        ax03=fig.add_subplot(gs[0,3])
        # ax11=fig.add_subplot(gs[1,1])
        # ax12=fig.add_subplot(gs[1,2])

        self.axes = [ax00,ax01,ax02,ax03]

        # COSMOLOGY
        self.MASS_UNIT   = 10**10
        self.HUBBLE      = 0.6736

        self._mstar_min = 0
        self._mstar_max = 0


    def _MainSeq(self,ax:plt.Axes,BOX:_Sim,red,mask_lim,**kwargs):
        # --- AUTO-FLAGS
        SNAP        = BOX.PIG(BOX.SnapNumFromZ(red))

        # --- GET FIELDS
        MHALO       = SNAP.FOFGroups.Mass() * self.MASS_UNIT / self.HUBBLE
        MSTAR       = (SNAP.FOFGroups.MassByType().T)[4] * self.MASS_UNIT / self.HUBBLE
        SFR         = SNAP.FOFGroups.StarFormationRate()

        # --- MASK AND PLOT
        mask1 = (MHALO>mask_lim)
        mask2 = (MSTAR>0)
        mask = mask1 & mask2
        MSTAR = MSTAR[mask]
        SFR = SFR[mask]

        ax.plot(MSTAR,SFR,'.',ms=2,**kwargs)
        # iax.plot(numpy.log10(MSTAR),numpy.log10(SFR/MSTAR),'.',ms=1,**kwargs)

        # Update star mass for observation fitting
        _mstar_min = numpy.min(MSTAR)
        _mstar_max = numpy.max(MSTAR)

        if (self._mstar_min==0) or (_mstar_min<self._mstar_min):
            self._mstar_min=_mstar_min
    
        if (self._mstar_max==0) or (_mstar_max>self._mstar_max):
            self._mstar_max=_mstar_min


    def Plot(self,sims:list[_Sim],redshifts:list[float]):
        self.reds=redshifts
        z_to_mask = {7:1e11,8:9e10,9:8e10,10:7e10}
        clrs=['c','m']        
        for i,sim in enumerate(sims):
            for ax,red in zip(self.axes,redshifts):
                self._MainSeq(ax,sim,red,z_to_mask[int(red)],c=clrs[i])

    # TODO: FIX thse, get redshift automatically for each axis
    def AddCalabro2024(self,M,ax:plt.Axes,**kwargs):
        M,SFR = Calabro2024_Fit(M)
        ax.plot(M,SFR,**kwargs)

    def AddSchreiber2014(self,M,z,ax:plt.Axes,**kwargs):
        M,SFR = Schreiber2014_Fit(M,z)
        ax.plot(M,SFR,**kwargs)

    def AddSpeagle2014(self,M,z,ax:plt.Axes,**kwargs):
        cosmo = FlatLambdaCDM(H0=67.36, Om0=0.3153)
        # atropy lookbacktime in in Gyrs
        lbt_inf = cosmo.lookback_time(999999)
        lbt_z = cosmo.lookback_time(z)
        age = (lbt_inf -lbt_z).value

        M,SFR = Speagle2014_Fit(M,age)
        ax.plot(M,SFR,**kwargs)

    def Beautify(self):
        SetMyStyle(16)

        axs = self.axes        
        for i,ax in enumerate(axs):
            ax.tick_params(axis='both', direction='in',which="both")
            ax.grid(False)
            ax.set_xscale('log')
            ax.set_yscale('log')
            ax.set_xlim(1e6,2e11)
            ax.set_xticks(10**(numpy.array([7,8,9,10,11])))
            ax.set_ylim(1e-3,1e4)
            ax.set_yticks(numpy.power(10.0,[-2,-1,0,1,2,3]))
            ax.annotate(f"z={numpy.round(self.reds[i],2)}",(0,1),(8,-8),
                        "axes fraction","offset pixels",ha="left",va="top")
            ax.grid(alpha=0.2)


        for ax in [axs[1],axs[2],axs[3]]:
            ax.yaxis.set_ticklabels([])
            ax.set_ylabel("")

        for ax in [axs[0],axs[1],axs[2],axs[3]]:
            ax.set_xlabel("$M_*/M_\odot$",fontsize=14)
        
        for ax in [axs[0]]:
            ax.set_ylabel("SFR $(M_{\odot} $yr$^{-1})$",fontsize=14)

        clrs=['c','m']
        labels=["L250N2040","L150N2040"]
        line1 = mlines.Line2D([], [], color=clrs[0],ls='', marker='o',markersize=2, label=labels[0])
        line2 = mlines.Line2D([], [], color=clrs[1],ls='', marker='o',markersize=2, label=labels[1])
        
        boxes = [line2,line1]
        leg=axs[-1].legend(handles=boxes,fontsize=12, loc='lower right',ncol=1,frameon=False)
        axs[-1].add_artist(leg)

        plt.subplots_adjust(wspace=0.03,hspace=0.03,bottom=0.2)


        # ADD OBS
        # TODO : AUTOMATE IT
        for ax,z in zip(self.axes,self.reds):
            M = numpy.geomspace(*ax.get_xlim(),100)
            self.AddSpeagle2014(M,z,ax,color='springgreen')
            self.AddCalabro2024(M,ax,color='darkorange')
            self.AddSchreiber2014(M,z,ax,color='royalblue')


        # MANUAL LEGEND
        clrs=['springgreen','darkorange','royalblue']
        labels=["Speagle et al. (2014)","Calabro et al. (2024)","Schreiber et al. (2014)"]
        ln_Spe = mlines.Line2D([], [], color=clrs[0],ls='-', marker=' ',markersize=2, label=labels[0])
        ln_Cal = mlines.Line2D([], [], color=clrs[1],ls='-', marker=' ',markersize=2, label=labels[1])
        ln_Sch = mlines.Line2D([], [], color=clrs[2],ls='-', marker=' ',markersize=2, label=labels[2])
        
        boxes = [ln_Sch,ln_Spe,ln_Cal]
        ax.figure.legend(handles=boxes,
                          loc='upper center',
                          frameon=False,
                          bbox_to_anchor=(0.5,1),
                          ncols=5,
                          fontsize=12)
