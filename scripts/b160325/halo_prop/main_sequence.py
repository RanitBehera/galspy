import numpy, galspy
import matplotlib.pyplot as plt

from galspy.MPGadget import _Sim

from galspy.utility.Figure.MainSequence import MainSequenceFigure
from galspy.utility.Figure.Beautification import SetMyStyle
SetMyStyle()



# --- SIMULATIONS
L150N2040   = galspy.NavigationRoot("/mnt/home/student/cranit/NINJA/simulations/L150N2040/SNAPS")
L250N2040   = galspy.NavigationRoot("/mnt/home/student/cranit/NINJA/simulations/L250N2040/SNAPS")


msfig = MainSequenceFigure(1,4)
msfig.Plot([L250N2040,L150N2040],[10,9,8,7])
msfig.Beautify()
plt.show()
