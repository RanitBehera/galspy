import numpy as np
import galspy as gs
import matplotlib.pyplot as plt
import os
from constant_m2l_ratio import dark_matter_mass_to_AB_magnitude
from scipy.interpolate import interp1d

# {'flat': isflat,'H0': H0,'Om0': Om0,'Ob0': Ob0,'sigma8': sig8,'ns': ns}
COSMO_IUCAA = {'flat': True,'H0': 67.36,'Om0': 0.3153,'Ob0': 0.0493,'sigma8': 0.8111,'ns': 0.9649}
COSMO_NISER = {'flat': True,'H0': 69.70,'Om0': 0.2814,'Ob0': 0.0464,'sigma8': 0.816,'ns': 0.9667}
def cosmology_correction(MAB,phi,redshift,from_cos=COSMO_NISER,to_cos=COSMO_IUCAA):
    dm_mass_range=np.logspace(6,15,1000)
    mr_frm,mf_frm=gs.Utility.MassFunctionLiterature("Press-Schechter",from_cos,redshift,dm_mass_range,"dn/dlnM")
    mr_to,mf_to=gs.Utility.MassFunctionLiterature("Press-Schechter",to_cos,redshift,dm_mass_range,"dn/dlnM")

    MAB_from = dark_matter_mass_to_AB_magnitude(mr_frm,1e30)
    MAB_to = dark_matter_mass_to_AB_magnitude(mr_to,1e30)

    interp_frm = interp1d(MAB_from,mf_frm)
    interp_to = interp1d(MAB_to,mf_to)

    phi_frm = interp_frm(MAB)
    phi_to = interp_to(MAB)

    factor = phi_to/phi_frm

    return  MAB,phi*factor





def load_lf_to_axis(ax:plt.Axes,redshift,filedir,bins=20):
    files = [f for f in os.listdir(filedir) if os.path.isfile(filedir + os.sep + f) and str(f).startswith("out")]
    redshift_token = 'z'+str(float(np.round(redshift,1))).replace('.','p')
    target_files = [f for f in files if redshift_token in str(f)]


    for f in target_files:
        filepath = filedir + os.sep + f
        # -----
        tokens = str(f).removesuffix(".csv").split('_')
        sys_token = tokens[-1]
        imf_token = tokens[-2]
        model_token = tokens[-3]
        redshift_token = tokens[-4]
        box_token = '_'.join(tokens[1:-4])
        boxsize=float(box_token.removeprefix("L").split("N")[0])
        # -----
        if model_token not in ["stnb"]:continue
        # -----
        table = np.loadtxt(filepath,usecols=(1,5))
        TGID,M_AB = table.T
        TGID=TGID.astype(np.int64)
        # -----
        h=0.6736
        h=0.697 if box_token.startswith("L50N1008") else 0.6736
        
        bin_AB,bin_phi,error=gs.Utility.LumimosityFunction(M_AB,boxsize/h,bins)
        if box_token=="L50N1008":
            bin_AB,bin_phi = cosmology_correction(bin_AB,bin_phi,redshift)
            
        # -----
        ax.plot(bin_AB,bin_phi,'-',label=f"{box_token} ({model_token})")


        DUMP = False
        DUMP_DIR = "/mnt/home/student/cranit/RANIT/Repo/galspy/temp/share_anand/lf_with_bpass_chabrier300"
        if DUMP:
            dumpfilepath = DUMP_DIR +os.sep + str(f).replace("out","lf").replace(".csv",".txt")
            np.savetxt(dumpfilepath,np.column_stack((bin_AB,bin_phi)),header="bin_AB bin_phi",fmt="%.02f %.02e")
            print("Dumped :",str(f).replace("out","lf").replace(".csv",".txt") )