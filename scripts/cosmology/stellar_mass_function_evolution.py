# %% 
import galspy
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import numpy as np
from galspy.utility.MassFunction import MassFunction
from galspy.utility.Figure.MassFunction import MassFunctionFigure

# Setup Grids
fig = plt.figure(figsize=(12,8))
gs = GridSpec(2,3)

ax00=fig.add_subplot(gs[0,0])
ax01=fig.add_subplot(gs[0,1])
ax02=fig.add_subplot(gs[0,2])
ax10=fig.add_subplot(gs[1,0])
ax11=fig.add_subplot(gs[1,1])
ax12=fig.add_subplot(gs[1,2])

axs=[ax00,ax01,ax02,ax10,ax11,ax12]


# Add Stellar Mass Function
L150N2040 = galspy.NavigationRoot("/mnt/home/student/cranit/NINJA/simulations/L150N2040/SNAPS")
L250N2040 = galspy.NavigationRoot("/mnt/home/student/cranit/NINJA/simulations/L250N2040/SNAPS")

axs=[ax00,ax01,ax02,ax10,ax11]
REDS = [12,11,10,9,8]


for ax,red in zip(axs,REDS):
    mffig = MassFunctionFigure(ax)
    sn  = L150N2040.SnapNumFromZ(red)
    PIG = L150N2040.PIG(sn)
    mffig.AddPIG_MF(PIG,star=True,color='m',label="L150N2040")
    sn  = L250N2040.SnapNumFromZ(red)
    PIG = L250N2040.PIG(sn)
    mffig.AddPIG_MF(PIG,star=True,color='c',label="L250N2040")

    mffig.BeautifyPlot()

# Beautify
for ax in axs:
    ax.tick_params(axis='both', direction='in')
    ax.grid(False)

for ax in [ax01,ax02,ax11,ax12]:
    ax.yaxis.set_ticklabels([])
    ax.set_ylabel("")

for ax in [ax00,ax01,ax02]:
    ax.xaxis.set_ticklabels([])
    ax.set_xlabel("")


plt.subplots_adjust(wspace=0.05,hspace=0.05)
plt.show()

# %%
