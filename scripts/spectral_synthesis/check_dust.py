import numpy as np
import matplotlib.pyplot as plt
from galspec.Dust import DustExtinction
import pickle


de = DustExtinction()

with open("cache/bpass_chab_300M.in","rb") as fp:
    tspec:dict = pickle.load(fp)
WL = tspec["0.02"]["WL"][700:30000]
flux = tspec["0.02"]["8.0"][700:30000]

fig = plt.figure()


# ============================
# Al4=de.get_kappa(WL,"Calzetti")
# plt.plot(WL,Al4,label="Calzetti")

# # Calzetti lam vs kappa(lam)
# x = [952.6807029019818, 1060.630006754609, 1205.5993565580898, 1379.906384600052, 2654.9732539157512, 8180.539667637443]
# y = [15, 13.781163434903046, 12.03601108033241, 10.90027700831025, 7.548476454293629, 2.479224376731302]
# plt.plot(x,y)


# ============================
plt.plot(WL,flux)
WL,rflux = de.get_reddened_spectrum(WL,flux,"Calzetti",1)
plt.plot(WL,rflux)
plt.yscale("log")
plt.xscale('log')

# ============================
plt.show()

