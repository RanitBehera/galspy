import numpy as np
import os

def dark_matter_mass_to_AB_magnitude(dm_mass,m2l_ratio,lam=1500):
    # dm_mass in M_solar
    # m2l_ratio in ergs s-1 A-1 Mo-1 
    # lam in Angstrom
    PC2CM = 3.086e18
    c= 3e8 * 1e10 # A Hz
    L_lam = m2l_ratio * dm_mass.astype(np.float64)
    f_lam = L_lam/(4*np.pi*(10*PC2CM)**2)
    f_nu = f_lam * ((lam**2)/c)
    # Oke & Gunn (1983) : with sign correction
    M_AB = -2.5 * np.log10(f_nu) - 48.6
    return M_AB



if __name__=="__main__":
    import galspy as gs

    M2L_RATIO = 1e30    # erg s-1 A-1 Mo-1
    MIN_DM_COUNT = 16
    def LF_for_BOX(snap_path,redshift):
        SIM = gs.NavigationRoot(snap_path)
        PIG=SIM.PIG(SIM.SnapNumFromRedshift(redshift))
        h=PIG.Header.HubbleParam()
        boxsize = PIG.Header.BoxSize()/1000 # Mpc

        MUNIT =1e10/h
        dm_mass = PIG.FOFGroups.MassByType().T[1]
        lower_limit = MIN_DM_COUNT*PIG.Header.MassTable()[1]
        mask = dm_mass>lower_limit
        dm_mass = dm_mass[mask]*MUNIT
        M_AB = dark_matter_mass_to_AB_magnitude(dm_mass,M2L_RATIO)
        bin_AB,bin_Phi,error = gs.Utility.LumimosityFunction(M_AB,boxsize/h,8)
        return bin_AB,bin_Phi,error, SIM

    # -------------------------------------------
    REDSHIFT=14
    SNAPPATH = gs.NINJA.L150N2040_WIND_WEAK
    # -------------------------------------------
    bin_AB,bin_Phi,error, SIM = LF_for_BOX(SNAPPATH,REDSHIFT)
    
    PLOT=True
    if PLOT:
        import matplotlib.pyplot as plt
        from load_observation import load_obs_to_axis
        load_obs_to_axis(plt.gca(),REDSHIFT,["Bouwens+21"])
        plt.plot(bin_AB,bin_Phi)
        plt.yscale("log")
        plt.show()
        
    DUMP=True
    if DUMP:
        DUMP_DIR = "/mnt/home/student/cranit/RANIT/Repo/galspy/temp/share_anand/lf_with_const_m2l_ratio"
        filename = f"LF_{SIM.sim_name}_z{str(float(np.round(REDSHIFT,1))).replace('.','p')}.txt"
        filepath = DUMP_DIR + os.sep + filename
        np.savetxt(filepath,np.column_stack((bin_AB,bin_Phi)),fmt="%.02f %.02e",
                    header=f"Min DM Count={MIN_DM_COUNT}\nM2L_ratio={M2L_RATIO} erg s-1 A-1 Mo-1\nlam=1500A\nbin_AB bin_phi")











