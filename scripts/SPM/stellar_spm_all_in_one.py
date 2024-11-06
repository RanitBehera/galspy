import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

# Prepare Axes
fig = plt.figure(figsize=(6,11))
gs = GridSpec(11,84)
ax_3D   = fig.add_subplot(gs[0:3,0:38])
ax_2D   = fig.add_subplot(gs[0:3,48:84])
ax_den  = fig.add_subplot(gs[3:6,24:60]) 
ax_P1m  = fig.add_subplot(gs[3:4,0:24]) 
ax_P1a  = fig.add_subplot(gs[4:5,0:24]) 
ax_P1z  = fig.add_subplot(gs[5:6,0:24]) 
ax_P2m  = fig.add_subplot(gs[3:4,60:84]) 
ax_P2a  = fig.add_subplot(gs[4:5,60:84]) 
ax_P2z  = fig.add_subplot(gs[5:6,60:84]) 
ax_S1   = fig.add_subplot(gs[6:9,0:42])
ax_S2   = fig.add_subplot(gs[6:9,42:84])
ax_R    = fig.add_subplot(gs[9:11,0:21])
ax_G    = fig.add_subplot(gs[9:11,21:42])
ax_B    = fig.add_subplot(gs[9:11,42:63])
ax_RGB  = fig.add_subplot(gs[9:11,63:84])

def SetSpineColor(ax:plt.Axes,color):
    for side in ['top','right','bottom','left']:
        ax.spines[side].set_color(color)


SetSpineColor(ax_R,'r')
SetSpineColor(ax_G,'g')
SetSpineColor(ax_B,'b')

# ax_R.set_facecolor('r',alpha=0.1)
# ax_R.set_facecolor('g',alpha=0.1)
# ax_R.set_facecolor('b',alpha=0.1)





# BEAUTIFICATION
axes = [ax_3D,ax_2D,ax_den,ax_P1m,ax_P1a,ax_P1z,ax_P2m,ax_P2a,ax_P2z,ax_S1,ax_S2,ax_R,ax_G,ax_B,ax_RGB]
for ax in axes:
    ax:plt.Axes
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)

    








plt.subplots_adjust(wspace=10,hspace=0.5)
plt.show()