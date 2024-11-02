import numpy
from galspy.utility.MassFunction import MassFunction,MassFunctionLiterature, LMF_OPTIONS
from galspy.MPGadget import _PIG
from galspy.utility.Figure.Beautification import SetMyStyle

import matplotlib
import matplotlib.axes
import matplotlib.axis
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as mpatches




def GetLMF(model:LMF_OPTIONS,redshift,COSMOLOGY=None):
    if COSMOLOGY==None:COSMOLOGY = {'flat': True,'H0': 67.36,'Om0': 0.3153,'Ob0': 0.0493,'sigma8': 0.811,'ns': 0.9649}
    MASS_HR     = numpy.logspace(7,12,100)
    hubble=(COSMOLOGY["H0"]/100)
    M, dn_dlogM = MassFunctionLiterature(model,COSMOLOGY,redshift,MASS_HR,'dn/dlnM')
    dn_dlogM *=hubble
    return M,dn_dlogM

def PlotLMF(ax:plt.Axes,model:LMF_OPTIONS,redshift,COSMOLOGY=None,**kwargs):
        ax.plot(*GetLMF(model,redshift,COSMOLOGY),**kwargs)

def PlotBMF(ax:plt.Axes,M,phi,error,min_mass,right_skip_count,**kwargs):
        # if right_skip_count>0:
            # M,dn_dlogM,error = M[:-right_skip_count],dn_dlogM[:-right_skip_count],error[:-right_skip_count]
        mass_mask = (M>min_mass)
        num_mask = (phi>1e-10)
        mask = mass_mask & num_mask
        # M,dn_dlogM,error = M[mask],dn_dlogM[mask],error[mask]

        ax.plot(M,phi,'-',lw=2,color=kwargs["color"],marker=kwargs["marker"],label="")
        ax.fill_between(M,phi-0.9*error,phi+0.9*error,color=kwargs["color"],alpha=0.2,ec=None)

def PlotDeviation(ax:plt.Axes,M,phi,error,M_ref,phi_ref,**kwarg):
    phi_expected = numpy.interp(M,M_ref,phi_ref)
    dev_by_fac =  phi/phi_expected
    dev_by_fac_p =  (phi+0.7*error)/phi_expected
    dev_by_fac_n =  (phi-0.7*error)/phi_expected

    ax.plot(M,dev_by_fac,'-',color=kwarg["color"])
    ax.fill_between(M,dev_by_fac_p,dev_by_fac_n,alpha=0.2,color=kwarg["color"],ec=None)


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

        MBT_FOF        = snap.FOFGroups.MassByType()
        M_GAS,M_DM,M_U1,M_U2,M_STAR,M_BH = numpy.transpose(MBT_FOF) * MASS_UNIT
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
            PlotBMF(self.ax,M,dn_dlogM,error,HALO_DEF * MASS_TABLE[1] * MASS_UNIT,0,color=kwargs["color"],marker="*")
            self._add_mfun_ptype("star")

        if bh:
            M_BH = SNAP.FOFGroups.BlackholeMass()*MASS_UNIT
            M, dn_dlogM,error = MassFunction(M_BH,BOX_SIZE,BIN_SIZE)
            PlotBMF(self.ax,M,dn_dlogM,error,HALO_DEF * MASS_TABLE[1] * MASS_UNIT,0,color=kwargs["color"],marker="o")
            self._add_mfun_ptype("bh")

        self._pig_colors += kwargs["color"]


    def BeautifyPlot(self):
        SetMyStyle()

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

        leg1=self.ax.legend(handles=hands,fontsize=12, loc='upper left',ncol=1,frameon=False)
        leg2=self.ax.legend(handles=boxes,fontsize=12, loc='upper right',ncol=1,frameon=True,
                               title="z="+",".join([f"{zi:.02f}" for zi in numpy.unique(numpy.round(self._redshifts,2))]),
                               title_fontsize=14)

        self.ax.add_artist(leg1)
        self.ax.add_artist(leg2)

        # plt.subplots_adjust(left=0.15,right=0.85,top=0.9,bottom=0.15,hspace=0)
        if self.add_dev:
            return self.ax,self.ax_dev
        else:
             return self.ax