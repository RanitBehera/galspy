import galspy as gs
import matplotlib.pyplot as plt

SIM = gs.NavigationRoot(gs.NINJA.L150N2040)
PIG = SIM.PIG(z=7)

NHI = PIG.Gas.NeutralHydrogenFraction()
GID = PIG.Gas.GroupID()

TGID = 2

tmask = GID==TGID
TNHI = NHI[tmask]



plt.hist(TNHI,bins=100)
plt.yscale("log")

plt.xlabel("Neutral Hydrogen Fraction")
plt.ylabel("Bin Count")

plt.show()

