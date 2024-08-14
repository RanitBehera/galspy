import galspy.utility.MassFunction as mf
import matplotlib.pyplot as plt
import numpy as np


astrid  = mf.CosmologyDict(True,67.74,0.3089,0.0486,0.816,0.9667)
ninja   = mf.CosmologyDict(True,69.70,0.2814,0.0464,0.816,0.9710)   # sig8 not used

redshift = 8
m_range = np.logspace(6,14,200)

m,phia=mf.MassFunctionLiterature('Press-Schechter',astrid,redshift,m_range,"dn/dlnM")
m,phin=mf.MassFunctionLiterature('Press-Schechter',ninja,redshift,m_range,"dn/dlnM")

diff = (phia*(0.0486/0.3089))/(phin*(0.0464/0.2814))


# PLOTTINGS
fig,axs = plt.subplots(1,2)
axs[0].plot(m,phia,label="Astrid")
axs[0].plot(m,phin,label="Ninja")
axs[0].set_yscale('log')
axs[0].set_ylabel("$\phi=dn/d\ln(M/M_\odot)$",fontsize=16)

axs[1].plot(m,diff)
axs[1].set_ylabel("$(\phi f_b)_{astrid}/(\phi f_b)_{ninja}$",fontsize=12)

for ax in axs:
    ax.legend()
    ax.set_xscale('log')
    ax.set_xlabel("$M/M_\odot$",fontsize=16)

plt.show()
