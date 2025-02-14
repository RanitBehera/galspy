import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/SPM2/data/mfrac_recovery.txt")
gid,stmass,nblob,rec_mask,rec_label=data.T

plt.plot(stmass,rec_mask,'.',ms=2,label="Mask")
plt.plot(stmass,rec_label,'.',ms=2,label="Label")

plt.xscale('log')
plt.legend()
plt.xlabel("Stellar Mass")
plt.ylabel("Recovery Fraction")

plt.figure()
plt.plot(stmass,nblob,'.',ms=2,label="Nblob")
plt.xscale('log')
plt.xlabel("Stellar Mass")
plt.ylabel("Number of Blobs")

plt.show()