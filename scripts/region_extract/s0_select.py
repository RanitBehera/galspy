import numpy as np
import galspy

L50N1008 = "/mnt/home/student/cranit/Data/MP_Gadget/Nishi/L50N1008z05"
SAVEDIR = "/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/region_extract/data_kanish"


root = galspy.NavigationRoot(L50N1008)

st_mass = root.PIG(174).FOFGroups.MassByType().T[4]
gid     = root.PIG(174).FOFGroups.GroupID()

smask = np.argsort(st_mass)
st_mass = st_mass[smask]
gid = gid[smask]


select = st_mass>1


tgid = gid[select][0]
tst_mass = st_mass[select][0]



print(tgid,tst_mass)

