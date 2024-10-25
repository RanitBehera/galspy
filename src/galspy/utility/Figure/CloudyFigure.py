import numpy
import matplotlib.pyplot as plt
from galspec.Cloudy import CloudyOutputReader
from matplotlib.gridspec import GridSpec
import galspy.utility.Figure.Beautification as bty
import matplotlib.lines as mlines
import matplotlib.patches as mpatches


def CloudySpecAndZone(out:CloudyOutputReader):
    fig=plt.figure(figsize=(12,8))
    gs = GridSpec(3,2)
    ax_spec     = fig.add_subplot(gs[0:3,0])
    ax_den    = fig.add_subplot(gs[2,1])
    ax_temp    = fig.add_subplot(gs[1,1])
    ax_ionfr    = fig.add_subplot(gs[0,1])

    # =========== SPECTRA
    con = out.Spectrum.Continuum
    ax_spec.plot(con.Frequency,con.Incident,c='b',lw=1,alpha=1,label="Incident")
    ax_spec.plot(con.Frequency,con.DiffuseOut,c='tab:blue',lw=1,alpha=1,label="Diffuse Out")
    ax_spec.plot(con.Frequency,con.Total,c='r',lw=1,alpha=1,label="Total")

    #region
    # egy = out.Spectrum.DiffuseContinuum.Energy
    # dout= out.Spectrum.DiffuseContinuum.ConEmitLocal
    # dline = out.Spectrum.DiffuseContinuum.DiffuseLineEmission

    # egy2 = out.Spectrum.TwoPhotonContinuum.Energy
    # tw  = out.Spectrum.TwoPhotonContinuum.nuFnu

    # D=out.Overview.Depth[-2]
    # dD=out.Overview.Depth[-1]-out.Overview.Depth[-2]
    # # print(D)
    # R0=3*(0.5*3.086e18)
    # R=R0+D
    # V=(4*numpy.pi)*(4*numpy.pi)*(R**2)*dD
    # ax_spec.plot(egy,dout*V/egy,'-k',label="Only Contunuum")
    # # ax_spec.plot(egy,dout,'-g')
    # # ax_spec.plot(egy2,tw,label="Two Ph")
    # # ax_spec.plot(egy,(dout+dline+tw)*V/egy)
    #endregion






    ax_spec.set_xscale('log')
    ax_spec.set_yscale('log')
    ax_spec.set_xlim(100,10000)
    ax_spec.set_ylim(1e25,1e38)
    # bty.AddRydebergScale(ax_spec)
    # bty.AttachSpectraLines(ax_spec)

    ax_spec.set_xlabel("Angstrom")
    ax_spec.set_ylabel("Flux")

    LB_L = 1400
    LB_R = 1500
    HB_L = 2500
    HB_R = 2600

    mask_LB = (con.Frequency>LB_L)&(con.Frequency<LB_R)
    mask_HB = (con.Frequency>HB_L)&(con.Frequency<HB_R)

    LB_Lf,LB_Rf = con.Frequency[mask_LB][[0,-1]][::-1]
    HB_Lf,HB_Rf = con.Frequency[mask_HB][[0,-1]][::-1]

    ax_spec.axvspan(LB_Lf,LB_Rf,color='k',alpha=0.1,ec=None)
    ax_spec.axvspan(HB_Lf,HB_Rf,color='k',alpha=0.1,ec=None)


    def Integrate(ang,sflux,intg_mask):
        lam = ang[intg_mask][::-1]
        sflux = sflux[intg_mask][:-1]
        dlam = numpy.diff(lam)
        flux = numpy.sum(sflux*dlam)
        return flux
    
    flx_in_LB=Integrate(con.Frequency,con.Incident,mask_LB)/(LB_Rf-LB_Lf)
    flx_out_LB=Integrate(con.Frequency,con.DiffuseOut,mask_LB)/(LB_Rf-LB_Lf)
    flx_tot_LB=Integrate(con.Frequency,con.Total,mask_LB)/(LB_Rf-LB_Lf)
    
    flx_in_HB=Integrate(con.Frequency,con.Incident,mask_HB)/(HB_Rf-HB_Lf)
    flx_out_HB=Integrate(con.Frequency,con.DiffuseOut,mask_HB)/(HB_Rf-HB_Lf)
    flx_tot_HB=Integrate(con.Frequency,con.Total,mask_HB)/(HB_Rf-HB_Lf)

    MARKER_SIZE = 10
    ax_spec.plot(0.5*(LB_Lf+LB_Rf),flx_in_LB,mec='b',mfc='w',marker='.',ms=MARKER_SIZE)
    ax_spec.plot(0.5*(LB_Lf+LB_Rf),flx_out_LB,mec='tab:blue',mfc='w',marker='.',ms=MARKER_SIZE)
    ax_spec.plot(0.5*(LB_Lf+LB_Rf),flx_tot_LB,mec='r',mfc='w',marker='.',ms=MARKER_SIZE)
    
    ax_spec.plot(0.5*(HB_Lf+HB_Rf),flx_in_HB,mec='b',mfc='w',marker='.',ms=MARKER_SIZE)
    ax_spec.plot(0.5*(HB_Lf+HB_Rf),flx_out_HB,mec='tab:blue',mfc='w',marker='.',ms=MARKER_SIZE)
    ax_spec.plot(0.5*(HB_Lf+HB_Rf),flx_tot_HB,mec='r',mfc='w',marker='.',ms=MARKER_SIZE)

    # Flux ratio
    rat_in = flx_in_LB/flx_in_HB
    rat_out = flx_out_LB/flx_out_HB
    rat_tot = flx_tot_LB/flx_tot_HB


    ax_spec.annotate(f"$R_{{in}}$={rat_in:.02f}\t\t$R_{{out}}$={rat_out:.02f}\t\t$R_{{tot}}$={rat_tot:.02f}",
                     xy=(0.5,1),xytext=(0,4),
                     xycoords="axes fraction", textcoords="offset pixels",
                     ha="center",va="bottom",fontsize=14)



    ax_spec.legend(loc='upper left')

    # ============ IONISATION STRUCURURE
    CM_IN_PARSEC = 3.086e18
    cloud = out.Overview
    depths = cloud.Depth/CM_IN_PARSEC

    alpha=[0.08,0.03]
    d_prev = depths[0]
    for i in range(len(depths)):
        if i==len(depths)-1:d_next=depths[-1]
        else:d_next=0.5*(depths[i]+depths[i+1])
        ax_den.axvspan(d_prev,d_next,color='k',alpha=alpha[i%2],ec=None)
        ax_temp.axvspan(d_prev,d_next,color='k',alpha=alpha[i%2],ec=None)
        ax_ionfr.axvspan(d_prev,d_next,color='k',alpha=alpha[i%2],ec=None)
        d_prev=d_next

        

    ax_den.plot(depths,cloud.HydrogenDensity,'.-',label="Hydrogen Density",markersize=5)
    ax_den.plot(depths,cloud.ElectronDensity,'.-',label="Electron Density",markersize=5)
    ax_temp.plot(depths,cloud.TemperatureElectron,'.-',markersize=5)
    
    ax_ionfr.plot(depths,out.Elements.Hydrogen.HI,color='g',ls='-')
    ax_ionfr.plot(depths,out.Elements.Hydrogen.HII,color='g',ls=(0,(1,1,5,1)))

    ax_ionfr.plot(depths,out.Elements.Helium.HeI,color='m',ls='-')
    ax_ionfr.plot(depths,out.Elements.Helium.HeII,color='m',ls=(0,(1,1,5,1)))    
    ax_ionfr.plot(depths,out.Elements.Helium.HeIII,color='m',ls=(0,(1,1,1,1,5,1)))    

    ax_ionfr.plot(depths,out.Elements.Oxygen.OI,color='r',ls='-')
    ax_ionfr.plot(depths,out.Elements.Oxygen.OII,color='r',ls=(0,(1,1,5,1)))    
    ax_ionfr.plot(depths,out.Elements.Oxygen.OIII,color='r',ls=(0,(1,1,1,1,5,1)))    
    ax_ionfr.plot(depths,out.Elements.Oxygen.OIV,color='r',ls=(0,(1,1,1,1,1,1,5,1)))    



    # Beautification
    for ax in [ax_den,ax_temp,ax_ionfr]:
        ax.set_xscale('log')
        ax.set_xlim(depths[0],depths[-1])
        ax.yaxis.tick_right()      # Move ticks to the right
        ax.yaxis.set_label_position("right")
        
    ax_den.set_yscale('log')
    ax_ionfr.set_yscale('log')

    ax_ionfr.get_xaxis().set_visible(False)
    ax_temp.get_xaxis().set_visible(False)


    ax_den.set_xlabel("Depth (Parsec)")
    ax_den.set_ylabel("Number\nDensity\n$(cm^{-3})$")
    ax_temp.set_ylabel("$T (K)$")
    ax_ionfr.set_ylabel("Ion\nFraction")


    # Legend
    ax_den.legend(fontsize=12, loc='lower left',ncol=1,frameon=False)

    # ---------------
    H_line  = mlines.Line2D([], [], color='g', label='H')
    He_line = mlines.Line2D([], [], color='m', label='He')
    O_line  = mlines.Line2D([], [], color='r', label='O')

    I_line      = mlines.Line2D([], [], color='k', ls='-' ,label='I')
    II_line     = mlines.Line2D([], [], color='k',ls=(2,(1,1,5,1)),label='II')
    III_line    = mlines.Line2D([], [], color='k',ls=(4,(1,1,1,1,5,1)),label='III')
    IV_line     = mlines.Line2D([], [], color='k',ls=(6,(1,1,1,1,1,1,5,1)),label='IV')


    leg_elem=ax_ionfr.legend(handles=[H_line,He_line,O_line],
                               fontsize=12, loc='center',ncol=3,frameon=False,bbox_to_anchor=(0.5, 1.2))
    
    leg_ion=ax_ionfr.legend(handles=[I_line,II_line,III_line,IV_line],
                               fontsize=12, loc='center',ncol=4,frameon=False,bbox_to_anchor=(0.5, 1.1))
    

    ax_ionfr.add_artist(leg_elem)
    ax_ionfr.add_artist(leg_ion)


    ax_temp.annotate(f"$R_0$={out.Output.InnerRadius} pc",
                    xy=(0,0.5),xytext=(4,0),
                    xycoords="axes fraction", textcoords="offset pixels",
                    ha="left",va="center",fontsize=12)

    ax_ionfr.set_ylim(1e-10,1)


    plt.subplots_adjust(hspace=0.05,wspace=0.05)

    # plt.show()

