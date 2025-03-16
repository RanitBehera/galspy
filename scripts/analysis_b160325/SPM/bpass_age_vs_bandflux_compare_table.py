import matplotlib.pyplot as plt
import numpy as np


tab1 = np.loadtxt("temp/age_flux_Z02.txt")
tab2 = np.loadtxt("temp/age_flux_Z002.txt")

t1a,t1b1,t1b2,t1b3 = tab1.T
t2a,t2b1,t2b2,t2b3 = tab2.T


plt.plot(t1a,t1b1,'r-',label="1450")
plt.plot(t1a,t1b2,'g-',label="2500")
plt.plot(t1a,t1b3,'b-',label="4450")

plt.plot(t2a,t2b1,'r--',label="1450")
plt.plot(t2a,t2b2,'g--',label="2500")
plt.plot(t2a,t2b3,'b--',label="4450")

plt.legend()
plt.show()