# %%
import numpy as np
import matplotlib.pyplot as plt
import galspy.IO.BigFile as bf
import os

path = "/mnt/home/student/cranit/runsim/MP-Gadget/examples/cooling_metal_UVB"


def ReadField(name):
    field = bf.Column(path + os.sep + name).Read()
    return field



N_HydrogenNumberDensity = ReadField("N_HydrogenNumberDensity")
N_MetallicityInSolar = ReadField("N_MetallicityInSolar")
N_Redshift = ReadField("N_Redshift")
N_Temperature = ReadField("N_Temperature")
HydrogenNumberDensity_bins = ReadField("HydrogenNumberDensity_bins")
MetallicityInSolar_bins = ReadField("MetallicityInSolar_bins")
Redshift_bins = ReadField("Redshift_bins")
Temperature_bins = ReadField("Temperature_bins")
NetCoolingRate = ReadField("NetCoolingRate")


# plt.plot(N_Redshift,N_HydrogenNumberDensity)

# print(N_HydrogenNumberDensity)
# print(MetallicityInSolar_bins)
print(N_MetallicityInSolar)
# print(N_Redshift)
# print(N_Temperature)


# %%
