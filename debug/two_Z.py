import numpy as np
import matplotlib.pyplot as plt


X1,Y1 = np.loadtxt("temp/age_flux.txt").T
X2,Y2 = np.loadtxt("temp/age_flux_Z002.txt").T

plt.plot(X1,Y1,label="Z=0.02")
plt.plot(X2,Y2,label="Z=0.002")
plt.legend()
plt.xlabel("Log10 Age")
plt.ylabel("Log10 Flux")
plt.show()