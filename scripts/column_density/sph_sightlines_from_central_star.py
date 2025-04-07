# %%
import galspy as gs
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import KDTree


SIM = gs.NavigationRoot(gs.NINJA.L150N2040)
PIG = SIM.PIG(z=7)
UNITS=PIG.Header.Units


print("Target Box ".ljust(32,"="))
PIG.print_box_info()


print("\nReading Fields ".ljust(32,"="))
print("- Gas".ljust(8),">","GroupIDs")
gas_gid = PIG.Gas.GroupID()
print("- Gas".ljust(8),">","Positions")
gas_pos = PIG.Gas.Position()
print("- Gas".ljust(8),">","Masses")
gas_mass = PIG.Gas.Mass()
print("- Gas".ljust(8),">","Metallicity")
gas_met = PIG.Gas.Metallicity()
print("- Gas".ljust(8),">","Smoothing Lengths")
gas_sml = PIG.Gas.SmoothingLength()
print("- Star".ljust(8),">","Central Location")

print("- FOF".ljust(8),">","GroupIDs")
fof_gids = PIG.FOFGroups.GroupID()
print("- FOF".ljust(8),">","Stellar Mass")
fof_st_mass = PIG.FOFGroups.MassByType().T[4]


# MASK FOFS =======================
MIN_STAR_NUM = 16
min_st_mass = MIN_STAR_NUM*PIG.Header.MassTable()[4]
fof_mask = fof_st_mass>min_st_mass
print("\nFiltering Target FoFs ".ljust(32,'='))
print(" - Minimum Star Number","=",MIN_STAR_NUM)
print(" - Corresponding Minimum Stellar Mass","=",f"{min_st_mass*1e10:.02e}","Mo/h")
TFOF_GIDS = fof_gids[fof_mask]
print(" - Number of target FoF found","=",len(TFOF_GIDS))


# KERNELS =======================
def CubicSpline(r,h):
    C = (8/(np.pi*h**3))
    q = r/h
    I1=C*(1 - 6*(q**2) + 6*(q**3))
    I2=C*(2*((1-q)**3))
    I3=np.zeros_like(q)
    conditions = [q <= 0.5, np.logical_and(0.5 < q, q <= 1), q > 1]
    output = np.select(conditions,[I1,I2,I3])
    return output


Kernel = CubicSpline
print("\nUsing Kernel :",Kernel.__name__)
# ================================


# %%
cstar_loc = PIG.GetCentralStarLocation()



# %%
def TargetFoF(tgid):
    tmask_gas = gas_gid==tgid
    tmask_star = star_gid==tgid


TargetFoF(2)
# %%
