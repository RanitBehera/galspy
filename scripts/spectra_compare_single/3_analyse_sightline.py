import pickle,os
import numpy as np
import matplotlib.pyplot as plt

DDIR = "/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/spectra_compare_single/data"
def Read(tgid,name):
    ddir = DDIR + os.sep + f"GID_{tgid}" + os.sep + name + ".dat"
    with open(ddir,"rb") as fp:
        return pickle.load(fp)

TGID = 4

m_star_gid = Read(TGID,"star_gid")
m_star_pos = Read(TGID,"star_pos")
m_star_mass = Read(TGID,"star_mass")
m_star_pot = Read(TGID,"star_pot")
m_star_id = Read(TGID,"star_id")

id_to_spos = dict(zip(m_star_id, m_star_pos))


cind = np.argmin(m_star_pot)
cpos = m_star_pos[cind]
X,Y,Z=m_star_pos.T
# X0,Y0,Z0 = cpos
X0,Y0,Z0 = np.mean(X),np.mean(Y),np.mean(Z)

X,Y,Z=X-X0,Y-Y0,Z-Z0
POS = np.column_stack((X,Y,Z))
dist = np.linalg.norm(POS,axis=1)

cid = m_star_id[cind]
cdist = dist[cind]



filepath = DDIR + f"/L150N2040_z7p00_{TGID}.dict"
with open(filepath,"rb") as fp:
    data=pickle.load(fp)

cdata = data[cid]
CN,CNZ,CAV,CAVZ = cdata 
odata = np.array([data[sid] for sid in m_star_id])
N,NZ,AV,AVZ=odata.T
# plt.hist(AVZ,bins=100)
# plt.axvline(CAVZ)

# plt.figure()
# plt.plot(dist,AVZ,'.',ms=2)

# plt.scatter(dist,AVZ,s=1,c='r')
# plt.scatter(dist,AV,s=1,c='b')


plt.scatter(dist,N,s=1,c=np.log10(m_star_pos.T[2]-Z0))
plt.plot(cdist,CN,'r.',ms=10)

plt.yscale("log")
plt.xscale("log")

# plt.colorbar()
plt.show()
