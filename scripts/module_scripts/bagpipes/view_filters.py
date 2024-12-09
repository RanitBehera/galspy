import numpy as np
import matplotlib.pyplot as plt
import os
from matplotlib import colors
from matplotlib.collections import PolyCollection

from galspy.utility.Figure.Beautification import gradient_fill


FILTER_DIR = "/mnt/home/student/cranit/RANIT/Repo/galspy/scripts_2/bagpipes/filters/jwst"

filters = [f for f in os.listdir(FILTER_DIR)
         if os.path.isfile(os.path.join(FILTER_DIR,f)) and
         not f.startswith('.') and
         f[0] in ['F','W'] and
         f.endswith(('M'))]


hues = np.linspace(0, 1, len(filters))
saturation = 0.8
value = 0.8
clrs = [colors.hsv_to_rgb([hue, saturation, value]) for hue in hues]

fills:list[PolyCollection] = []
vlines = []
annots =[]

exclude_filters=[]
for i,file in enumerate(filters):
    if file in exclude_filters:continue
    wave,trans = np.loadtxt(os.path.join(FILTER_DIR,file)).T
    trans = trans#/max(trans)
    lam_repr = np.sum(wave*trans)/np.sum(trans)

    fill=plt.fill_between(wave,trans,fc=(*clrs[i],0.1),ec=(0,0,0,0.1))
    vline=plt.axvline(lam_repr,c='k',ls='--',alpha=0,lw=1)
    annot = plt.gca().annotate(f"{file}\n{lam_repr:.02f}$\AA$",
                               (lam_repr,1.2),(8,-8),xycoords='data',textcoords='offset pixels',ha="left",va="top")

    # --------------------
    fills.append(fill)
    vlines.append(vline)
    annots.append(annot)
    annot.set_visible(False)

plt.xscale("log")
plt.ylim(0,1.2)
plt.yticks([0,0.5,1])
plt.ylabel("Transmission",fontsize=14)
plt.xlabel("Wavelength $(\\AA)$",fontsize=14)

def on_plot_hover(event):
    for i,fill in enumerate(fills):
        fill.set_facecolor((*(clrs[i]),1))
        fill.set_edgecolor((0,0,0,1))
        fill.set_linewidth(1)
        vlines[i].set_alpha(0)
        annots[i].set_visible(False)
    
    if event.inaxes != plt.gca():
        plt.gcf().canvas.draw()
        return
    

    for i,fill in enumerate(fills):
        if fill.contains(event)[0]:
            fill.set_facecolor((*(clrs[i]),0.5))
            fill.set_edgecolor((0,0,0,1))
            fill.set_linewidth(1.5)

            vlines[i].set_alpha(0.5)
            annots[i].set_visible(True)


    plt.gcf().canvas.draw()


plt.gcf().canvas.mpl_connect('motion_notify_event', on_plot_hover)           

plt.subplots_adjust(bottom=0.2)
plt.show()