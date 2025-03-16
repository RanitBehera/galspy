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
mass = GetPickle("scripts/gas_density_profile/cache/mass_gas_1.dat")
metallicity = GetPickle("scripts/gas_density_profile/cache/metallicity_gas_1.dat")


# plt.xscale("log")
plt.yscale("log")
plt.hist(np.log10(metallicity[metallicity>1e-20]),bins=100)
plt.show()