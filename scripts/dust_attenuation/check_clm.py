import numpy as np
import galspy as gs

SIM = gs.NavigationRoot(gs.NINJA.L150N2040)
REDSHIFT=7
SNAP = SIM.PART(SIM.SnapNumFromRedshift(REDSHIFT))
print("hi")



gas_pos = SNAP.Gas.Position()
gas_mass = SNAP.Gas.Mass()



input("Done=")







