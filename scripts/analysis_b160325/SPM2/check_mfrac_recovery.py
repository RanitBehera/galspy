import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/SPM2/data/mfrac_recovery250.txt")
gid,stmass,nblob,rec_mask,rec_label=data.T

frac80 =len(rec_label[rec_label>0.8])/len(rec_label) 

plt.plot(stmass,rec_mask,'.',ms=2,label="Mask")
plt.plot(stmass,rec_label,'.',ms=2,label=f"Label: >0.8={frac80*100:.02f}%")


plt.xscale('log')
plt.legend()
plt.xlabel("Stellar Mass")
plt.ylabel("Recovery Fraction")

plt.axhline(0.8,color='k',ls='--',lw=1)




plt.figure()
plt.plot(stmass,nblob,'.',ms=2,label="Nblob")
plt.xscale('log')
plt.xlabel("Stellar Mass")
plt.ylabel("Number of Blobs")

unq_nblob,nblob_count=np.unique(nblob,return_counts=True)
nblob_frac=nblob_count/len(nblob)

plt.yticks(unq_nblob,[f"{int(unq)} ({frac*100:.01f})%" for unq,frac in zip(unq_nblob,nblob_frac)])
plt.subplots_adjust(left=0.2)
plt.show()