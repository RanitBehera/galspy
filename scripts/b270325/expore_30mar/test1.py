import numpy as np
import galspy as gs
from galspy.Utility.Visualization import Cube3D
import matplotlib.pyplot as plt
from galspy.MPGadget import _Sim
from matplotlib.patches import Circle



SIM_150 = gs.NavigationRoot(gs.NINJA.L150N2040)
SIM_150_WW = gs.NavigationRoot(gs.NINJA.L150N2040_WIND_WEAK)

gs.SetPlotStyle()

REDSHIFT=7
# TARGET_INDEX=2

def ForBox(SIM:_Sim,ax:plt.Axes,ax_spec:plt.Axes,TARGET_INDEX):
    print("BOX",SIM.sim_name)
    PIG=SIM.PIG(SIM.SnapNumFromRedshift(REDSHIFT))

    fof_gid = PIG.FOFGroups.GroupID()
    fof_mbt=PIG.FOFGroups.MassByType()
    fof_lbt=PIG.FOFGroups.LengthByType()
    fof_pos=PIG.FOFGroups.MassCenterPosition()

    tgid = fof_gid[TARGET_INDEX]
    tpos=fof_pos[tgid-1]
    tmbt=fof_mbt[tgid-1]
    tlbt=fof_lbt[tgid-1]

    print(tgid,"---->",tpos)


    # dm_gid = PIG.DarkMatter.GroupID()
    # gas_gid = PIG.Gas.GroupID()
    star_gid = PIG.Star.GroupID()


    # mask_dm = dm_gid==tgid
    # mask_gas = gas_gid==tgid
    mask_star = star_gid==tgid


    # dm_pos = PIG.DarkMatter.Position()[mask_dm]
    # gas_pos = PIG.Gas.Position()[mask_gas]
    star_pos = PIG.Star.Position()[mask_star]



    # Cube3d

    # c3d = Cube3D()
    # c3d.add_points(star_pos,points_size=5)
    # ax=c3d.show(False)
    # ax.set_title(f"$M_*$ = {tmbt[4]*1e10/0.6736:.02e}\n$N_*$={tlbt[4]}")
    




    spm=gs.PIGSpectrophotometry(PIG)
    DUMP_DIR = "/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/light_generation/data_temp1234"
    imgs=spm.get_photometry_images(int(tgid))
    timg = imgs["F115W"]

    timg = (timg/np.max(timg))**0.2


    x,y,z=star_pos.T
    plt.figure()
    ax=plt.gca()

    CX={"L150N2040":131463,"L150N2040_WIND_WEAK":131460}[SIM.sim_name]
    CY=15102

    CX=0
    scale = 8*0.6736 # 8 is for redshift 7 =(1+z) and then h for hubble
    CY=2802.5*scale
    CZ={"L150N2040":17040.5*scale,"L150N2040_WIND_WEAK":17040*scale}[SIM.sim_name]



    # h=ax.imshow(timg.T,cmap="gist_gray",origin="lower")
    h=ax.imshow(timg.T,cmap="gist_gray",origin="lower",extent=((np.min(y)-CY)/scale,(np.max(y)-CY)/scale,(np.min(z)-CZ)/scale,(np.max(z)-CZ)/scale))
    # plt.colorbar(h)


    # ax.set_xlim(cx-10,cx+10)
    # ax.set_ylim(cy-10,cy+10)
    # ax.set_title(SIM.sim_name)
    # ax[0].set_gca().set_aspect("equal")
    # plt.colorbar()
    ax.set_xlim(-50/scale,50/scale)
    ax.set_ylim(-50/scale,50/scale)

    # ax.axvline(0,0.5-0.125,0.5+0.125,color='w',ls='--',lw=1,alpha=0.5)
    # ax.axhline(0,0.5-0.125,0.5+0.125,color='w',ls='--',lw=1,alpha=0.5)

    ax.set_xlabel("Y (pKpc)")
    ax.set_ylabel("Z (pKpc)")

    ax.set_xticks([-7.5,-5,-2.5,0,2.5,5,7.5])
    ax.set_yticks([-7.5,-5,-2.5,0,2.5,5,7.5])

    from matplotlib.font_manager import FontProperties
    font_prop = FontProperties(fname='/mnt/home/student/cranit/.fonts/Roboto-Regular.ttf',)
    # ax.annotate(f"z=7",(0,1),(16,-16),"axes fraction","offset pixels",ha="left",va="top",fontsize=16,color='w',fontproperties=font_prop)
    # ax.annotate(f"F115W",(1,0),(-16,16),"axes fraction","offset pixels",ha="right",va="bottom",fontsize=10,color='w',fontproperties=font_prop)

    ## ax.annotate(f"$N_*$={len(star_pos)}\n$M_*$={tmbt[4]*1e10/0.6736:.02e}",(0,0),(16,16),"axes fraction","offset pixels",ha="left",va="bottom",fontsize=12,color='w',fontproperties=font_prop)
    # ax.annotate("$N_*$="+f"{len(star_pos)}"+
    #             "\n$M_*$="+f"{10**(np.log10(tmbt[4]*1e10/0.6736)%1):.02f}"+
    #             "$\\times 10^{10}M_\odot$",(0,0),(16,16),
    #             "axes fraction","offset pixels",ha="left",va="bottom",fontsize=12,color='w',fontproperties=font_prop)
    ax.set_title(f"{SIM.sim_name}")

    # circ=Circle((0,0),2.5,fill=False,ec='w',ls='--',alpha=0.6)
    # ax.add_patch(circ)


