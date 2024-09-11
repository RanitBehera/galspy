import numpy as np
import matplotlib.pyplot as plt

primary_snaps=[90,50,20]+list(np.arange(15,-0.1,-0.5))
secondary_snaps = np.logspace(0,1,40)


fig,axs = plt.subplots(2,1)


for z in primary_snaps:
    axs[0].plot(z,0,'.',ms=10,color='blue')
    axs[1].plot(z,0,'.',ms=10,color='blue')

for z in secondary_snaps:
    axs[0].plot(z,0,'.',ms=5,color='red')
    axs[1].plot(z,0,'.',ms=5,color='red')

axs[1].set_xscale('log')
axs[0].xaxis.tick_top()

axs[0].set_ylabel("Linear",fontsize=16)
axs[1].set_ylabel("Logarithimic",fontsize=16)


xticks = [1,5,10,15,20,25]
for ax in axs:
    ax.set_xticks(xticks)
    ax.set_xticklabels([str(xt) for xt in xticks]) 
    ax.set_xlim(1,25)
    ax.set_ylim(-0.5,0.5)
    ax.set_yticks([])
    ax.grid()

plt.show()