import galspy
import matplotlib.pyplot as plt
import numpy as np
from galspy.utility.Figure.MassFunction import StellarMassFunctionEvolutionFigure


# Add Stellar Mass Function
L150N2040 = galspy.NavigationRoot("/mnt/home/student/cranit/NINJA/simulations/L150N2040/SNAPS")
L250N2040 = galspy.NavigationRoot("/mnt/home/student/cranit/NINJA/simulations/L250N2040/SNAPS")
REDS = [10,9,8,7]

smf = StellarMassFunctionEvolutionFigure([L150N2040,L250N2040],REDS,1,4)

smf.Plot()

smf.Beautify(["L150N2040","L250N2040"])
# plt.show()

