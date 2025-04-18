import galspy as gs
import matplotlib.pyplot as plt

PIG = gs.NavigationRoot(gs.NINJA.L150N2040).PIG(z=7)

TGID = 3

gid = PIG.Gas.GroupID()
mask = gid==TGID
rho = PIG.Gas.Density()[mask]
ie = PIG.Gas.InternalEnergy()[mask]
nebynh = PIG.Gas.ElectronAbundance()[mask]

rho,temp,temp1=PIG.Gas.GetDensityAndTemperature(rho,ie,nebynh,PIG.Header.Units)
plt.figure()
plt.hist(temp,bins=100)
plt.figure()
plt.hist(temp1,bins=100)
# plt.xscale("log")

plt.figure()
dT = temp-temp1
plt.hist(dT,bins=100)
plt.show()

