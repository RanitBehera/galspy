import galspy as gs
import numpy as np
import matplotlib.pyplot as plt
from galspy.MPGadget import _Sim


UNIT= 1e10/0.6736

def ForSim(sim_path,z):
    SIM = gs.NavigationRoot(sim_path)
    PIG = SIM.PIG(z=z)

    st_len = PIG.FOFGroups.LengthByType().T[4]
    st_mass = PIG.FOFGroups.MassByType().T[4]
    gas_mass = PIG.FOFGroups.MassByType().T[1]
    avg_met = PIG.FOFGroups.GasMetalMass()




    


    # mask = st_len>16
    mask = st_mass > 1e-3 
    st_mass=st_mass[mask]*UNIT
    gas_mass=gas_mass[mask]*UNIT
    avg_met=avg_met[mask]*UNIT


    plt.plot(gas_mass,(avg_met/gas_mass)/0.02,'.',ms=2,label=SIM.sim_name)
    
ForSim(gs.NINJA.L250N2040,7)
ForSim(gs.NINJA.L150N2040,7)
    
plt.xscale('log')
plt.yscale('log')


plt.legend()
plt.show()











