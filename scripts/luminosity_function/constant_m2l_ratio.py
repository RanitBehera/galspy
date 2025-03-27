import galspy as gs
import numpy as np



def dark_matter_mass_to_AB_magnitude(dm_mass,m2l_ratio,lam=1500):
    # dm_mass in M_solar
    # m2l_ratio in ergs s-1 A-1 Mo-1 
    # lam in Angstrom
    PC2CM = 3.086e18
    c= 3e8 * 1e10 # A Hz
    L_lam = m2l_ratio * dm_mass.astype(np.float64)
    f_lam = L_lam/(4*np.pi*(10*PC2CM)**2)
    f_nu = f_lam * ((lam**2)/c)

    # Oke & Gunn (1983) : with correction
    M_AB = -2.5 * np.log10(f_nu) - 48.6
    return M_AB



if __name__=="__main__":
    SIM = gs.NavigationRoot(gs.NINJA.L150N2040)
    redshift=7
    PIG=SIM.PIG(SIM.SnapNumFromRedshift(redshift))
    h=PIG.Header.HubbleParam()
    boxsize = PIG.Header.BoxSize()/1000 # Mpc

    M2L_RATIO = 1e30    # erg s-1 A-1 Mo-1
    MUNIT =1e10/h
    dm_mass = PIG.FOFGroups.MassByType().T[1]
    lower_limit = 32*PIG.Header.MassTable()[1]
    mask = dm_mass>lower_limit
    dm_mass = dm_mass[mask]*MUNIT
    M_AB = dark_matter_mass_to_AB_magnitude(dm_mass,M2L_RATIO)
    bin_AB,bin_Phi,error = gs.Utility.LumimosityFunction(M_AB,boxsize,20)

    PLOT=True
    if PLOT:
        import matplotlib.pyplot as plt
        plt.plot(bin_AB,bin_Phi)
        plt.yscale("log")
        plt.show()

    DUMP=False





