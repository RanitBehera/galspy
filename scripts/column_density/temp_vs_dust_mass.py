import galspy as gs
import matplotlib.pyplot as plt
import numpy as np


PIG = gs.NavigationRoot(gs.NINJA.L150N2040).PIG(z=7)
TGID = 3


dens = PIG.Gas.Density()
elec_abun = PIG.Gas.ElectronAbundance()
ie = PIG.Gas.InternalEnergy()
mass = PIG.Gas.Mass()
met = PIG.Gas.Metallicity()
delay = PIG.Gas.DelayTime()
pot = PIG.Gas.Potential()
sfr = PIG.Gas.StarFormationRate()
nhfrac = PIG.Gas.NeutralHydrogenFraction()

BS,BE = PIG.GetParticleBlockIndex(gs.GAS)

tdens = dens[BS[TGID]:BE[TGID]]
telec_abun = elec_abun[BS[TGID]:BE[TGID]]
tie = ie[BS[TGID]:BE[TGID]]
tmass = mass[BS[TGID]:BE[TGID]]
tmet = met[BS[TGID]:BE[TGID]]
tpot = pot[BS[TGID]:BE[TGID]]
tsfr = sfr[BS[TGID]:BE[TGID]]
tdelay = delay[BS[TGID]:BE[TGID]]
tnhfrac = nhfrac[BS[TGID]:BE[TGID]]

met_mass = tmass*tmet*1e10

# ----------
ps_dens,ps_temp = PIG.Gas.GetDensityAndTemperature(tdens,tie,telec_abun,PIG.Header.Units)
ps_ndens = ps_dens/1.67e-27
# ----------

plt.figure(figsize=(6,6))
plt.scatter(ps_ndens,ps_temp,2,np.log10(tnhfrac),cmap="cool")

# mask = tdelay>0
# plt.scatter(ps_ndens[~mask],ps_temp[~mask],2,'c')
# plt.scatter(ps_ndens[mask],ps_temp[mask],6,'m')


plt.xscale("log")
plt.yscale("log")
plt.xlabel("Hydrogen Number Density (cm$^{-3}$)")
plt.ylabel("Temperature (K)")
plt.colorbar(location="top",orientation="horizontal",label="log$_{10}$(x$_{HI}$)",fraction=0.05,aspect=40)
plt.subplots_adjust(bottom=0.15,left=0.15)
plt.show()