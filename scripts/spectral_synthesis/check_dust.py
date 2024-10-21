import numpy as np
import matplotlib.pyplot as plt
from galspec.Dust import DustExtinction
import pickle


de = DustExtinction()

with open("cache/bpass_chab_300M.ch","rb") as fp:
    tspec:dict = pickle.load(fp)
WL = tspec["0.02"]["WL"][700:10000]
flux = tspec["0.02"]["8.0"][700:10000]

fig = plt.figure()

if True:
    Al1=de.ALam(WL,"MW",5,3.1)
    Al2=de.ALam(WL,"LMC",5,3.1)
    Al3=de.ALam(WL,"SMC_BAR",5,3.1)
    Al4=de.ALam(WL,"Calzetti",5,3.1)
    # plt.plot(1e4/WL,Al1/5,label="MW")
    # plt.plot(1e4/WL,Al2/5,label="LMC")
    # plt.plot(1e4/WL,Al3/5,label="SMC_BAR")
    plt.plot(WL,Al1,label="MW")
    plt.plot(WL,Al2,label="LMC")
    plt.plot(WL,Al3,label="SMC_BAR")
    plt.plot(WL,Al4,label="Calzetti")


if False:
    tau_lam = de.GetOpticalDepth(WL,"MW",5,1)
    plt.plot(WL,flux)
    plt.plot(WL,flux*np.exp(-tau_lam))
    plt.plot(WL,np.exp(-tau_lam2),'--')
    plt.yscale("log")


# plt.axvline(5500)
# plt.legend()
# plt.axvline(1/(2700*1e-10/1e-6))
# plt.axvline(1/(5500*1e-10/1e-6),ls='--')
plt.legend()
plt.show()
