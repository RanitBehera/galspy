import galspy
import numpy as np
import pickle

BOX = "L250N2040"
MPGADGET_OUTPUT_DIR = f"/mnt/home/student/cranit/NINJA/simulations/{BOX}/SNAPS"

ROOT = galspy.NavigationRoot(MPGADGET_OUTPUT_DIR)
Z=8
SNAP_NUM = ROOT.SnapNumFromZ(Z)



h=0.6736
MASS_UNIT = 1e10/h


# COLUMN 0 : GID
GID = ROOT.PIG(SNAP_NUM).FOFGroups.GroupID()

# COLUMN 1,2,3 : MASS (DM,STAR,BH)
_,GMDM,_,_,GMST,GMBH = (ROOT.PIG(SNAP_NUM).FOFGroups.MassByType().T)*MASS_UNIT

# COLUMN 4,5 : Number (STAR,BH)
_,_,_,_,NST,NBH = ROOT.PIG(SNAP_NUM).FOFGroups.LengthByType().T

# COLUMN 6 : BH Mass Accretion Rate
acc = ROOT.PIG(SNAP_NUM).FOFGroups.BlackholeAccretionRate()
acc*= (MASS_UNIT/3.08568e+16) * (365 * 24 * 3600) # M_sun /year

# COLUMN 7 : Eddington Mass Accretion Rate
Mdot_edd = (2.2e-9/0.1)*GMBH

# COLUMN 8 : Eddington Luminosity (In solar Luminosity Units)
L_edd = 3.2e4 * GMBH


# TABLE
table = np.column_stack((GID,GMDM,GMST,GMBH,NST,NBH,acc,Mdot_edd,L_edd))
table=table[:50000,:]


np.savetxt(f"/mnt/home/student/cranit/RANIT/Repo/galspy/scripts_2/galaxy_statistics/data/table1_{BOX}_{Z}.txt",table,
           header="GID(0) GMDM(1) GMST(2) GMBH(3) NST(4) NBH(5) bh_acc/(Mo/yr)(6) Mdot_edd/(Mo/yr)(7) L_edd/Lo(8)",comments='#',
           fmt="%d %g %g %g %d %d %g %g %g")

# with open("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts_2/galaxy_statistics/data/table1.pcl","wb") as fp:
#     pickle.dump(table,fp)

print("SAVED")





