import galspy as gs
import numpy as np
import matplotlib.pyplot as plt

REDSHIFT = 7
SIM = gs.NavigationRoot(gs.NINJA.L150N2040)
SN = SIM.SnapNumFromRedshift(REDSHIFT)
PIG = SIM.PIG(SN)

p = gs.Plots(PIG)

p.mass_metallicity_scatter()

