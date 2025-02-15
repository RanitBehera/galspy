import numpy as np
import matplotlib.pyplot as plt


gid,blobnum,uvlum = np.loadtxt("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/SPM2/data/blob_UV_2.txt").T
# mask=blobnum!=0
# uvlum = uvlum[mask]

uvlum=uvlum/200 #roughly 1400A to 1600A
LSOL=3.846e33 #erg s-1
uvlum =uvlum*LSOL # erg s-1 AA-1

PC2CM = 3.086e18
D = 10*PC2CM  # In cm

flam=uvlum/(4*np.pi*D**2)

# lam . f_lam = nu . f_nu
c=3e8*1e10  #in AA s-1
lam = 1500 #in AA in rest

fnu = (lam**2)*flam/c #erg s-1 cm-2 Hz-1 at obs
Jy=1e-23 #erg s-1 cm-2 Hz-1
fnu = fnu/Jy  # in Jy

mAB = -2.5*np.log10(fnu/3631)
M_AB = mAB #as distance was 10pc


from galspec.Utility import LuminosityFunction


log_L,dn_dlogL,error = LuminosityFunction(M_AB,150**3,0.5)
plt.plot(log_L,dn_dlogL)


x = [-22.965968509217227, -22.714659508937057, -22.431937018434454, -22.094240830167536, -21.67801001759394, -21.175392736034077, -20.594240470667298, -19.97382215139801, -19.345549470947468, -18.803664697484145, -18.308900339104593, -17.735602434919073, -17.264398284081402]
y = [-7.426086369245929, -6.730434553005776, -6.026086820375284, -5.399999946925958, -4.782608591811657, -4.2347825775434975, -3.765217422456503, -3.36521760821565, -3.008695783705235, -2.739130535738666, -2.5304349112555586, -2.2434784275912847, -2.0347828031081754]
y=10**np.array(y)
plt.plot(x,y,label="Cosmos-Web")

plt.xlabel("$M_{UV}$")
plt.ylabel("$\phi$")

plt.yscale("log")
# plt.xlim(-24,-18)
plt.legend()
plt.show()
