# %%
import galspy as gs
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import KDTree


SIM = gs.NavigationRoot(gs.NINJA.L150N2040)
PIG = SIM.PIG(z=7)
UNITS=PIG.Header.Units


print("READING","-"*62)
gid = PIG.Gas.GroupID()
pos = PIG.Gas.Position()
# met = PIG.Gas.Metallicity()
# sml = PIG.Gas.SmoothingLength()
# den = PIG.Gas.Density()

gid_star = PIG.Star.GroupID()
pos_star = PIG.Star.Position()

# %%
def Target(tgid):
    # STEP 0 - Mask for target particles 
    print("- STEP 0 : Masking for target particles ...")
    tmask=gid==tgid
    tpos=pos[tmask]
    # tmet=met[tmask]
    # tsml=sml[tmask]
    tstar_pos = pos_star[gid_star==tgid]

    for tp in tstar_pos:
        ips = np.linalg.norm(tpos-tp,axis=1)

    print("done")


Target(2)
# %%
