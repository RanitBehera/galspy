import numpy as np
from galspy.utility.MassFunction import MassFunction
import matplotlib.pyplot as plt


table = np.loadtxt("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/get_centers/data/subinfo.txt")
gid,nsubs,subid,nstar_group,nstar_sub,st_mass_fof,st_mass_sum,st_mass_sub=table.T

st_mass_fof *=(1e10 /0.6736)  # M_solar
st_mass_sum *=(1e10 /0.6736)  # M_solar
st_mass_sub *=(1e10 /0.6736)  # M_solar

box_size = (150000/0.6736)/1000    #Mpc

M,phi,err = MassFunction(st_mass_fof,box_size) 
plt.plot(M/2,phi,label="FOF")
ints=np.sum(M[:-1]*phi[:-1]*np.diff(M))
print(np.log10(ints))
M,phi,err = MassFunction(st_mass_sub,box_size) 

plt.plot(M,phi,label="Sub")
ints=np.sum(M[:-1]*phi[:-1]*np.diff(M))
print(np.log10(ints))


plt.xscale("log")
plt.yscale("log")
plt.legend()
plt.show()