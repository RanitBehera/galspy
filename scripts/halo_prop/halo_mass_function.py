import matplotlib.axes
import matplotlib.axis
import galspy
from galspy.utility.MassFunction import MassFunction, MassFunctionLiterature,LMF_OPTIONS
import numpy
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.lines as mlines
import matplotlib.patches as mpatches


L150N2040 = "/mnt/home/student/cranit/NINJA/simulations/L150N2040/SNAPS"
L50N640 = "/mnt/home/student/cranit/Data/MP_Gadget/Nishi/L50N640"
MASS_UNIT = 1e10
INCLUDE_DEVIATION = False





# --- PLOT HANDLES
if INCLUDE_DEVIATION:
    fig,ax = plt.subplots(2,1,figsize=(10,8),sharex=True,height_ratios=[3,1])
else:
    fig,ax = plt.subplots(1,1,figsize=(10,8))
    ax  =   [ax]    # to use ax[0] syntax
ax:list[matplotlib.axes.Axes]




def Extrapolated_MF(lit_m,lit_mf,mass):
    near_mf=numpy.empty(len(mass))
    for i,m in enumerate(mass):
        mass_diff_arr = lit_m-m
        min_mass_diff_ind = numpy.argmin(numpy.abs(mass_diff_arr))
        # Interpolate in log plot while values are in linear plot
        min_mass_diff = mass_diff_arr[min_mass_diff_ind]
        if min_mass_diff<0:slope_offset = 1
        else:slope_offset = -1
        delta_logy = numpy.log10(lit_mf[min_mass_diff_ind+slope_offset])-numpy.log10(lit_mf[min_mass_diff_ind])
        delta_logx = numpy.log10(lit_m[min_mass_diff_ind+slope_offset])-numpy.log10(lit_m[min_mass_diff_ind])
        slope = delta_logy/delta_logx
        d_logx = numpy.log10(m) - numpy.log10(lit_m[min_mass_diff_ind])
        d_logy = slope * d_logx
        near_mf[i] = 10**(numpy.log10(lit_mf[min_mass_diff_ind]) + d_logy)
    return near_mf


def Manual_Legend():
    pass
    # if True:
    #     dm_leg = False
    #     gas_leg = False
    #     star_leg = False
    
    # dm_line = mlines.Line2D([], [], color='k', marker='',markersize=8, label='Dark Matter')
    # star_line = mlines.Line2D([], [], color='k', marker='*',markersize=8, label='Stellar')
    # gas_line = mlines.Line2D([], [], color='k', marker='.',markersize=8, label='Gas')
    
    # htype=[]
    # hbox=[]
    # for i,PLOT in enumerate(CURVE_LIST):
    #     BOX         = PLOT[0]
    #     PLT_HALO    = Get_Options_List(PLOT[1])
    #     PLT_TYPE    = Get_Options_List(PLOT[2])
        
    #     box_patch = mpatches.Patch(color=COLORS_FOF[i],label=str(BOX).split("_")[-1])
    #     hbox.append(box_patch)


    #     if DM in PLT_TYPE and not dm_leg: dm_leg = True
    #     if GAS in PLT_TYPE and not gas_leg: gas_leg = True
    #     if STAR in PLT_TYPE and not star_leg: star_leg = True

    # if dm_leg:htype.append(dm_line)
    # if gas_leg:htype.append(gas_line)
    # if star_leg:htype.append(star_line)
    
    # leg1=ax[0].legend(handles=htype,fontsize=12, loc='lower left',ncol=1,frameon=False)
    # leg2=ax[0].legend(handles=hbox,fontsize=12, loc='upper right',ncol=1,frameon=True,title=LEGEND_TITLE)

    # ax[0].add_artist(leg1)
    # # ax[0].add_artist(leg2)



