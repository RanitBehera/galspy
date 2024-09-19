import galspy
import matplotlib.pyplot as plt
from scipy import spatial
import numpy as np

root=galspy.NavigationRoot("/mnt/home/student/cranit/NINJA/simulations/L150N2040/SNAPS")


gm = root.PART(11).Header.MassTable()[0]
mass = root.PART(11).Star.Mass()/gm

ms = np.sort(mass)

plt.hist(ms,bins=np.linspace(0.1,0.4,100))
# plt.yscale('log')
plt.show()
