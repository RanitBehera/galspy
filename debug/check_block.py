import galspy as gs
import numpy as np

import os
import time



SIM = gs.NavigationRoot(gs.NINJA.L150N2040)
PIG = SIM.PIG(z=5)
PIG.print_box_info()

print("slice start")
S,E = PIG.GetParticleBlockIndex(gs.STAR)
print("slice end")

TGID = 20

GID = PIG.Star.GroupID()
A = GID[S[TGID]:E[TGID]]


print(A)
