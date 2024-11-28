
import numpy as np
import matplotlib.pyplot as plt

GID,GMDM,GMST,GMBH,NST,NBH,bh_acc,Mdot_edd,L_edd = np.loadtxt("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts_2/galaxy_statistics/data/table1.txt").T
GID_s,MAB_ST_s,MAB_ST_RED_s,MAB_TOT_s,MAB_TOT_RED_s,beta_ST_s,beta_ST_RED_s,beta_TOT_s,beta_TOT_RED_s = np.loadtxt("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts_2/galaxy_statistics/data/table2_solar.txt").T
GID_p,MAB_ST_p,MAB_ST_RED_p,MAB_TOT_p,MAB_TOT_RED_p,beta_ST_p,beta_ST_RED_p,beta_TOT_p,beta_TOT_RED_p = np.loadtxt("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts_2/galaxy_statistics/data/table2_primordial.txt").T

MAB_ks = np.loadtxt("/mnt/home/student/cranit/RANIT/Repo/galspy/study/LuvAB/MUVAB_SFR.txt")

# Luminosity functions
from galspec.Utility import LuminosityFunction
plt.figure()
#
h=0.6736
M,phi,err = LuminosityFunction(MAB_ks,(150/h)**3,0.5)
mask=(M< -18)&(M> -27)&(phi>1e-9)
M,phi,err=M[mask],phi[mask],err[mask]
plt.plot(M,phi,label="MD")
#
M,phi,err = LuminosityFunction(MAB_ST_s,(150/h)**3,0.5)
mask=(M< -18)&(M> -27)&(phi>1e-9)
M,phi,err=M[mask],phi[mask],err[mask]
plt.plot(M,phi,label="Stellar (solar)")

M,phi,err = LuminosityFunction(MAB_TOT_s,(150/h)**3,0.5)
mask=(M< -18)&(M> -27)&(phi>1e-9)
M,phi,err=M[mask],phi[mask],err[mask]
plt.plot(M,phi,label="+ Nebular (solar)")

M,phi,err = LuminosityFunction(MAB_TOT_p,(150/h)**3,0.5)
mask=(M< -18)&(M> -27)&(phi>1e-9)
M,phi,err=M[mask],phi[mask],err[mask]
plt.plot(M,phi,label="+ Nebular (primorial)")

M,phi,err = LuminosityFunction(MAB_TOT_RED_p,(150/h)**3,0.5)
mask=(M< -18)&(M> -27)&(phi>1e-9)
M,phi,err=M[mask],phi[mask],err[mask]
plt.plot(M,phi,label="+ Reddened (primorial)")




# Observational
obs = np.genfromtxt("/mnt/home/student/cranit/RANIT/Repo/galspy/obs/uvlf/uvlf.txt",dtype=None,encoding='utf-8')
obs = np.array([list(row) for row in obs],dtype=object)

MAB = obs[:,3]
phi_exp = obs[:,9]
phi = obs[:,6] * (10.**phi_exp)
phi_p = obs[:,7] * (10.**phi_exp)
phi_n = -obs[:,8] * (10.**phi_exp)

plt.errorbar(MAB,phi,(phi_n,phi_p),fmt='.',capsize=4)


# Beta function
# plt.plot(GMST[:33179],beta_ST_p,'.',label="Stellar")
# plt.plot(GMST[:33179],beta_TOT_p,'.',label="Tottal")

# ===
# edd_rat = bh_acc / Mdot_edd
# edd_rat = edd_rat[:33179]
# mask = edd_rat>0.01

# # plt.plot(GMST,edd_rat,'.')

# plt.plot(GMST[:33179],MAB_TOT_p,'.',c='g')
# plt.plot(GMST[:33179][mask],MAB_TOT_p[mask],'.',c='r',ms=10)




# plt.axhline(-2.4)
plt.legend()
# plt.xscale("log")
plt.yscale("log")
plt.show()

