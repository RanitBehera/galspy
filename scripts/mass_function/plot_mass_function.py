import galspy as gs
import numpy as np
import matplotlib.pyplot as plt

L150N2040 = gs.NavigationRoot(gs.NINJA.L150N2040)
L250N2040 = gs.NavigationRoot(gs.NINJA.L250N2040)
L150N2040_WW = gs.NavigationRoot(gs.NINJA.L150N2040_WIND_WEAK)

SIMS = [L150N2040,L250N2040,L150N2040_WW]
COLORS = ['r','g','b']

REDSHIFT=11.5
for SIM,C in zip(SIMS,COLORS):
    SN=SIM.SnapNumFromRedshift(REDSHIFT)
    
    # Validation
    if SN is None:
        print(f"Skipping {SIM.sim_name} for redshift z={z} as the snapshot doesn't exist.")
        continue

    PIG = SIM.PIG(SN)

    h=PIG.Header.HubbleParam()
    z=PIG.Header.Redshift()
    box_size = PIG.Header.BoxSize()/1000

    # Dark Matter Mass Function
    fof_dm_mass = PIG.FOFGroups.MassByType().T[1]*1e10
    M,dn_dlogM,error=gs.Utility.MassFunction(fof_dm_mass,box_size)
    lower_limit = 32*PIG.Header.MassTable()[1]*1e10
    mask = M>lower_limit 
    plt.plot(M[mask],dn_dlogM[mask],label=f"{SIM.sim_name}; z={z:.02f}")
    
    # Dark Stellar Mass Function
    fof_stellar_mass = PIG.FOFGroups.MassByType().T[4]*1e10
    M,dn_dlogM,error=gs.Utility.MassFunction(fof_stellar_mass,box_size)
    lower_limit = 32*PIG.Header.MassTable()[4]*1e10
    mask = M>lower_limit 
    plt.plot(M[mask],dn_dlogM[mask],label=f"{SIM.sim_name}; z={z:.02f}",marker='*')


# ----- LITERATURE
plt.plot(*gs.Utility.MassFunctionLiterature(
                "Press-Schechter",
                SIMS[0].GetCosmology(),
                REDSHIFT,
                np.logspace(6,12,100),
                'dn/dlnM'
            ),
            color='k',
            ls='--',
            lw=1,
            label="Press-Schechter"
        )

plt.plot(*gs.Utility.MassFunctionLiterature(
                "Seith-Tormen",
                SIMS[0].GetCosmology(),
                REDSHIFT,
                np.logspace(6,12,100),
                'dn/dlnM'
            ),
            color='k',
            ls=':',
            lw=1,
            label="Seith-Tormen"
        )



# ----- BEAUTIFICATION
plt.xscale("log")
plt.yscale("log")

plt.xlabel("Mass $(M_\odot/h)$")
plt.ylabel("dn/dlnM")

plt.legend()

plt.show()