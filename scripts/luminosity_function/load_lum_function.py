import numpy as np
import galspy as gs
import matplotlib.pyplot as plt
import os


h=0.6736

def load_lf_to_axis(ax:plt.Axes,redshift,filedir,bins=20):
    files = [f for f in os.listdir(filedir) if os.path.isfile(filedir + os.sep + f) and str(f).startswith("out")]
    redshift_token = 'z'+str(float(np.round(redshift,1))).replace('.','p')
    target_files = [f for f in files if redshift_token in str(f)]

    for f in target_files:
        filepath = filedir + os.sep + f
        # -----
        tokens = str(f).removesuffix(".csv").split('_')
        box_token = tokens[1]
        post_token = tokens[3]
        imf_token = tokens[4]
        sys_token = tokens[5]
        boxsize=float(box_token.removeprefix("L").split("N")[0])
        # -----
        if post_token!="st":continue
        # -----
        table = np.loadtxt(filepath,usecols=(1,5))
        TGID,M_AB = table.T
        TGID=TGID.astype(np.int64)
        log_L,dn_dlogL,error=gs.Utility.LumimosityFunction(M_AB,boxsize/h,bins)
        XLF = log_L
        YLF = dn_dlogL
        ax.plot(XLF,YLF,'-',label=f"{box_token} ({post_token})")