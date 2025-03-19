import  numpy as np
import matplotlib.pyplot as plt
import matplotlib
from galspy.MPGadget import _PART, _PIG

class _Plots:
    def __init__(self,PIG:_PIG):
        self.PIG = PIG

    def SetStyle(fontsize=12):
        font = {
                'family':'serif',
                'serif':['Roboto'],
                'size':fontsize,
                # 'weight' : 'bold'
                }
        matplotlib.rc('font', **font)
        matplotlib.rc('text', usetex=True)

    def mass_metallicity_scatter(self):
        _Plots.SetStyle(14)

        z=self.PIG.Header.Redshift()
        MASS_UNIT = 1e10


        mass_by_type = self.PIG.FOFGroups.MassByType().T
        gas_mass = mass_by_type[0]
        # dm_mass = mass_by_type[1]
        stellar_mass = mass_by_type[4]
        # bh_mass = mass_by_type[5]

        # This is metallicity times mass, 
        # where metallicity in absolute units (not relative to solar) and by mass
        gas_metal_mass = self.PIG.FOFGroups.GasMetalMass()
        stellar_metal_mass = self.PIG.FOFGroups.StellarMetalMass()

        mask = stellar_mass > (10*self.PIG.Header.MassTable()[4])


        # ----- PLOT
        fig,axs = plt.subplots(1,3,figsize=(15,5))
        HEXBIN = False

        ax0:plt.Axes=axs[0]
        if not HEXBIN:
            ax0.plot(gas_mass[mask]*MASS_UNIT,gas_metal_mass[mask]*MASS_UNIT,'.',ms=2)
        else:
            ax0.hexbin(gas_mass[mask]*MASS_UNIT,gas_metal_mass[mask]*MASS_UNIT,
                    gridsize=30,cmap="Oranges",xscale='log',yscale='log',bins='log')
        
        ax1:plt.Axes=axs[1]
        if not HEXBIN:
            ax1.plot(stellar_mass[mask]*MASS_UNIT,gas_metal_mass[mask]*MASS_UNIT,'.',ms=2)
        else:
            ax1.hexbin(stellar_mass[mask]*MASS_UNIT,gas_metal_mass[mask]*MASS_UNIT,
                    gridsize=30,cmap="Oranges",xscale='log',yscale='log',bins='log')

        ax2:plt.Axes=axs[2]
        if not HEXBIN:
            ax2.plot(stellar_mass[mask]*MASS_UNIT,stellar_metal_mass[mask]*MASS_UNIT,'.',ms=2)
        else:
            ax2.hexbin(stellar_mass[mask]*MASS_UNIT,stellar_metal_mass[mask]*MASS_UNIT,
                   gridsize=30,cmap="Oranges",xscale='log',yscale='log',bins='log')
        
        # ----- BEUTIFICATION
        for ax in axs:
            ax:plt.Axes
            ax.set_xscale('log')
            ax.set_yscale('log')
            
            ax.set_aspect('equal',adjustable='box') # box, datalim
        
        ax0.set_xlabel('Gas Mass $(M_\odot/h)$')
        ax0.set_ylabel('Gas Metal Mass $((M_\odot/h))$')
        
        ax1.set_xlabel('Stellar Mass $(M_\odot/h)$')
        ax1.set_ylabel('Gas Metal Mass $((M_\odot/h))$')
        
        ax2.set_xlabel('Stellar Mass $(M_\odot/h)$')
        ax2.set_ylabel('Stellar Metal Mass $((M_\odot/h))$')

        ax0.annotate(f"z={z:.02f}\nN={len(stellar_mass[mask])}",
                     (0,1),(8,-8),"axes fraction","offset pixels",va="top",ha="left",fontsize=14)

        plt.subplots_adjust(bottom=0.15,left=0.15,right=0.85)
        # plt.show()
        plt.savefig("/mnt/home/student/cranit/RANIT/Repo/galspy/temp/Mar19/met_scatter_at_z12.png",dpi=400)

    def main_sequence_plot(self):
        pass

