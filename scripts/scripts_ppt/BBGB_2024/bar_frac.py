import galspy,os
import numpy as np
import matplotlib.pyplot as plt


PATH = "/mnt/home/student/cranit/NINJA/simulations/L150N2040/SNAPS/"
root = galspy.NavigationRoot(PATH)

filepath = "/mnt/home/student/cranit/RANIT/Repo/galspy/scripts_ppt/BBGB_2024/data" + os.sep + "bar_frac.txt"


if not os.path.exists(filepath):
    sn,a = np.loadtxt(os.path.join(PATH,"Snapshots.txt")).T
    z=(1/a) -1
    z=z[5:]
    sn = np.int32(sn)[5:]
    zgas=[]
    zstar=[]
    for s in sn:
        print(int(s))
        pig = root.PIG(int(s))
        masses = pig.FOFGroups.MassByType()
        gas,dm,_,_,star,bh = masses.T

        tot_gas = np.sum(gas)
        tot_star = np.sum(star)
    
        zgas.append(tot_gas)
        zstar.append(tot_star)
    
    np.savetxt(filepath,np.column_stack((z,zgas,zstar)),header="z gas star")


z,gas,star = np.loadtxt(filepath).T

structure_baryons = gas+star

structure_gas_fraction=gas/structure_baryons

plt.plot(z,structure_gas_fraction)

plt.show()

