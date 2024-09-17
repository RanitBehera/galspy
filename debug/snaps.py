import numpy as np
import matplotlib.pyplot as plt





primary_snap_redshift=[90,50,20]+list(np.arange(15,-0.1,-0.5))
primary_snaps_redshift=[]
secondary_snaps_scale = np.logspace(np.log10(1/(4+1)),np.log10(1/(11+1)),51)
secondary_snaps_redshift = (1/secondary_snaps_scale)-1
#region
# fig,axs = plt.subplots(2,1)


# for z in primary_snaps:
#     axs[0].plot(z,0,'.',ms=10,color='blue')
#     axs[1].plot(z,0,'.',ms=10,color='blue')

# for z in secondary_snaps:
#     axs[0].plot(z,0,'.',ms=5,color='red')
#     axs[1].plot(z,0,'.',ms=5,color='red')

# axs[1].set_xscale('log')
# axs[0].xaxis.tick_top()

# axs[0].set_ylabel("Linear",fontsize=16)
# axs[1].set_ylabel("Logarithimic",fontsize=16)


# xticks = [1,5,10,15,20,25]
# for ax in axs:
#     ax.set_xticks(xticks)
#     ax.set_xticklabels([str(xt) for xt in xticks]) 
#     ax.set_xlim(1,25)
#     ax.set_ylim(-0.5,0.5)
#     ax.set_yticks([])
#     ax.grid()

# plt.show()
#endregion

all_snaps = np.array(list(primary_snaps_redshift) + list(secondary_snaps_redshift))
all_snaps = np.unique(all_snaps)
all_snaps = np.sort(all_snaps)[::-1]

for i,z in enumerate(all_snaps):
    print(i+1,"z=",np.round(z,4),"a=",np.round(1/(z+1),7))





