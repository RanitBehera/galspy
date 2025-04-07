import galspy as gs
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import KDTree


SIM = gs.NavigationRoot(gs.NINJA.L150N2040)
PIG = SIM.PIG(z=7)
UNITS=PIG.Header.Units


print("Target Box ".ljust(32,"="))
PIG.print_box_info()

cstar_loc = PIG.GetCentralStarPosition()