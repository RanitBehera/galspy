import numpy
from galspy.utility.MassFunction import MassFunction,MassFunctionLiterature, LMF_OPTIONS
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



def GetLMF(model:LMF_OPTIONS,redshift,COSMOLOGY=None):
    if COSMOLOGY==None:COSMOLOGY = {'flat': True,'H0': 67.36,'Om0': 0.3153,'Ob0': 0.0493,'sigma8': 0.811,'ns': 0.9649}
    MASS_HR     = numpy.logspace(7,12,100)
    hubble=(COSMOLOGY["H0"]/100)
    M, dn_dlogM = MassFunctionLiterature(model,COSMOLOGY,redshift,MASS_HR,'dn/dlnM')
    
    # Ibstead of h-shufting the litreture one
    # h-shift the mass units so that not,only halo mass but all other mass is treated equally
    # and match with observations plus the litreture mass function
    # Hence turining off this, instead doing MASS * MASSUNIT / HUBBLE 
    # dn_dlogM *=hubble
    
    return M,dn_dlogM

def PlotLMF(ax:plt.Axes,model:LMF_OPTIONS,redshift,COSMOLOGY=None,**kwargs):
        ax.plot(*GetLMF(model,redshift,COSMOLOGY),**kwargs)

def PlotBMF(ax:plt.Axes,M,phi,error,min_mass,right_skip_count,**kwargs):
        # if right_skip_count>0:
            # M,dn_dlogM,error = M[:-right_skip_count],dn_dlogM[:-right_skip_count],error[:-right_skip_count]
        # mass_mask = (M>min_mass)
        # num_mask = (phi>1e-10)
        num_mask = (phi>((M**(-7/5))*(10**(-((-7/5)*6+3)))))
        mask =  num_mask
        M,phi,error = M[mask],phi[mask],error[mask]

        ax.plot(M,phi,'-',lw=2,color=kwargs["color"],marker=kwargs["marker"],label="")
        ax.fill_between(M,phi-0.9*error,phi+0.9*error,color=kwargs["color"],alpha=0.2,ec=None)

def PlotDeviation(ax:plt.Axes,M,phi,error,M_ref,phi_ref,**kwarg):
    phi_expected = numpy.interp(M,M_ref,phi_ref)
    dev_by_fac =  phi/phi_expected
    dev_by_fac_p =  (phi+0.7*error)/phi_expected
    dev_by_fac_n =  (phi-0.7*error)/phi_expected

    ax.plot(M,dev_by_fac,'-',color=kwarg["color"])
    ax.fill_between(M,dev_by_fac_p,dev_by_fac_n,alpha=0.2,color=kwarg["color"],ec=None)

# ======================================

