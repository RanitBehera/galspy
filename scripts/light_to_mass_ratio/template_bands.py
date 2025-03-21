import numpy as np
import matplotlib.pyplot as plt
from galspy.Spectra.Templates import Templates
from galspy.Spectra.Templates import BPASS

import galspy as gs
gs.SetPlotStyle(14)


LSOL = 3.846e33

tp=Templates()
def PlotFor(imf:BPASS.AVAIL_MODEL_HINT,system="Binary",label=""):
    table = tp.GetStellarTemplates(imf,system)

    # -------------------------------------
    wave,specs = table[0],table[1:]
    specs *= LSOL   # Lsol A-1 to ergs s-1 A-1
    Z_block = 0
    start = 51*Z_block
    end = 51*Z_block+50
    spec_block = specs[start:end]

    # -------------------------------------
    BAND = 1500
    index = np.argmin(np.abs(wave-BAND))
    istart=index-10
    iend=index+10
    band_wave = wave[istart:iend]
    band_block = spec_block[:,istart:iend]

    avg_lum_band = np.mean(band_block,axis=1)
    age = np.arange(6,11.1,0.1)


    sls = {"Binary":"-","Single":"--"}[system]
    slw = {"Binary":1.5,"Single":1}[system]


    plt.plot(age[:41],avg_lum_band[:41]/1e6,label=label,ls=sls,lw=slw)



plt.figure(figsize=(10,8))


PlotFor("KROUPA_UPTO_300M_TOP_HEAVY","Binary","Kroupa300TH")
PlotFor("KROUPA_UPTO_100M_TOP_HEAVY","Binary","Kroupa100TH")
PlotFor("CHABRIER_UPTO_300M","Binary","Chabrier300")
PlotFor("KROUPA_UPTO_300M","Binary","Kroupa300")
PlotFor("CHABRIER_UPTO_100M","Binary","Chabrier100")
PlotFor("KROUPA_UPTO_100M","Binary","Kroupa100")
PlotFor("SALPETER_UPTO_100M","Binary","Salpeter100")
PlotFor("KROUPA_UPTO_300M_BOTTOM_HEAVY","Binary","Kroupa300BH")
PlotFor("KROUPA_UPTO_100M_BOTTOM_HEAVY","Binary","Kroupa100BH")

# plt.gca().set_prop_cycle(None)








plt.yscale("log")
plt.xlabel("Log Age (Yr)")
plt.ylabel("$L_{\lambda}/M_\odot$ (erg s$^{-1}$ $\AA^{-1}$ $M_\odot^{-1}$)")
plt.subplots_adjust(left=0.15)
plt.title("Light-to-Mass ratio in BPASS")
plt.grid(alpha=0.3)
plt.xlim(6,10)
plt.ylim(1e28,1e35)
plt.legend(ncols=1,frameon=False,markerfirst=False)
plt.show()
