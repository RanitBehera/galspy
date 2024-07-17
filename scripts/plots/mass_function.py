from __future__ import annotations
import numpy, galspy,os
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as mpatches


from matplotlib import rc

import galspy.IO.MPGadget
rc('font',**{'family':'serif','serif':['Roboto']})
rc('text', usetex=True)


import galspy.IO
from galspy.utility.MassFunction import MassFunction, MassFunctionLiterature,LMF_OPTIONS

L50N640 = "/mnt/home/student/cranit/Work/test_para_rock/L50N640"
OUT_L50N640 = "/mnt/home/student/cranit/Work/test_para_rock/OUT_L50N640"



# --- FLAGS
FOF,ROCKSTAR    = 1,2       # Don't change this
DM,GAS,STAR,BH  = 1,2,4,8   # Don't change this

# Skip points structure [[fof-dm,fof-gas,fof-star],[vir-dm,vir-gas,vir-star]]
CURVE_LIST       = [ 
        [L50N640, ROCKSTAR, (DM+GAS+STAR),[[1,2,4],[1,1,4]]]
    ]

COLORS_FOF  = ['deeppink','deepskyblue','springgreen','gold','magenta']
# COLORS_RKS  = ['r','lime','b','m','cyan']
COLORS_RKS = COLORS_FOF
# COLORS_FOF  = ['tab:blue','tab:orange','tab:green','g']



SNAP_NUM    = 36
BIN_SIZE    = 0.5
MASS_HR     = numpy.logspace(7,12,100) # High resolution mass for literature mass function plot
SAVE_PATH   = "temp/test.png" 
INCLUDE_DEVIATION = False
# INCLUDE_LMF = True          # Deviation axis and its plot also needs to be adapted. Not implemeted for now.



# LEGEND_TITLE    = "Friends-of-Friends"
LEGEND_TITLE    = "ROCKSTAR-Galaxies"


# --- COMMON AUTO-FLAGS
# Make sure following parameters are same in all simulations
REFBOX      = galspy.IO.MPGadget.NavigationRoot(OUT_L50N640)
COSMOLOGY   = {
                # Get these from simulation run files
                'flat': True,
                'H0': 69.7,
                'Om0': 0.2814,
                'Ob0': 0.0464,
                'sigma8': 0.81,
                'ns': 0.971
                }
SNAP= REFBOX.RSG(SNAP_NUM)
REDSHIFT    = 8
HUBBLE      = 0.697

# --- HELPER FUNCTION
def Get_Options_List(value):
    # 7  = 4 + 2 + 1
    # 13 = 8 + 4 + 1
    seq = []
    while value>0:
        p= 1
        while p*2 <= value:p *= 2
        seq.append(p)
        value -= p
    return seq

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


# --- PLOT HANDLES
if INCLUDE_DEVIATION:
    fig,ax = plt.subplots(2,1,figsize=(10,8),sharex=True,height_ratios=[3,1])
else:
    fig,ax = plt.subplots(1,1,figsize=(10,8))
    ax  =   [ax]    # to use ax[0] syntax


# --- PLOT HELPER FUNCTION
# Literature mass function
def PlotLMF(model:LMF_OPTIONS,label:str="",**kwargs):
    # HUBBLE=1
    M, dn_dlogM = MassFunctionLiterature(model,COSMOLOGY,REDSHIFT,MASS_HR,'dn/dlnM')
    ax[0].plot(M,dn_dlogM*HUBBLE,label=model + label,lw=1,**kwargs)
    return M,dn_dlogM*HUBBLE

M_st,mfhr_st = PlotLMF("Seith-Tormen","",ls="--",c='k')
M_ps,mfhr_ps = PlotLMF("Press-Schechter","",ls=":",c='k')
# M_ps,mfhr_ps = PlotLMF("Comparat(z=0)","",ls="-",c='k')




# Box mass function
def PlotBMF(M,dn_dlogM,error,min_mass,right_skip_count,include_deviation,color,leg,marker):
    # Filters
    if right_skip_count>0:
        M,dn_dlogM,error = M[:-right_skip_count],dn_dlogM[:-right_skip_count],error[:-right_skip_count]
    mass_mask = (M>min_mass)
    num_mask = (dn_dlogM>1e-20)
    mask = mass_mask & num_mask
    M,dn_dlogM,error = M[mask],dn_dlogM[mask],error[mask]
    
    #Deviation
    ax[0].plot(M,dn_dlogM,'-',label= BOX_TEXT + leg,lw=2,color=color,marker=marker)
    ax[0].fill_between(M,dn_dlogM-0.9*error,dn_dlogM+0.9*error,color=color,alpha=0.2,ec=None)

    if include_deviation:
        osmf = (dn_dlogM)                           # Observed simulation mass function (linear)
        eelmf = Extrapolated_MF(M_st,mfhr_st,M)     # Expected extrapolated litrarture mass function (linear)
        dev_by_fac =  osmf/eelmf
        dev_by_fac_p =  (osmf+0.7*error)/eelmf
        dev_by_fac_n =  (osmf-0.7*error)/eelmf
        ax[1].plot(M,dev_by_fac,'-',color=color)
        ax[1].fill_between(M,dev_by_fac_p,dev_by_fac_n,alpha=0.2,color=color,edgecolor=None)





# --- PLOT ROUTINE
for i,PLOT in enumerate(CURVE_LIST):
    # --- AUTO-FLAGS
    SIM         = PLOT[0]
    PLT_HALO    = Get_Options_List(PLOT[1])
    PLT_TYPE    = Get_Options_List(PLOT[2])
    # ---

    CFG         = galspy.RockstarCFG(SIM)
    BOX_TEXT    = os.path.basename(CFG.INBASE)
    BOX         = galspy.NavigationRoot(CFG.OUTBASE)
    LINKED_BOX  = galspy.NavigationRoot(CFG.INBASE)
    COSMOLOGY   = BOX.GetCosmology("MassFunctionLitrature")

    # ---
    if not ONLY_PIG: SNAP = BOX.RSG(SNAP_NUM)
    if ONLY_PIG : SNAP = LINKED_BOX.PART(SNAP_NUM)
    # ---
    REDSHIFT    = (1/SNAP.Attribute.Time())-1
    HUBBLE      = SNAP.Attribute.HubbleParam()
    BOX_SIZE    = (SNAP.Attribute.BoxSize()/1000)
    MASS_UNIT   = 10**10
    MASS_TABLE  = SNAP.Attribute.MassTable()
    if not ONLY_PIG:HALO_DEF    = CFG.MIN_HALO_PARTICLES
    if ONLY_PIG: HALO_DEF = 32
    # ---
    RIGHT_SKIP_FOF  = PLOT[3][0]
    RIGHT_SKIP_RKS  = PLOT[3][1]