class MassFunctionFigure:
    def __init__(self,ax=None,add_deviation:bool=False):
        # Create a Axes if not provides
        if ax is not None:self.ax = ax
        else:_,self.ax = plt.subplots(1,1,figsize=(8,6))

        self._pig_colors=[]
        self._mfun_ptype=[]
        self._redshifts=[]

        # Create Deivation Axis if needed
        self.add_dev = add_deviation
        if not self.add_dev: return

        fraction=1/4
        orig_ax = self.ax.get_position()

        self.ax.set_position([0,orig_ax.y0+(fraction*orig_ax.height),
                                1,(1-fraction)*orig_ax.height])
        self.ax_dev:plt.Axes = self.ax.figure.add_axes([0, orig_ax.y0,
                                                        1, fraction*orig_ax.height])
        self.ax.set_xlabel([])

        def update_xaxis(event):
            self.ax_dev.set_xlim(self.ax.get_xlim())
            self.ax_dev.set_xscale(self.ax.get_xscale())  # Sync the x-scale (linear/log)
            self.ax.figure.canvas.draw_idle()  # Refresh the figure

        self.ax.callbacks.connect('xlim_changed', update_xaxis)

    def _add_mfun_ptype(self,token:str):
        if token not in self._mfun_ptype:
                self._mfun_ptype.append(token)

    def AddPIG_MF(self,snap:_PIG,dm=False,gas=False,star=False,bh=False,**kwargs):
        SNAP        = snap
        MASS_UNIT   = 1e10
        BOX_SIZE    = SNAP.Header.BoxSize()/1000
        REDSHIFT    = SNAP.Header.Redshift()
        BIN_SIZE    = 0.5
        HALO_DEF    = 32
        MASS_TABLE  = SNAP.Header.MassTable()
        HUBBLE      = 0.6736

        MBT_FOF        = snap.FOFGroups.MassByType()
        M_GAS,M_DM,M_U1,M_U2,M_STAR,M_BH = numpy.transpose(MBT_FOF) * MASS_UNIT / HUBBLE
        M_TOTAL = M_GAS+M_DM+M_STAR+M_BH
        
        if not any([dm,gas,star,bh]):
             raise ValueError("At least one particle type is needed")
        
        self._redshifts.append(REDSHIFT)

        if dm:
            M, dn_dlogM,error = MassFunction(M_DM,BOX_SIZE,BIN_SIZE)
            mask=(M>32*MASS_TABLE[1]*MASS_UNIT)
            M,dn_dlogM,error = M[mask],dn_dlogM[mask],error[mask]
            PlotBMF(self.ax,M,dn_dlogM,error,HALO_DEF * MASS_TABLE[1] * MASS_UNIT,0,color=kwargs["color"],marker=" ")
            PlotDeviation(self.ax_dev,M,dn_dlogM,error,*GetLMF("Seith-Tormen",REDSHIFT),color=kwargs["color"])
            self._add_mfun_ptype("dm")

        if gas:
            M, dn_dlogM,error = MassFunction(M_GAS,BOX_SIZE,BIN_SIZE)
            mask=(M>32*MASS_TABLE[0]*MASS_UNIT)
            M,dn_dlogM,error = M[mask],dn_dlogM[mask],error[mask]
            PlotBMF(self.ax,M,dn_dlogM,error,HALO_DEF * MASS_TABLE[0] * MASS_UNIT,0,color=kwargs["color"],marker="x")
            self._add_mfun_ptype("gas")

        if star:
            M, dn_dlogM,error = MassFunction(M_STAR,BOX_SIZE,BIN_SIZE)
            PlotBMF(self.ax,M,dn_dlogM,error,HALO_DEF * MASS_TABLE[1] * MASS_UNIT,0,color=kwargs["color"],marker=kwargs.get("star_marker") or "*")
            self._add_mfun_ptype("star")

        if bh:
            M_BH = SNAP.FOFGroups.BlackholeMass()*MASS_UNIT
            M, dn_dlogM,error = MassFunction(M_BH,BOX_SIZE,BIN_SIZE)
            PlotBMF(self.ax,M,dn_dlogM,error,HALO_DEF * MASS_TABLE[1] * MASS_UNIT,0,color=kwargs["color"],marker="o")
            self._add_mfun_ptype("bh")

        self._pig_colors += kwargs["color"]


    def BeautifyPlot(self):
        SetMyStyle(16)

        self.ax.set_xscale('log')
        self.ax.set_yscale('log')
        self.ax.grid(alpha=0.3)
        self.ax.tick_params(axis='both', which='major', labelsize=16)
        self.ax.tick_params(axis='both', which='minor', labelsize=12)
        self.ax.set_xlim(left=1e5,right=1e10)
        self.ax.set_ylabel("$dn/d\log(M/M_{\odot})$",fontsize=16)
        if self.add_dev: 
            self.ax_dev.set_xlabel("$M/M_{\odot}$",fontsize=16)
        else:
            self.ax.set_xlabel("$M/M_{\odot}$",fontsize=16)
        # self.ax.legend()

        if self.add_dev:
            # self.ax_dev.yaxis.set_label_position("right")
            self.ax_dev.yaxis.tick_right()
            self.ax_dev.set_ylabel("FoF - ST\nDeviation\nby Factor",fontsize=10)
            self.ax_dev.set_xscale('log')
            self.ax_dev.axhline(1,ls='--',c='k',lw=1)
            self.ax_dev.grid(alpha=0.3)
            # self.ax_dev.set_yscale('log')
            self.ax_dev.set_ylim(0.6,1.5)
            # Direct yscale('log') has issue of hiding default labels and ticks 
            # which is partly from ylim values also. 
            # So as work around we make lin-log conversion
            ticks= [0.8,1,1.25]
            self.ax_dev.set_yticks(ticks,minor=False)
            self.ax_dev.set_yticklabels(["$\\times$ " + str(t) for t in ticks])
            self.ax_dev.tick_params(axis='both', which='major', labelsize=16)
            self.ax_dev.tick_params(axis='both', which='minor', labelsize=12)

        # self.ax[0].set_title("Halo Mass Function",fontsize=16)

        # MANUAL LEGEND    
        # self.ax[0].annotate(f"$z={numpy.round(_REDSHIFT,2)}$",xy=(0,0),xytext=(10,-10),xycoords="axes fraction",textcoords="offset pixels",ha="left",va='top',fontsize=20)
        
        dm_line = mlines.Line2D([], [], color='k', marker='',markersize=8, label='Dark Matter')
        gas_line = mlines.Line2D([], [], color='k', marker='x',markersize=8, label='Gas')
        star_line = mlines.Line2D([], [], color='k', marker='*',markersize=8, label='Stellar')
        bh_line = mlines.Line2D([], [], color='k', marker='o',markersize=8, label='BH')
    
        box_L150N2040 = mpatches.Patch(color='m',label="L150N2040")
        box_L250N2040 = mpatches.Patch(color='c',label="L250N2040")
        ST_line = mlines.Line2D([], [], color='k', ls='--',label="Seith-Tormen")
        

        hands = []
        if "dm" in self._mfun_ptype: hands.append(dm_line)
        if "gas" in self._mfun_ptype: hands.append(gas_line)
        if "star" in self._mfun_ptype: hands.append(star_line)
        if "bh" in self._mfun_ptype: hands.append(bh_line)

        boxes =[]
        boxes.append(box_L150N2040)
        boxes.append(box_L250N2040)
        # boxes.append(ST_line)

        leg_part=self.ax.legend(handles=hands,fontsize=12, loc='upper left',ncol=1,frameon=False)
        leg_box=self.ax.legend(handles=boxes,fontsize=12, loc='upper right',ncol=1,frameon=True,
                               title="z="+",".join([f"{zi:.02f}" for zi in numpy.unique(numpy.round(self._redshifts,2))]),
                               title_fontsize=14)

        self.ax.add_artist(leg_part)
        self.ax.add_artist(leg_box)

        # plt.subplots_adjust(left=0.15,right=0.85,top=0.9,bottom=0.15,hspace=0)
        if self.add_dev:
            return self.ax,self.ax_dev
        else:
             return self.ax
        


