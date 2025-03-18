import galspy as gs
import numpy as np
import matplotlib.pyplot as plt

REDSHIFT = 11
SIM = gs.NavigationRoot(gs.NINJA.L150N2040)
SN = SIM.SnapNumFromRedshift(REDSHIFT)
PIG = SIM.PIG(SN)

pl = gs.Plots(PIG)

# pl.mass_metallicity_scatter()



