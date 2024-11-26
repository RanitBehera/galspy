import galspy
import numpy as np
import os


MPGADGET_OUTPUT_DIR = "/mnt/home/student/cranit/NINJA/simulations/L150N2040/SNAPS"
SNAP_NUM = 43
ROOT = galspy.NavigationRoot(MPGADGET_OUTPUT_DIR)

h=0.6736
MASS_UNIT = 1e10/h


# COLUMN 0 : GID
GID = ROOT.PIG(SNAP_NUM).FOFGroups.GroupID()

# COLUMN 1,2,3 : MASS (DM,STAR,BH)
_,GMDM,_,_,GMST,GMBH = (ROOT.PIG(SNAP_NUM).FOFGroups.MassByType().T)*MASS_UNIT

# COLUMN 4,5 : Number (STAR,BH)
_,_,_,_,NST,NBH = ROOT.PIG(SNAP_NUM).FOFGroups.LengthByType().T

# COLUMN 6 : BH Accretion Rate
acc = ROOT.PIG(SNAP_NUM).FOFGroups.BlackholeAccretionRate()
acc*= (MASS_UNIT/3.08568e+16) * (365 * 24 * 3600) # M_sun /year

# COLUMN 7 : Eddington Ratio









