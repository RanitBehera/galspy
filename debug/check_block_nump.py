import numpy as np
import galspy.IO.BigFile as bf
import galspy.IO.MPGadget as mp

path = "/mnt/home/student/cranit/Work/test_para_rock/OUT_L50N640/RSG_036"
snap = mp.RSGRoot(path).RKSHalos

nump = snap.ParticleLength()
bp = snap.PP_ParticleBlock()[:,2]

mask = ~(nump==0)

rat = nump[mask]/bp[mask]
uq=np.unique(rat)
print(uq)


# for n,b in zip(nump,bp):
#     print(n,b)