
import numpy as np
import matplotlib.pyplot as plt


path = "/mnt/home/student/cranit/runsim/MP-Gadget/examples/TREECOOL_fg_june11"
data = np.loadtxt(path)

z = np.power(10,data[:,0]) - 1

# Photo-Ionisation Rate in s^-1
Gamma_HI    = data[:,1]
Gamma_HeI   = data[:,2]
Gamma_HeII  = data[:,3]

# Photo-Heating Rate in erg s^-1
Qdot_HI     = data[:,4]
Qdot_HeI    = data[:,5]
Qdot_HeII   = data[:,6]

fig,axs = plt.subplots(2,1,sharex=True)

axs[0].plot(z,Gamma_HI,label = "$\Gamma_{HI}$")
axs[0].plot(z,Gamma_HeI,label = "$\Gamma_{HeI}$")
axs[0].plot(z,Gamma_HeII,label = "$\Gamma_{HeII}$")
axs[1].plot(z,Qdot_HI,label = "$\dot{Q}_{HI}$")
axs[1].plot(z,Qdot_HeI,label = "$\dot{Q}_{HeI}$")
axs[1].plot(z,Qdot_HeII,label = "$\dot{Q}_{HeII}$")

for ax in axs:
    ax.set_yscale("log")
    ax.legend(ncol=3)

axs[-1].set_xlabel("Redshift")
axs[0].set_ylabel("PhotoIonisation Rate\nin s$^{-1}$")
axs[1].set_ylabel("Heating Rate\nin ergs s$^{-1}$")

plt.show()
