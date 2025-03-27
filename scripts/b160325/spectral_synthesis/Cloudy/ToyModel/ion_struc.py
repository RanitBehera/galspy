import numpy as np
import matplotlib.pyplot as plt
import os

# PATH = "/mnt/home/student/cranit/RANIT/Repo/galspy/study/cloudy/uveffect/Test"
PATH = "/mnt/home/student/cranit/RANIT/Repo/galspy/study/cloudy/bpass_ri"

def DoFor(ax:plt.Axes,fn):
    H=np.loadtxt(PATH+os.sep+fn+".is_H").T
    He=np.loadtxt(PATH+os.sep+fn+".is_He").T
    O=np.loadtxt(PATH+os.sep+fn+".is_O").T

    ax.plot(H[0],H[1],label="H I")
    ax.plot(H[0],H[2],label="H II")
    ax.plot(H[0],H[3],label="H2")

    ax.plot(He[0],He[1],ls='--',label="He I")
    ax.plot(He[0],He[2],ls='--',label="He II")
    ax.plot(He[0],He[3],ls='--',label="He III")


    ax.plot(O[0],O[1],ls='-.',label="O I")
    ax.plot(O[0],O[2],ls='-.',label="O II")
    ax.plot(O[0],O[3],ls='-.',label="O III")

    ax.legend()
    ax.set_xscale('log')



fig,axes = plt.subplots(1,3)
DoFor(axes[0],"r01")
DoFor(axes[1],"r05")
DoFor(axes[2],"r1")

# DoFor(axes[0],"t0")


plt.show()

