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
        _Plots.SetStyle()

        mass_by_type = self.PIG.FOFGroups.MassByType().T
        gas_mass = mass_by_type[0]
        dm_mass = mass_by_type[1]
        stellar_mass = mass_by_type[4]
        bh_mass = mass_by_type[5]

        # This is metallicity times mass, 
        # where metallicity in absolute units (not relative to solar) and by mass
        gas_metal_mass = self.PIG.FOFGroups.GasMetalMass()
        stellar_metal_mass = self.PIG.FOFGroups.StellarMetalMass()

        mask = stellar_mass > (32*self.PIG.Header.MassTable()[4])

        MASS_UNIT = 1e10

        plt.figure()

        plt.plot(gas_mass[mask]*MASS_UNIT,gas_metal_mass[mask]*MASS_UNIT,'.',ms=2)
        plt.xscale('log')
        plt.yscale('log')
        plt.xlabel('Gas Mass $(M_\odot/h)$')
        plt.ylabel('Metal Mass $((M_\odot/h))$')
        plt.show()

    def main_sequence_plot(self):
        pass

