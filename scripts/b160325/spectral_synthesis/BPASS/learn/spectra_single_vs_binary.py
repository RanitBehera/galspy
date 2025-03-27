import galspec as gs
import matplotlib.pyplot as plt


# PARAMETERS
Z = 0.001
lam = [100,9000]
Age = 8.0


# -----
sin = gs.BPASS("KROUPA_UPTO_300M","Single",Z)
bin = gs.BPASS("KROUPA_UPTO_300M","Binary",Z)
# -----
fsin=sin.Spectra.GetFlux(lam[0],lam[-1])
fbin=bin.Spectra.GetFlux(lam[0],lam[-1])
plt.plot(fsin.WL,fsin[str(Age)],label="Single")
plt.plot(fbin.WL,fbin[str(Age)],label="Binary")
plt.xlabel("Wavelength ($\AA$)")
plt.ylabel("Flux")
plt.legend(title=f"Z={Z}")
plt.yscale('log')
plt.xscale('log')
plt.show()