import numpy as np
import galspy.FileTypes.BigFile as bf
import galspy.MPGadget as mp

path = "/mnt/home/student/cranit/Work/test_para_rock/OUT_L50N640/RSG_036"
snap = mp.RSGRoot(path).RKSHalos

# length = snap.ParticleLength()
# lbt = np.sum(snap.PP_LengthByType(),axis=1)

# mask = ~(length==0)
# rat = length[mask]/lbt[mask]

# uq = np.unique(rat)
# print(uq)


l = bf.Blob(snap.ParticleLength.path + "/000001").Read()
b = bf.Blob(snap.PP_ParticleBlock.path + "/000001").Read()
print(l[461],b[461])

# for l,lb in zip(length,lbt):
#     print(l,lb)