import galspy
import galspy.MPGadget as mp
import numpy as np
import matplotlib.pyplot as plt

import galspy.utility
import galspy.utility.visualization

PATH = "/mnt/home/student/cranit/Data/MP_Gadget/Nishi/L10N64/output"
SNAP = mp.NavigationRoot(PATH).PART(17)

CENTER  = np.array((6.2,5.4,1.9))
SPAN    = np.array((1,1,1))

ORIGIN  = CENTER - (SPAN/2)
BOUNDS  = ORIGIN + SPAN

OX,OY,OZ = ORIGIN
BX,BY,BZ = BOUNDS


X,Y,Z     = (SNAP.DarkMatter.Position()/1000).T
# BOUND MASKS
MX = (X>OX) & (X<BX)
MY = (Y>OY) & (Y<BY)
MZ = (Z>OZ) & (Z<BZ)
M  = MX & MY & MZ
M=MX
# -------
X   = X[M]
Y   = Y[M]
Z   = Z[M]

# SML       = SNAP.Gas.SmoothingLength()[M]/1000


pos = np.column_stack((X,Y,Z))

if False:
    ax=plt.axes(projection='3d')
    cb=galspy.utility.visualization.CubeVisualizer(ax)
    cb.add_points(pos)
    cb.show()

if False:
    plt.plot(Y,Z,'.',ms=1,alpha=0.01)
    plt.axis("equal")
    plt.show()