class StellarMassFunctionEvolutionFigure:
    def __init__(self,sims:list[_Sim],redshifts:list[float],nrow:int=2,nclm:int=3):    
        self.sims = sims
        self.reds = redshifts
        
        fig = plt.figure(figsize=(14,4))
        num_axis = len(redshifts)
        if num_axis>nrow*nclm:
                raise ValueError("More axis are needed as length of redshifts array is larger then nrow x nclms.")

        gs = GridSpec(nrow,nclm)

        # TODO : Improve
        ax00=fig.add_subplot(gs[0,0])
        ax01=fig.add_subplot(gs[0,1])
        ax02=fig.add_subplot(gs[0,2])
        ax03=fig.add_subplot(gs[0,3])
        # ax11=fig.add_subplot(gs[1,1])
        # ax12=fig.add_subplot(gs[1,2])

        self.axes = [ax00,ax01,ax02,ax03]


    
    def Plot(self):
        # TODO : GET FROM BOX
        # TODO : SHIFT sim and redshift as function arguments to here
        clrs=['m','c']
        for ax,red in zip(self.axes,self.reds):
            mffig = MassFunctionFigure(ax)
            for i,sim in enumerate(self.sims): 
                sn  = sim.SnapNumFromZ(red)
                PIG = sim.PIG(sn)
                mffig.AddPIG_MF(PIG,star=True,color=clrs[i],star_marker=' ')

    def Beautify(self,labels=list[str]):
        SetMyStyle(16)
        self.AddObs()

        axs = self.axes
        for i,ax in enumerate(axs):
            ax.tick_params(axis='both', direction='in',which="both")
            ax.set_xscale('log')
            ax.set_yscale('log')
            ax.set_xlim(1e5,1e11)
            ax.set_xticks(10**(numpy.array([6,7,8,9,10])))
            ax.set_ylim(1e-8,1e0)
            ax.set_yticks(numpy.power(10.0,[-7,-6,-5,-4,-3,-2,-1]))
            ax.annotate(f"z={numpy.round(self.reds[i],2)}",(1,1),(-8,-8),
                        "axes fraction","offset pixels",ha="right",va="top")
            ax.grid(alpha=0.2)

        for ax in [axs[1],axs[2],axs[3]]:
            ax.yaxis.set_ticklabels([])
            ax.set_ylabel("")
        
        # for ax in [axs[0],axs[1],axs[2]]:
        #     ax.xaxis.set_ticklabels([])
        #     ax.set_xlabel("")
        
        for ax in [axs[0],axs[1],axs[2],axs[3]]:
            ax.set_xlabel("$M_*/M_\odot$",fontsize=14)
        
        for ax in [axs[0]]:
            ax.set_ylabel("$\phi(M_*)$/dex$^{-1}$ Mpc$^{-3}$",fontsize=14)


        # MANUAL LEGEND
        clrs=['m','c']
        labels=["L150N2040","L250N2040"]
        line1 = mlines.Line2D([], [], color=clrs[0], marker=' ',markersize=8, label=labels[0])
        line2 = mlines.Line2D([], [], color=clrs[1], marker=' ',markersize=8, label=labels[1])
        
        boxes = [line1,line2]
        leg=axs[0].legend(handles=boxes,fontsize=12, loc='lower left',ncol=1,frameon=False)
        axs[0].add_artist(leg)

        plt.subplots_adjust(wspace=0.03,hspace=0.03,bottom=0.2)
        


    def AddObs(self):
        # TODO : AUTOMATE
        axs = self.axes
        # z12 = axs[0]
        # z11 = axs[1]
        z10 = axs[0]
        z9 = axs[1]
        z8 = axs[2]
        z7 = axs[3]

        # https://arxiv.org/pdf/1507.05636
        CLR = (0.7,0,0)
        M=10**numpy.arange(7.25,11.30,0.5)
        
        p7=10**numpy.array([-1.63,-2.07,-2.49,-2.96,-3.47,-4.11,-4.61,-5.24])
        p7p=p7*(10**numpy.array([0.54,0.45,0.38,0.32,0.32,0.41,0.72,0.90])-1)
        p7n=p7*(1-1/10**numpy.array([0.54,0.41,0.32,0.30,0.35,0.57,0.82,0.57]))
        song2016=z7.errorbar(M[:len(p7)],p7,[p7n,p7p],fmt='o',capsize=4,color=CLR,ms=5)
        
        
        p8=10**numpy.array([-1.73,-2.28,-2.88,-3.45,-4.21,-5.31])
        p8p=p8*(10**numpy.array([1.01,0.84,0.75,0.57,0.63,1.01])-1)
        p8n=p8*(1-1/10**numpy.array([0.84,0.64,0.57,0.60,0.78,1.64]))
        z8.errorbar(M[:len(p8)],p8,[p8n,p8p],fmt='o',capsize=4,color=CLR,ms=4)

        # https://arxiv.org/pdf/2111.01160
        CLR = (0,0.6,0.25)

        M=10**numpy.array([7.75,8.25,8.70,9.10,9.50,9.90,10.30])
        Merrp=M*(10**numpy.array([0.25,0.25,0.20,0.20,0.20,0.20,0.20])-1)
        Merrn=M*(1-1/10**numpy.array([0.25,0.25,0.20,0.20,0.20,0.20,0.20]))
        p7=numpy.array([71.7,39.4,13.2,7.70,3.18,1.68,0.104])*1e-4
        p7p=numpy.array([23.7,6.9,2.7,1.67,0.88,0.63,0.240])*1e-4
        p7n=numpy.array([18.3,6.3,2.4,1.49,0.78,0.53,0.090])*1e-4
        stefanon2021=z7.errorbar(M,p7,[p7n,p7p],[Merrn,Merrp],fmt='o',capsize=4,color=CLR,ms=4)

        M=10**numpy.array([7.90,8.40,8.90,9.35,9.75,10.15])
        Merrp=M*(10**numpy.array([0.25,0.25,0.25,0.20,0.20,0.20])-1)
        Merrn=M*(1-1/10**numpy.array([0.25,0.25,0.25,0.20,0.20,0.20]))
        p8=numpy.array([41.9,8.91,3.56,1.11,0.591,0.0711])*1e-4
        p8p=numpy.array([20.6,2.49,1.19,0.57,0.371,0.1637])*1e-4
        p8n=numpy.array([14.5,2.08,0.95,0.42,0.262,0.0617])*1e-4
        z8.errorbar(M,p8,[p8n,p8p],[Merrn,Merrp],fmt='o',capsize=4,color=CLR,ms=4)
        
        M=10**numpy.array([7.50,8.25,8.75,9.50])
        Merrp=M*(10**numpy.array([0.50,0.25,0.25,0.50])-1)
        Merrn=M*(1-1/10**numpy.array([0.50,0.25,0.25,0.50]))
        p9=numpy.array([29.1,3.67,0.738,0.0764])*1e-4
        p9p=numpy.array([23.0,2.93,0.348,0.1016])*1e-4
        p9n=numpy.array([13.9,1.81,0.256,0.0517])*1e-4
        z9.errorbar(M,p9,[p9n,p9p],[Merrn,Merrp],fmt='o',capsize=4,color=CLR,ms=4)


        M=10**numpy.array([7.65,8.25,8.75])
        Merrp=M*(10**numpy.array([0.35,0.25,0.25])-1)
        Merrn=M*(1-1/10**numpy.array([0.35,0.25,0.25]))
        p10=numpy.array([12.0,0.264,0.0872])*1e-4
        p10p=numpy.array([15.8,0.258,0.1997])*1e-4
        p10n=numpy.array([7.8,0.146,0.0729])*1e-4
        z10.errorbar(M,p10,[p10n,p10p],[Merrn,Merrp],fmt='o',capsize=4,color=CLR,ms=4)


        # https://arxiv.org/pdf/2403.08872
        CLR = (0.25,0.5,1.0)

        M=10**numpy.arange(8.25,11.80,0.5)
        p7=10**numpy.array([-2.40,-2.70,-3.35,-3.96,-4.35,-4.78,-5.38,-5.69])
        p7p=p7*(10**numpy.array([0.15,0.14,0.14,0.19,0.25,0.38,0.43,0.55])-1)
        p7n=p7*(1-1/10**numpy.array([0.24,0.20,0.21,0.33,0.58,numpy.inf,numpy.inf,numpy.inf]))
        weibel2024=z7.errorbar(M[:len(p7)],p7,[p7n,p7p],fmt='o',capsize=4,color=CLR,ms=5)

        M=10**numpy.arange(8.75,11.80,0.5)
        p8=10**numpy.array([-3.0,-3.64,-4.09,-4.33,-4.78,-5.54,-5.66])
        p8p=p8*(10**numpy.array([0.18,0.19,0.24,0.30,0.45,0.57,0.56])-1)
        p8n=p8*(1-1/10**numpy.array([0.28,0.33,0.55,1.39,numpy.inf,numpy.inf,numpy.inf]))
        z8.errorbar(M[:len(p8)],p8,[p8n,p8p],fmt='o',capsize=4,color=CLR,ms=5)
        
        M=10**numpy.arange(8.75,11.80,0.5)
        p9=10**numpy.array([-3.39,-3.81,-4.35,-4.79,-5.27,-5.61,-5.61])
        p9p=p9*(10**numpy.array([0.25,0.24,0.31,0.40,0.54,0.64,0.61])-1)
        p9n=p9*(1-1/10**numpy.array([0.64,0.52,1.54,numpy.inf,numpy.inf,numpy.inf,numpy.inf]))
        z9.errorbar(M[:len(p9)],p9,[p9n,p9p],fmt='o',capsize=4,color=CLR,ms=5)





        # MANUAL LEGEND
        song2016.set_label("Song et al. (2016)")
        stefanon2021.set_label("Stefanon et al. (2021)")
        weibel2024.set_label("Weibel et al. (2024)")
        z10.figure.legend(handles=[song2016,stefanon2021,weibel2024],
                          loc='upper center',
                          frameon=False,
                          bbox_to_anchor=(0.5,1),
                          ncols=5,
                          fontsize=12)
