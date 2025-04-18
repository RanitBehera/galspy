import galspy as gs
import numpy as np


CELL = 12
print("Redshift".ljust(CELL),"HALO".ljust(CELL),"Gas".ljust(CELL),"Star".ljust(CELL))
for z in [5,6,7,8,9,10]:
    PIG=gs.NavigationRoot(gs.NINJA.L150N2040).PIG(z=z)

    lbt = PIG.FOFGroups.LengthByType().T
    gc,dc,sc=lbt[1],lbt[2],lbt[4]
    
    mask = sc>100
    gc = gc[mask]
    dc = dc[mask]
    sc = sc[mask]

    sc_=np.sum(sc)
    gc_=np.sum(gc)

    print(f"{z}".ljust(CELL),f"{len(lbt.T[mask])}".ljust(CELL),f"{gc_}".ljust(CELL),f"{sc_}".ljust(CELL))