def MF_from_PIG(PATH,SN,PLOT_LMF=True,COLOR='r',TEXT=""):
    ROOT = galspy.NavigationRoot(PATH)
    COSMOLOGY   = ROOT.GetCosmology()
    SNAP_NUM    = SN
    SNAP        = ROOT.PIG(SNAP_NUM)
    REDSHIFT    = SNAP.Header.Redshift()
    HUBBLE      = SNAP.Header.HubbleParam()
    BOX_SIZE    = SNAP.Header.BoxSize()/1000
    MASS_HR     = numpy.logspace(7,12,100)
    HALO_DEF    = 32
    MASS_TABLE  = SNAP.Header.MassTable()
    BIN_SIZE    = 0.5
    REP_COLOR   = COLOR

    # LITERATURE MF
    def PlotLMF(model:LMF_OPTIONS,label:str="",**kwargs):
        # HUBBLE=1
        M, dn_dlogM = MassFunctionLiterature(model,COSMOLOGY,REDSHIFT,MASS_HR,'dn/dlnM')
        if PLOT_LMF:
            ax[0].plot(M,dn_dlogM*HUBBLE,label=model + label,lw=1,**kwargs)
        return M,dn_dlogM*HUBBLE
    
    M_st,mfhr_st = PlotLMF("Seith-Tormen","",ls="--",c='k')
    # M_ps,mfhr_ps = PlotLMF("Press-Schechter","",ls=":",c='k')


    # BOX MF
    def PlotBMF(M,dn_dlogM,error,min_mass,right_skip_count,include_deviation,color,leg,marker,box_text):
        # Filters
        if right_skip_count>0:
            M,dn_dlogM,error = M[:-right_skip_count],dn_dlogM[:-right_skip_count],error[:-right_skip_count]
        mass_mask = (M>min_mass)
        num_mask = (dn_dlogM>1e-20)
        mask = mass_mask & num_mask
        # M,dn_dlogM,error = M[mask],dn_dlogM[mask],error[mask]
    
        #Deviation
        ax[0].plot(M,dn_dlogM,'-',label= box_text + leg,lw=2,color=REP_COLOR,marker=marker)
        ax[0].fill_between(M,dn_dlogM-0.9*error,dn_dlogM+0.9*error,color=color,alpha=0.2,ec=None)

        if include_deviation:
            osmf = (dn_dlogM)                           # Observed simulation mass function (linear)
            eelmf = Extrapolated_MF(M_st,mfhr_st,M)     # Expected extrapolated litrarture mass function (linear)
            dev_by_fac =  osmf/eelmf
            dev_by_fac_p =  (osmf+0.7*error)/eelmf
            dev_by_fac_n =  (osmf-0.7*error)/eelmf
            ax[1].plot(M,dev_by_fac,'-',color=REP_COLOR)
            ax[1].fill_between(M,dev_by_fac_p,dev_by_fac_n,alpha=0.2,color=REP_COLOR,edgecolor=None)


    MBT_FOF        = SNAP.FOFGroups.MassByType()
    M_GAS,M_DM,M_U1,M_U2,M_STAR,M_BH = numpy.transpose(MBT_FOF) * MASS_UNIT
    M_TOTAL = M_GAS+M_DM+M_STAR+M_BH
    
    M, dn_dlogM,error = MassFunction(M_TOTAL,BOX_SIZE,BIN_SIZE)
    PlotBMF(M,dn_dlogM,error,HALO_DEF * MASS_TABLE[1] * MASS_UNIT,0,INCLUDE_DEVIATION,'r'," ",marker=" ",box_text=TEXT)
    M, dn_dlogM,error = MassFunction(M_GAS,BOX_SIZE,BIN_SIZE)
    PlotBMF(M,dn_dlogM,error,HALO_DEF * MASS_TABLE[1] * MASS_UNIT,0,INCLUDE_DEVIATION,'r'," ",marker=" ",box_text=TEXT)
    M, dn_dlogM,error = MassFunction(M_STAR,BOX_SIZE,BIN_SIZE)
    M, dn_dlogM,error = MassFunction(M_STAR,BOX_SIZE,BIN_SIZE)
    PlotBMF(M,dn_dlogM,error,HALO_DEF * MASS_TABLE[1] * MASS_UNIT,0,INCLUDE_DEVIATION,'r'," ",marker=" ",box_text=TEXT)

    M_BH = SNAP.FOFGroups.BlackholeMass()*MASS_UNIT
    M, dn_dlogM,error = MassFunction(M_BH,BOX_SIZE,BIN_SIZE)
    PlotBMF(M,dn_dlogM,error,HALO_DEF * MASS_TABLE[1] * MASS_UNIT,0,INCLUDE_DEVIATION,'r'," ",marker=" ",box_text=TEXT)


    # BEAUTIFICATION
    ax[0].set_xscale('log')
    ax[0].set_yscale('log')
    ax[0].grid(alpha=0.3)
    ax[0].tick_params(axis='both', which='major', labelsize=16)
    ax[0].tick_params(axis='both', which='minor', labelsize=12)
    ax[0].annotate(f"$z={numpy.round(REDSHIFT,2)}$",xy=(0,1),xytext=(10,-10),xycoords="axes fraction",textcoords="offset pixels",ha="left",va='top',fontsize=20)
    # ax[0].set_xlim(left=1e8,right=1e12)
    ax[0].set_ylabel("$dn/d\log(M/M_{\odot})$",fontsize=16)
    ax[-1].set_xlabel("$M/M_{\odot}$",fontsize=16)
    ax[0].legend()

    if INCLUDE_DEVIATION:
        # ax[1].yaxis.set_label_position("right")
        ax[1].yaxis.tick_right()
        ax[1].set_ylabel("FoF - ST\nDeviation\nby Factor",fontsize=10)
        ax[1].set_xscale('log')
        ax[1].axhline(1,ls='--',c='k',lw=1)
        ax[1].grid(alpha=0.3)
        # ax[1].set_yscale('log')
        ax[1].set_ylim(0.6,1.5)
        # Direct yscale('log') has issue of hiding default labels and ticks 
        # which is partly from ylim values also. 
        # So as work around we make lin-log conversion
        ticks= [0.8,1,1.25]
        ax[1].set_yticks(ticks,minor=False)
        ax[1].set_yticklabels(["$\\times$ " + str(t) for t in ticks])
        ax[1].tick_params(axis='both', which='major', labelsize=16)
        ax[1].tick_params(axis='both', which='minor', labelsize=12)

    ax[0].set_title("Halo Mass Function",fontsize=16)

MF_from_PIG(L150N2040,11,True,'r',"L150N2040")
MF_from_PIG(L50N640,20,True,'b',"L50N640")

plt.subplots_adjust(hspace=0)
plt.show()