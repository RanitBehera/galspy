import numpy as np
import matplotlib.pyplot as plt
import pickle

with open("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/region_extract/data_kanish/GID_827/dens_gas_827.dat","rb") as fp:
    rho = pickle.load(fp)

with open("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/region_extract/data_kanish/GID_827/ie_gas_827.dat","rb") as fp:
    ie = pickle.load(fp)


ie*=1e-10
gamma=5/3
X=0.75
Y=1-X
Ne=1
mu=1/(X + (Y/4) + (Ne*X))
m_P=1.67e-24
k_B=1.38e-16
T = ie*(gamma-1)*mu*m_P/k_B


plt.plot(rho,T,'.',ms=2)
plt.xscale("log")
plt.yscale("log")

plt.show()