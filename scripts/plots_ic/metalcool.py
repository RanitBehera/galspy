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


# Plot between NetCoolingRate vs Temperature_bins
# However length mismatch 520200 vs 200, factor of 2601
# Then length of HydrogenNumberDesnity_bin and Redshift_bins are 51 and 51.
# and 51x51=2601, so chnage shape to (51,51,200)
# First dimension is redshift
# Second dimension is HydrogneDensity

print(Redshift_bins)
print(HydrogenNumberDensity_bins)

NetCoolingRate=NetCoolingRate.reshape((51,51,200))
NetCoolingRate=np.log10(NetCoolingRate)

for i in range(51):
    plt.plot(Temperature_bins,NetCoolingRate[50,20],'r')
    plt.plot(Temperature_bins,NetCoolingRate[50,50],'b')
    plt.plot(Temperature_bins,NetCoolingRate[0,20],'r--')
    plt.plot(Temperature_bins,NetCoolingRate[0,50],'b--')
    # plt.plot(Temperature_bins,NetCoolingRate[i,49])
    # plt.plot(Temperature_bins,NetCoolingRate[i,20])

plt.xlabel("log T")
plt.ylabel("Cooling Rate")
plt.show()




