from galspec.bpass import BPASSCache
import matplotlib.pyplot as plt
import numpy as np
import galspy.utility.Figure.Beautification as bty

specs:dict = BPASSCache("cache/bpass.ch").Read()

Z = "0.02"
Zspecs  = specs[Z]
Tkeys   = specs["T_KEYS"] 
WL      = Zspecs["WL"]

fig,ax = plt.subplots(1,1,figsize=(10,6))
ax:plt.Axes

clrs = bty.GetGradientColorList((0,0,1),(1,0,0),51)
for i,Tkey in enumerate(Tkeys):
    if i==41:break
    # if not i%10==7: continue
    OFFSET = 1/(100**i)
    Tspec   = specs[Z][Tkey]
    ax.plot(WL,Tspec * OFFSET,c=clrs[i])

ax.set_xscale("log")
ax.set_yscale("log")

ax.set_xlim(1,1e5)

# ax.axvline(912,ls='--',c='k',alpha=0.2,lw=1)
# ax.axvline(3646,ls='--',c='k',alpha=0.2,lw=1)
ax.axvspan(3646,7000,color='k',alpha=0.1,ec=None)
ax.axvspan(912,3646,color='k',alpha=0.05,ec=None)
ax.axvspan(912/4,912,color='k',alpha=0.1,ec=None)

# ax.set_yticks([])
bty.AddRydebergScale(ax)

ax.set_xlabel("Wavelength $(\\AA)$",fontsize=12)
ax.set_ylabel("Offset Flux $(L_\odot\ \\AA^{-1})$",fontsize=12)

if True:
    # Stick may be slow due to its calculations
    bty.sticky_tick_to_curve(ax,[0,10,20,30,40],
                             ["1 Myr","10 Myr","100 Myr","1 Gyr","10Gyr"])


plt.title("BPASS Spectra Evolution",fontsize=16,pad=10)
plt.subplots_adjust(bottom=0.15,top=0.8)
plt.tight_layout()
plt.show()







