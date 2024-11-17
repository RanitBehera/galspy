import pickle

import numpy

import matplotlib.pyplot as plt

with open("/mnt/home/student/cranit/RANIT/Repo/galspy/cache/bpass_chab_300M.ch","rb") as fp:
    file = pickle.load(fp)

with open("/mnt/home/student/cranit/RANIT/Repo/galspy/cache/cloudy_chab_300M.in","rb") as fp:
    filein = pickle.load(fp)

with open("/mnt/home/student/cranit/RANIT/Repo/galspy/cache/cloudy_chab_300M.out","rb") as fp:
    fileout = pickle.load(fp)


Z="0.00001"

sl1 = file[Z]
sl2 = filein[Z]
sl3 = fileout[Z]

T="6.0"

plt.plot(sl1["WL"],sl1[T]*(3.846e33),label="bpass")
print(len(sl1["WL"]))

plt.plot(sl2["WL"],sl2[T],label="cin")
print(len(sl2["WL"]))

plt.plot(sl3["WL"],sl3[T],label="cout")

plt.plot(sl2["WL"],sl2[T]+sl3[T],label="ctot")


plt.xscale("log")
plt.yscale("log")
plt.legend()
plt.show()