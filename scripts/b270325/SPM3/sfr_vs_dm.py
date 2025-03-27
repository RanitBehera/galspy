import numpy as np
import galspy as gs
import matplotlib.pyplot as plt


table = np.loadtxt("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/SPM3/data/out_L150N2040_z7p0.csv",
                  usecols=(1,2))

tgid,rf_L_lam_UV = table.T
tgindex = (tgid-1).astype(np.int64)



# REDSHIFT = 7.0
SIM = gs.NavigationRoot(gs.NINJA.L150N2040)

def ForRedshift(REDSHIFT):
    SN = SIM.SnapNumFromRedshift(REDSHIFT)
    PIG = SIM.PIG(SN)

    dm_mass = PIG.FOFGroups.MassByType().T[1]*1e10
    dm_mass = dm_mass

    fof_sfr = PIG.FOFGroups.StarFormationRate()
    fof_sfr = fof_sfr

    # plt.plot(dm_mass,rf_L_lam_UV,'.',ms=1)
    # plt.plot(dm_mass,rf_L_lam_UV/dm_mass,'.',ms=2,label=f"z={REDSHIFT:.02f}")

    x=dm_mass
    y=fof_sfr#/dm_mass

    mask = fof_sfr>0.0001
    x=x[mask]
    y=y[mask]

    # plt.plot(x,y,'.',label=f"z={REDSHIFT:.02f}",ms=2,alpha=0.1)
    plt.hexbin(x,y,gridsize=30,cmap="Oranges",xscale='log',yscale='log',bins='log',label=f"z={REDSHIFT:.02f}")

    print(np.max(y),np.min(y))

    
    x_median = np.median(x)
    y_median = np.median(y)

    print(f"z={REDSHIFT}  ---> x_med={x_median:.02e} ; y_med={y_median:.02e}")

    plt.axvline(x_median,color='k',ls='--')
    plt.axhline(y_median,color='k',ls='--')


    plt.gca().set_xscale("log")
    plt.gca().set_yscale("log")
    
    # # plt.xlim(1e8,1e13)
    # # plt.ylim(1e28,1e33)
    
    plt.xlabel("DM Mass $(M_\odot/h)$")
    # plt.ylabel("SFR/DM Mass")
    plt.title("L150N2040")
    plt.legend()
    plt.axis("equal")
    # plt.colorbar()

plt.figure()
ForRedshift(7)
plt.figure()
ForRedshift(8)
plt.figure()
ForRedshift(9)

# plt.plot(1,1)



plt.show()


