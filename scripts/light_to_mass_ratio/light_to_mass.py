import matplotlib.pyplot as plt
import numpy as np
import galspy as gs
from matplotlib.gridspec import GridSpec
from typing import Literal

# Initialise Figure
gs.SetPlotStyle()
fig = plt.figure(figsize=(12,8))
gsp = GridSpec(2,2,figure=fig)
ax00 = fig.add_subplot(gsp[0,0])
ax01 = fig.add_subplot(gsp[0,1])
ax10 = fig.add_subplot(gsp[1,0])
ax11 = fig.add_subplot(gsp[1,1])




SIM = gs.NavigationRoot(gs.NINJA.L150N2040)
SIM250 = gs.NavigationRoot(gs.NINJA.L250N2040)
SIM150WW = gs.NavigationRoot(gs.NINJA.L150N2040_WIND_WEAK)






def ForRedshift(BOX,REDSHIFT,Ax):
    red_to_name = {
        7:"z7p0",
        8:"z8p0",
        9:"z9p0",
    }

    table = np.loadtxt(f"/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/SPM3/data/out_L150N2040_{red_to_name[REDSHIFT]}.csv",
                    usecols=(1,2))

    tgid,rf_L_lam_UV = table.T
    tgindex = (tgid-1).astype(np.int64)






    SN = SIM.SnapNumFromRedshift(REDSHIFT)
    PIG = SIM.PIG(SN)

    dm_mass = PIG.FOFGroups.MassByType().T[1]*1e10
    dm_mass = dm_mass[tgindex]

    # plt.plot(dm_mass,rf_L_lam_UV,'.',ms=1)
    # plt.plot(dm_mass,rf_L_lam_UV/dm_mass,'.',ms=2,label=f"z={REDSHIFT:.02f}")

    x=dm_mass
    y=rf_L_lam_UV/dm_mass

    plt.plot(x,y,'.',label=f"z={REDSHIFT:.02f}",ms=2)
    # plt.hexbin(x,y,gridsize=30,cmap="Oranges",xscale='log',yscale='log',bins='log',label=f"z={REDSHIFT:.02f}")


    x_median = np.median(x)
    y_median = np.median(y)

    print(f"z={REDSHIFT}  ---> x_med={x_median:.02e} ; y_med={y_median:.02e}")

    plt.axvline(x_median,color='k',ls='--')
    plt.axhline(y_median,color='k',ls='--')