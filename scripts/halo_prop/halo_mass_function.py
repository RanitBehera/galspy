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
# L50N640 = "/mnt/home/student/cranit/Data/MP_Gadget/Nishi/L50N640"
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
        # print(REDSHIFT)
        M, dn_dlogM = MassFunctionLiterature(model,COSMOLOGY,REDSHIFT,MASS_HR,'dn/dlnM')
        if PLOT_LMF:
            ax[0].plot(M,dn_dlogM*HUBBLE,label=model + label,lw=1,**kwargs)
        return M,dn_dlogM*HUBBLE
    
    M_st,mfhr_st = PlotLMF("Seith-Tormen","",ls="--",c='k')
    M_ps,mfhr_ps = PlotLMF("Press-Schechter","",ls=":",c='k')


    # BOX MF
    def PlotBMF(M,dn_dlogM,error,min_mass,right_skip_count,include_deviation,color,leg,marker,box_text):
        # Filters
        # if right_skip_count>0:
            # M,dn_dlogM,error = M[:-right_skip_count],dn_dlogM[:-right_skip_count],error[:-right_skip_count]
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
    
    M, dn_dlogM,error = MassFunction(M_DM,BOX_SIZE,BIN_SIZE)
    mask=(M>32*MASS_TABLE[1]*MASS_UNIT)
    M,dn_dlogM,error = M[mask],dn_dlogM[mask],error[mask]
    PlotBMF(M,dn_dlogM,error,HALO_DEF * MASS_TABLE[1] * MASS_UNIT,0,INCLUDE_DEVIATION,'r'," ",marker=" ",box_text=TEXT)

    M, dn_dlogM,error = MassFunction(M_GAS,BOX_SIZE,BIN_SIZE)
    mask=(M>32*MASS_TABLE[0]*MASS_UNIT)
    M,dn_dlogM,error = M[mask],dn_dlogM[mask],error[mask]
    PlotBMF(M,dn_dlogM,error,HALO_DEF * MASS_TABLE[0] * MASS_UNIT,0,INCLUDE_DEVIATION,'r'," ",marker=" ",box_text=TEXT)

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


    # --- Temporary for Astrid SHMF
    if numpy.round(REDSHIFT,1)==9.0:
        x = [7.023529411764706, 7.241176470588235, 7.576470588235294, 7.911764705882353, 8.323529411764707, 8.652941176470588, 8.994117647058824, 9.358823529411765, 9.7]
        y = [-2.3245823389021476, -2.5250596658711215, -2.9451073985680187, -3.403341288782816, -3.9761336515513124, -4.5680190930787585, -5.26491646778043, -5.837708830548926, -6.954653937947494]
    if numpy.round(REDSHIFT,1)==8.0:
        x = [7.012820317195012, 7.262820317195012, 7.512820317195012, 7.762820317195012, 8.025640927828276, 8.301281855656551, 8.532051086425781, 8.762820317195011, 8.961538461538462, 9.173076923076923, 9.371795067420372, 9.512820317195011, 9.66025660588191, 9.80128185565655, 10.012820317195011, 10.365384615384615]
        y = [-1.968912396380584, -2.1968914768212704, -2.445596100707992, -2.7564768805663933, -3.0777206693310246, -3.4196895271752665, -3.7202072981274386, -4.051813621431875, -4.352331866750472, -4.715025793674323, -5.056994651518566, -5.326424818851322, -5.678756211235369, -6.07253916487791, -6.7357508627539335, -7.233160110527377]
    if numpy.round(REDSHIFT,1)==7.0:
        x = [7.034246676275522, 7.335616612304624, 7.726027530406008, 8.061643829173903, 8.37671218488383, 8.684931330753344, 9.054794305796761, 9.342465508608308, 9.684931644290073, 9.897259971173433, 10.041095572579206, 10.369862661506687, 10.72602721686928]
        y = [-1.6536309734637742, -1.8994413493542073, -2.312848964853215, -2.636871454090015, -2.9832399691584945, -3.351955021526399, -3.8324017374559336, -4.2234633271232624, -4.78212266786691, -5.2067032962817565, -5.486033222387455, -6.335195502152641, -6.949719907475487]
    if numpy.round(REDSHIFT,1)==6.0:
        x = [7.031389081467508, 7.8799997802734545, 8.764999941635136, 9.409999663543728, 10.264999598312409, 11.060000453186001]
        y = [-1.378816988054881, -2.121951580331236, -2.9512194236923377, -3.707316542154029, -5.048780576307662, -6.829267843361102]
    if numpy.round(REDSHIFT,1)==5.0:
        x = [6.989949443575691, 7.713567423057761, 8.301507031386942, 9.055276680141938, 9.718592701269916, 10.351758433316727, 11.06030057816233, 11.422109567903366, 11.768844103199699]
        y = [-1.1951220261064828, -1.6585362449705308, -2.146341449798821, -2.7560971184616907, -3.5609750923552075, -4.414633921680551, -5.609755389538705, -6.756097118461691, -7.268292192757565]
    if numpy.round(REDSHIFT,1)==4.0:
        x = [6.994999388885403, 8.374999141692982, 9.215000185394315, 9.829999821472141, 10.340000357055718, 10.954999993133544, 11.405000061798106, 11.765000116729755]
        y = [-0.975609851408251, -1.8780484196687626, -2.536584943763459, -3.146341728922985, -3.707316542154029, -4.682926951810608, -5.536584664639295, -6.560974813231043]
    else:
        x = [6.994999388885403]
        y = [-0.975609851408251]
    X=numpy.power(10,x)
    Y=numpy.power(10,y)
    ax[0].plot(X,Y*HUBBLE,lw=2,color='k',label="Astrid",ls="-.")

    # --- Temporary for Astrid BHMF
    if numpy.round(REDSHIFT,1)==7.0:
        x = [4.699115219910853, 4.9911505787063755, 5.265486689814112, 5.513274537040976, 5.69026539351669, 5.778761226855087, 6.044247916669198, 6.318584432877474, 6.663717129635819, 7.132743344907056, 7.4070798611153315, 7.681415567122526]
        y = [-1.515267183074764, -1.5725190049458124, -1.8473281692523535, -2.0763359808934325, -2.5916031639681973, -2.9122136809402006, -4.4465650230373495, -5.190840017753193, -5.774809491904593, -6.438931988416657, -6.54198542503161, -6.862595417846729]
    if numpy.round(REDSHIFT,1)==6.0:
        x = [4.681415972223066, 4.973451331018588, 5.274336516208275, 5.504424710646813, 5.796460069442334, 6.061946759256446, 6.345133101858885, 6.5929201388846685, 6.92920381944993, 7.230088194438538, 7.4070798611153315, 7.654866898141115, 7.938053240743555, 8.185840277769339, 8.495575289353189]
        y = [-1.171755727691588, -1.2633586951009539, -1.5267176522803503, -1.7442747326374013, -2.488549727353244, -3.759542112270997, -4.423664084626177, -4.870228976624306, -5.213740432007483, -5.488549596314024, -5.660305324005612, -6.152672092826087, -6.370229697340021, -6.6450388616465625, -6.851145734876469]
    if numpy.round(REDSHIFT,1)==5.0:
        x = [4.716814467598641, 4.982301157412753, 5.256637673621028, 5.530973379628223, 5.796460069442334, 6.053097743063362, 6.318584432877474, 6.5929201388846685, 6.849557812505697, 7.141593171301221, 7.389380208327005, 8.21238894675075, 8.504424305546273, 8.743362326378975, 9.035397685174495, 9.557522048609634]
        y = [-0.9541983852560953, -0.9999999999999991, -1.2519084879738092, -1.4694655683308602, -1.984732751405625, -3.049618263093471, -3.6450384685288997, -4.011450338166365, -4.286259502472906, -4.629770957856083, -4.847328562370017, -5.7290076150822475, -6.09542053303348, -6.54198542503161, -6.656488544616824, -7.114504167898981]
    # if numpy.round(REDSHIFT,1)==4.0:
        # pass
    else:
        x = [4.716814467598641]
        y = [-0.9541983852560953]

    X=numpy.power(10,x)
    Y=numpy.power(10,y)
    ax[0].plot(X,Y*HUBBLE,lw=2,color='k',label="Astrid",ls="-.")




MF_from_PIG(L150N2040,63,True,'r',"L150N2040") # 9:26, 8:34 , 7:43 , 6:52, 5:63
MF_from_PIG(L150N2040,52,True,'g',"L150N2040") # 9:26, 8:34 , 7:43 , 6:52, 5:63
MF_from_PIG(L150N2040,67,True,'b',"L150N2040") # 9:26, 8:34 , 7:43 , 6:52, 5:63


plt.subplots_adjust(hspace=0)
plt.show()