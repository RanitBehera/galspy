import numpy as np
import matplotlib.pyplot as plt
import pickle
from galspec.Dust import DustExtinction
from galspy.utility.Figure.Beautification import SetMyStyle
from matplotlib import ticker
from galspec.bpass import BPASS

SetMyStyle()


Z="0.02"
T="6.0"

WRANGE = [700,6000]
L_SOL = 3.846e33 

# =============== Stellar
with open("cache/cloudy_chab_300M_solar.in","rb") as fp:
    tspec_stl:dict = pickle.load(fp)
WL_stl = tspec_stl[Z]["WL"]
flux_stl = tspec_stl[Z][T]
plt.plot(WL_stl,flux_stl/L_SOL,label=f"Stellar Atmosphere",c="deepskyblue",lw=2)



with open("bpass_chab_300M.ch","rb") as fp:
    tspec_stl:dict = pickle.load(fp)
WL_stl = tspec_stl[Z]["WL"]
flux_stl = tspec_stl[Z][T]
plt.plot(WL_stl,flux_stl/L_SOL,label=f"Stellar Atmosphere",c="deepskyblue",lw=2)






plt.xscale("log")
plt.yscale("log")

plt.gca().xaxis.set_major_formatter(ticker.ScalarFormatter())
plt.gca().xaxis.set_minor_formatter(ticker.NullFormatter())

ticks = [912,1215,2175,3646,4400,5500]
plt.xticks(ticks,labels=[str(v) for v in ticks])
plt.xlim(700,6000)
plt.ylim(0.9e3,1.1e9)
plt.tick_params(axis='both',which='minor',bottom=False,left=False)
plt.xlabel("Wavelength $(\\AA)$")
plt.ylabel("Spectral Luminosity $(L_\odot/\\AA)$")
plt.legend(markerfirst=False,frameon=False)
# plt.grid(alpha=0.3)

text =f"$M_c=10^6 M_\odot$"
text +=f"\n$Z={Z}$"
text +=f"\n$T = {round(10**float(T)/1e6,1)}$ Myr"
plt.annotate(text,xy=(0,1),xytext=(10,-10),ha="left",va="top",xycoords="axes fraction",textcoords="offset pixels")


plt.show()