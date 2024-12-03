import numpy as np
import matplotlib.pyplot as plt
import pickle
from galspec.Dust import DustExtinction
from galspy.utility.Figure.Beautification import SetMyStyle
from matplotlib import ticker
from galspec.bpass import BPASS

SetMyStyle()






WRANGE = [700,6000]
L_SOL = 3.846e33 
Z="0.02"
T="6.0"


# ================== BPASS Direct
_BPASS = BPASS("CHABRIER_UPTO_300M","Binary",0.02)
table=_BPASS.Spectra.GetFlux().to_numpy()
lam,aged_flux = table[:,0],table[:,1:].T
first = aged_flux[0]
plt.plot(lam,first,label=f"Stellar Atmosphere",c="red",lw=2)


_BPASS = BPASS("KROUPA_UPTO_300M","Binary",0.02)
table=_BPASS.Spectra.GetFlux().to_numpy()
lam,aged_flux = table[:,0],table[:,1:].T
first = aged_flux[0]
plt.plot(lam,first,label=f"Stellar Atmosphere",c="pink",lw=2)

_BPASS = BPASS("KROUPA_UPTO_300M_TOP_HEAVY","Binary",0.02)
table=_BPASS.Spectra.GetFlux().to_numpy()
lam,aged_flux = table[:,0],table[:,1:].T
first = aged_flux[0]
plt.plot(lam,first,label=f"Stellar Atmosphere",c="blue",lw=2)

_BPASS = BPASS("KROUPA_UPTO_300M_BOTTOM_HEAVY","Binary",0.02)
table=_BPASS.Spectra.GetFlux().to_numpy()
lam,aged_flux = table[:,0],table[:,1:].T
first = aged_flux[0]
plt.plot(lam,first,label=f"Stellar Atmosphere",c="orange",lw=2)









# =================== Check BPASS Cache
if False:
    with open("cache/bpass_chab_300M.ch","rb") as fp:
        tspec_stl:dict = pickle.load(fp)
    WL_stl1 = tspec_stl[Z]["WL"]
    flux_stl1 = tspec_stl[Z][T]
    plt.plot(WL_stl1,flux_stl1,label=f"Stellar Atmosphere",c="blue",lw=2)


    print(len(flux_stl1))




# =============== BPASS from Cloudy Feedback
if False:
    with open("cache/cloudy_chab_300M_solar.in","rb") as fp:
        tspec_stl:dict = pickle.load(fp)
    WL_stl2 = tspec_stl[Z]["WL"]
    flux_stl2 = tspec_stl[Z][T]
    # plt.plot(WL_stl2,flux_stl2/L_SOL,label=f"Stellar Atmosphere",c="deepskyblue",lw=2)

    print(len(flux_stl2))




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