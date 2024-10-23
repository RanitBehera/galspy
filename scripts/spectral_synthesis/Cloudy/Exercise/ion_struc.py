import numpy as np
import matplotlib.pyplot as plt
import os

PATH = "/mnt/home/student/cranit/RANIT/Repo/galspy/study/cloudy/uveffect/Test"

H=np.loadtxt(PATH+os.sep+"t0.is_H").T
He=np.loadtxt(PATH+os.sep+"t0.is_He").T
O=np.loadtxt(PATH+os.sep+"t0.is_O").T

# plt.plot(H[0],H[1],label="H I")
# plt.plot(H[0],H[2],label="H II")
# plt.plot(H[0],H[3],label="H2")

# plt.plot(He[0],He[1],ls='--',label="He I")
# plt.plot(He[0],He[2],ls='--',label="He II")
# plt.plot(He[0],He[3],ls='--',label="He III")


plt.plot(O[0],O[1],ls='-.',label="O I")
plt.plot(O[0],O[2],ls='-.',label="O II")
plt.plot(O[0],O[3],ls='-.',label="O III")


plt.legend()

# plt.xscale('log')
# plt.yscale('log')

plt.show()

