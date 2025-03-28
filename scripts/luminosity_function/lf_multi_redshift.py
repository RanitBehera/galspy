import matplotlib.pyplot as plt
import numpy as np
import galspy as gs
from matplotlib.gridspec import GridSpec
from load_observation import load_obs_to_axis


# Initialise Figure
gs.SetPlotStyle()
fig = plt.figure(figsize=(12,8))
gs = GridSpec(2,2,figure=fig)
ax00 = fig.add_subplot(gs[0,0])
ax01 = fig.add_subplot(gs[0,1])
ax10 = fig.add_subplot(gs[1,0])
ax11 = fig.add_subplot(gs[1,1])



for ax in [ax00,ax01,ax10,ax11]:
    ax.legend()
    ax.set_yscale("log")














plt.show()
