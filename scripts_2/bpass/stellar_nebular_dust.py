import numpy as np
import matplotlib.pyplot as plt
import pickle
from galspec.Dust import DustExtinction
from galspy.utility.Figure.Beautification import SetMyStyle
from matplotlib import ticker


SetMyStyle()


Z="0.02"
T="6.0"

WRANGE = [700,6000]

# =============== Stellar
with open("cache/cloudy_chab_300M_solar.in","rb") as fp:
    tspec_stl:dict = pickle.load(fp)
WL_stl = tspec_stl[Z]["WL"]
flux_stl = tspec_stl[Z][T]

mask1 = WL_stl>WRANGE[0]
mask2 = WL_stl<WRANGE[1]
mask = mask1 & mask2

WL_stl = WL_stl[mask]
flux_stl = flux_stl[mask]


# ================= Nebular
with open("cache/cloudy_chab_300M_solar.out","rb") as fp:
    tspec_neb:dict = pickle.load(fp)
WL_neb = tspec_neb[Z]["WL"]
flux_neb= tspec_neb[Z][T]

WL = WL_neb[mask]
flux = flux_stl + flux_neb[mask]

# ================== Dust
de = DustExtinction()
AV=0.5
WL,flux_red = de.get_reddened_spectrum(WL,flux,"Calzetti",AV)



# ================== Plots
L_SOL = 3.846e33 
plt.plot(WL_stl,flux_stl/L_SOL,label=f"Stellar Atmosphere",c="deepskyblue",lw=2)
plt.plot(WL,flux/L_SOL,label="+ Nebular Emission",c="darkorange",lw=2)
plt.plot(WL,flux_red/L_SOL, label=f"+ Dust Reddening",c='indianred',lw=2)


# =========== BEAUTIFICATION
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
text +=f"\n$A_V={AV}$"
plt.annotate(text,xy=(0,1),xytext=(10,-10),ha="left",va="top",xycoords="axes fraction",textcoords="offset pixels")


plt.show()