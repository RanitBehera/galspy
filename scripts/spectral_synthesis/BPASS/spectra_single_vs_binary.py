import galspec as gs
import matplotlib.pyplot as plt


# PARAMETERS
Z = 0.001           # Metallicity :  0.00001,0.0001,0.001,0.002,0.003,0.004,0.006,0.008,0.010,0.020,0.030,0.040
lam = [100,9000]    # Wavelength Limits : 1 Angstrom <-> 100,000 Angstrom
Age = 8.0             # Log Age of population : 6 to 11 in steps of 0.1 


# -----
sin = gs.BPASS("KROUPA_UPTO_300M","Single",Z)
bin = gs.BPASS("KROUPA_UPTO_300M","Binary",Z)
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