import numpy as np
import galspy as gs
import matplotlib.pyplot as plt




# REDSHIFT = 7.0
SIM = gs.NavigationRoot(gs.NINJA.L150N2040)

def ForRedshift(REDSHIFT):
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


plt.gca().set_xscale("log")
plt.gca().set_yscale("log")
    
    # plt.xlim(1e8,1e13)
    # plt.ylim(1e28,1e33)
    
plt.xlabel("DM Mass $(M_\odot/h)$")
plt.ylabel("$L_{\lambda=1500}^{rest}$/DM Mass")
plt.title("L150N2040")
plt.legend()
plt.axis("equal")
# plt.colorbar()

# plt.figure()
ForRedshift(7)
# plt.figure()
ForRedshift(8)
# plt.figure()
ForRedshift(9)

plt.legend()

plt.show()