# \\times 10^${int(np.log10(tmbt[4]*1e10/0.6736))}

    # r=np.linalg.norm(star_pos.T[0:1].T-np.array([CX-CY]),axis=1)
    # ax_spec.hist(r,bins=100)





    # wl_rest_st,wl_rest_stnb,summed_spec_st,summed_spec_stnb=spm.get_light_dict(tgid,DUMP_DIR)
    # ax_spec.plot(wl_rest_st,summed_spec_st,label=f"{SIM.sim_name} : Stellar")
    # ax_spec.plot(wl_rest_stnb,summed_spec_stnb,label=f"{SIM.sim_name} :Stellar + Nebular")
    # ax_spec.set_xlim(300,10000)
    # ax_spec.set_ylim(1e-5*np.max(summed_spec_stnb),1e1*np.max(summed_spec_stnb))


    # np.savetxt(f"/mnt/home/student/cranit/RANIT/Repo/galspy/temp/share_anand/img_and_spec/{SIM.sim_name}_z7p0_st_gid{TARGET_INDEX+1}.txt",
    #            np.column_stack((wl_rest_st,summed_spec_st)),fmt="%.02f %.02e",header="Wavelength in Angstrom\nSpectral Luminosity in Solar Luminosity per Angstrom\nWavelength Spectral_Luminosity")

    # np.savetxt(f"/mnt/home/student/cranit/RANIT/Repo/galspy/temp/share_anand/img_and_spec/{SIM.sim_name}_z7p0_stnb_gid{TARGET_INDEX+1}.txt",
    #            np.column_stack((wl_rest_stnb,summed_spec_stnb)),fmt="%.02f %.02e",header="Wavelength in Angstrom\nSpectral Luminosity in Solar Luminosity per Angstrom\nWavelength Spectral_Luminosity")

# plt.figure(SIM.sim_name)

from matplotlib.gridspec import GridSpec

def DoForTarget(TARGET_INDEX):
    fig=plt.figure()
    gsp=GridSpec(2,2)
    ax_L150 = fig.add_subplot(gsp[0,0])
    ax_L150WW = fig.add_subplot(gsp[0,1])
    ax_spec=fig.add_subplot(gsp[1,:])

    ForBox(SIM_150_WW,ax_L150WW,ax_spec,TARGET_INDEX)
    ForBox(SIM_150,ax_L150,ax_spec,TARGET_INDEX)

    ax_spec.set_yscale("log")
    # ax_spec.set_xscale("log")
    # ax_spec.legend()
    plt.show()



# for i in range(0,3):
DoForTarget(1)