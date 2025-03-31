import numpy as np
import matplotlib.pyplot as plt
from galspy.Spectra.Utility import LuminosityFunction
import galspy





def ForFile(path,boxsize):
    gid,mab,mab_s = np.loadtxt(path).T
    BOXSIZE=boxsize/0.6736



    bin_AB,bin_phi,error = LuminosityFunction(mab,BOXSIZE**3,0.5)   # 200 multiplied so that it gets cancelled in the other logic
    plt.plot(bin_AB,bin_phi,label="Light")

    bin_AB,bin_phi,error = LuminosityFunction(mab_s,BOXSIZE**3,0.5)   # 200 multiplied so that it gets cancelled in the other logic
    plt.plot(bin_AB,bin_phi,label="MD Scaling")




ForFile("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/SPM3/data/out_L150N2040.csv",150)



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
