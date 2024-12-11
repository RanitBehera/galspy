import numpy as np
import pickle
import matplotlib.pyplot as plt
import time

def GetPickle(filepath):
    with open(filepath,"rb") as fp:
        data = pickle.load(fp)
    return data

pos = GetPickle("scripts/gas_density_profile/cache/pos_gas_1.dat")
vel = GetPickle("scripts/gas_density_profile/cache/vel_gas_1.dat")
mass = GetPickle("scripts/gas_density_profile/cache/mass_gas_1.dat")*1e10
metallicity = GetPickle("scripts/gas_density_profile/cache/metallicity_gas_1.dat")

metallicity = metallicity*mass

# Recenter
if True:
    CX,CY,CZ=131462.60496180426,15102.526179407781,91828.29217856088
    Center = np.column_stack((CX,CY,CZ))
    pos = pos-Center


# Get Radius and bin
rad = np.linalg.norm(pos,axis=1)
delta_rad = 1.
bin_indices=np.int32(rad/delta_rad)
num_bins = np.max(bin_indices) + 1


# Brute force python for loop
# bin_mass2[bin_indices[i]]+=mass[i]
# Checked bruteforce gives same as following numpy method
# Numpy advanced binning add - 7 times faster than brute force add
bin_mass = np.zeros(num_bins)
bin_metallicity = np.zeros(num_bins)
np.add.at(bin_mass,bin_indices,mass)
np.add.at(bin_metallicity,bin_indices,metallicity)

bin_rad = delta_rad*np.arange(num_bins)
bin_volume = 4*np.pi*(bin_rad**2)*delta_rad
bin_dens = bin_mass/bin_volume
bin_dens *= 0.75*2e33/((3e21)**3) 
bin_dens /=1.67e-24

# https://ned.ipac.caltech.edu/level5/Madau6/Madau1_1.html
n_igm = (1.6e-7)*((1/6)/0.019)#*((1+7)**3)



bin_met_dens = bin_metallicity/bin_volume
bin_met_dens *=2e33/((3e21)**3)

# divide by number of particle or mass of particles

# plot
fig,ax=plt.subplots(2,1)
ax:list[plt.Axes]

ax[0].plot(bin_rad,bin_dens)
ax[0].set_yscale('log')
ax[0].set_xscale('log')
ax[0].set_xlabel("ckpc/h")
# ax[0].set_ylabel("$(M_\odot/h)  (ckpc/h)^{-3}$")
# ax[0].set_ylabel("$(gm/h)  (cm/h)^{-3}$")
ax[0].axvline(2000)
ax[0].axhline(n_igm,color='k',lw=1,ls='--')

ax[1].plot(bin_rad,bin_met_dens)
ax[1].set_yscale('log')
ax[1].set_xscale('log')
ax[1].set_xlabel("ckpc/h")
# ax[1].set_ylabel("$(gm/h)  (cm/h)^{-3}$")
# ax[1].axhline(0.02)
ax[1].axvline(2000)

# ===============================

# table = []
# for i in range(num_bins):table.append([])
# table:list[list]

# for j in range(len(bin_indices)):
#     table[bin_indices[j]].append(metallicity[j])

# mean=[]
# sigma=[]
# # print(table)
# for row in table:
#     numrow=np.array(row)
#     rmean=np.mean(numrow)
#     rsigma = np.std(numrow)
#     mean.append(rmean)
#     sigma.append(rsigma)

# mean = np.array(mean)
# sigma = np.array(sigma)
# bin_rad = delta_rad*np.arange(num_bins)
# bin_volume = 4*np.pi*(bin_rad**2)*delta_rad
# mean = mean/bin_volume
# sigma = sigma/bin_volume


# # plot
# plt.plot(bin_rad,np.log10(mean))
# plt.fill_between(bin_rad,np.log10(mean)+np.log10(sigma),np.log10(mean)-np.log10(sigma),color='k',alpha=0.1,ec=None)
# plt.xscale('log')
# # plt.yscale('log')
# plt.axvline(2000,color='k',ls='--')
# plt.axhline(np.log10(0.02),color='k',ls='--')




plt.show()
