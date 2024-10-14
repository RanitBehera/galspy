from galspec.Dust import DustExtinction
import numpy as np
import matplotlib.pyplot as plt
import pickle

de = DustExtinction()

with open("cache/bpass.ch","rb") as fp:
    tspec:dict = pickle.load(fp)
WL = tspec["0.02"]["WL"][700:10000]
flux = tspec["0.02"]["8.0"][700:10000]







fig = plt.figure()
x1,al_b_AV1 = de.ALam_b_AV(WL,"MW",5,3)
plt.plot(x1,al_b_AV1)









fig2 = plt.figure()
tau_lam1 = de.GetOpticalDepth(WL,"MW",5,1)
plt.plot(WL,flux)
plt.plot(WL,flux*np.exp(-tau_lam1))

# plt.plot(WL,np.exp(-tau_lam2),'--')


plt.axvline(5500)
plt.yscale("log")
# plt.legend()
# plt.axvline(1/(2700*1e-10/1e-6))
# plt.axvline(1/(5500*1e-10/1e-6),ls='--')
plt.show()
