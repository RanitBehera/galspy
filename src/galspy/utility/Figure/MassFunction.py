import numpy
from galspy.utility.MassFunction import MassFunction,MassFunctionLiterature, LMF_OPTIONS
from galspy.MPGadget import _PIG

import matplotlib
import matplotlib.axes
import matplotlib.axis
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as mpatches

class MassFunctionFigure:
    def __init__(self):
        self.IncludeDeviation = True

        self._pig_colors=[]
        self._initialise_handles()

    def _initialise_handles(self):
        if self.IncludeDeviation:
            fig,ax = plt.subplots(2,1,figsize=(8,6),sharex=True,height_ratios=[3,1])
        else:
            fig,ax = plt.subplots(1,1,figsize=(10,8))
            ax  =   [ax]    # to use ax[0] syntax
        self.ax:list[matplotlib.axes.Axes] = ax

    def GetLMF(self,model:LMF_OPTIONS,redshift,COSMOLOGY=None):
        if COSMOLOGY==None:COSMOLOGY = {'flat': True,'H0': 67.36,'Om0': 0.3153,'Ob0': 0.0493,'sigma8': 0.811,'ns': 0.9649}
        MASS_HR     = numpy.logspace(7,12,100)
        hubble=(COSMOLOGY["H0"]/100)
        M, dn_dlogM = MassFunctionLiterature(model,COSMOLOGY,redshift,MASS_HR,'dn/dlnM')
        dn_dlogM *=hubble
        return M,dn_dlogM

    def PlotLMF(self,model:LMF_OPTIONS,redshift,COSMOLOGY=None,**kwargs):
        self.ax[0].plot(*self.GetLMF(model,redshift,COSMOLOGY),**kwargs)
        
    def PlotBMF(self,M,phi,error,min_mass,right_skip_count,**kwargs):
        # if right_skip_count>0:
            # M,dn_dlogM,error = M[:-right_skip_count],dn_dlogM[:-right_skip_count],error[:-right_skip_count]
        mass_mask = (M>min_mass)
        num_mask = (phi>1e-20)
        mask = mass_mask & num_mask
        # M,dn_dlogM,error = M[mask],dn_dlogM[mask],error[mask]

        self.ax[0].plot(M,phi,'-',lw=2,color=kwargs["color"],marker=kwargs["marker"],label="")
        self.ax[0].fill_between(M,phi-0.9*error,phi+0.9*error,color=kwargs["color"],alpha=0.2,ec=None)

    def PlotDeviation(self,M,phi,error,M_ref,phi_ref,**kwarg):
        if self.IncludeDeviation:
            phi_expected = numpy.interp(M,M_ref,phi_ref)
            dev_by_fac =  phi/phi_expected
            dev_by_fac_p =  (phi+0.7*error)/phi_expected
            dev_by_fac_n =  (phi-0.7*error)/phi_expected

            self.ax[1].plot(M,dev_by_fac,'-',color=kwarg["color"])
            self.ax[1].fill_between(M,dev_by_fac_p,dev_by_fac_n,alpha=0.2,color=kwarg["color"],ec=None)


    def AddPIG_MF(self,snap:_PIG,**kwargs):
        SNAP        = snap
        MASS_UNIT   = 1e10
        BOX_SIZE    = SNAP.Header.BoxSize()/1000
        REDSHIFT    = SNAP.Header.Redshift()
        BIN_SIZE    = 0.5
        HALO_DEF    = 32
        MASS_TABLE  = SNAP.Header.MassTable()

        MBT_FOF        = snap.FOFGroups.MassByType()
        M_GAS,M_DM,M_U1,M_U2,M_STAR,M_BH = numpy.transpose(MBT_FOF) * MASS_UNIT
        M_TOTAL = M_GAS+M_DM+M_STAR+M_BH
        
        if kwargs["dm"]:
            M, dn_dlogM,error = MassFunction(M_DM,BOX_SIZE,BIN_SIZE)
            mask=(M>32*MASS_TABLE[1]*MASS_UNIT)
            M,dn_dlogM,error = M[mask],dn_dlogM[mask],error[mask]
            self.PlotBMF(M,dn_dlogM,error,HALO_DEF * MASS_TABLE[1] * MASS_UNIT,0,color=kwargs["color"],marker=" ")
            self.PlotDeviation(M,dn_dlogM,error,*self.GetLMF("Seith-Tormen",REDSHIFT),color=kwargs["color"])

        if kwargs["gas"]:
            M, dn_dlogM,error = MassFunction(M_GAS,BOX_SIZE,BIN_SIZE)
            mask=(M>32*MASS_TABLE[0]*MASS_UNIT)
            M,dn_dlogM,error = M[mask],dn_dlogM[mask],error[mask]
            self.PlotBMF(M,dn_dlogM,error,HALO_DEF * MASS_TABLE[0] * MASS_UNIT,0,color=kwargs["color"],marker="x")

        if kwargs["star"]:
            M, dn_dlogM,error = MassFunction(M_STAR,BOX_SIZE,BIN_SIZE)
            self.PlotBMF(M,dn_dlogM,error,HALO_DEF * MASS_TABLE[1] * MASS_UNIT,0,color=kwargs["color"],marker="*")

        if kwargs["bh"]:
            M_BH = SNAP.FOFGroups.BlackholeMass()*MASS_UNIT
            M, dn_dlogM,error = MassFunction(M_BH,BOX_SIZE,BIN_SIZE)
            self.PlotBMF(M,dn_dlogM,error,HALO_DEF * MASS_TABLE[1] * MASS_UNIT,0,color=kwargs["color"],marker="o")

        self._pig_colors += kwargs["color"]

    def BeautifyPlot(self):
        _REDSHIFT = 9
        self.ax[0].set_xscale('log')
        self.ax[0].set_yscale('log')
        self.ax[0].grid(alpha=0.3)
        self.ax[0].tick_params(axis='both', which='major', labelsize=16)
        self.ax[0].tick_params(axis='both', which='minor', labelsize=12)
        # self.ax[0].set_xlim(left=1e8,right=1e12)
        self.ax[0].set_ylabel("$dn/d\log(M/M_{\odot})$",fontsize=16)
        self.ax[-1].set_xlabel("$M/M_{\odot}$",fontsize=16)
        self.ax[0].legend()

        if self.IncludeDeviation:
            # self.ax[1].yaxis.set_label_position("right")
            self.ax[1].yaxis.tick_right()
            self.ax[1].set_ylabel("FoF - ST\nDeviation\nby Factor",fontsize=10)
            self.ax[1].set_xscale('log')
            self.ax[1].axhline(1,ls='--',c='k',lw=1)
            self.ax[1].grid(alpha=0.3)
            # self.ax[1].set_yscale('log')
            self.ax[1].set_ylim(0.6,1.5)
            # Direct yscale('log') has issue of hiding default labels and ticks 
            # which is partly from ylim values also. 
            # So as work around we make lin-log conversion
            ticks= [0.8,1,1.25]
            self.ax[1].set_yticks(ticks,minor=False)
            self.ax[1].set_yticklabels(["$\\times$ " + str(t) for t in ticks])
            self.ax[1].tick_params(axis='both', which='major', labelsize=16)
            self.ax[1].tick_params(axis='both', which='minor', labelsize=12)

        self.ax[0].set_title("Halo Mass Function",fontsize=16)

        # MANUAL LEGEND    
        # self.ax[0].annotate(f"$z={numpy.round(_REDSHIFT,2)}$",xy=(0,0),xytext=(10,-10),xycoords="axes fraction",textcoords="offset pixels",ha="left",va='top',fontsize=20)
        
        dm_line = mlines.Line2D([], [], color='k', marker='',markersize=8, label='Dark Matter')
        star_line = mlines.Line2D([], [], color='k', marker='*',markersize=8, label='Stellar')
        gas_line = mlines.Line2D([], [], color='k', marker='x',markersize=8, label='Gas')
        bh_line = mlines.Line2D([], [], color='k', marker='o',markersize=8, label='BH')
    
        box_L150N2040 = mpatches.Patch(color='m',label="L150N2040")
        box_L250N2040 = mpatches.Patch(color='c',label="L250N2040")
        ST_line = mlines.Line2D([], [], color='k', ls='--',label="Seith-Tormen")

        leg1=self.ax[0].legend(handles=[dm_line,gas_line,star_line,bh_line],
                               fontsize=12, loc='upper left',ncol=1,frameon=False)
        leg2=self.ax[0].legend(handles=[box_L150N2040,box_L250N2040,ST_line],
                               fontsize=12, loc='upper right',ncol=1,frameon=True,title="z=9",title_fontsize=14)

        self.ax[0].add_artist(leg1)
        self.ax[0].add_artist(leg2)


        plt.subplots_adjust(left=0.15,right=0.85,top=0.9,bottom=0.15,hspace=0)