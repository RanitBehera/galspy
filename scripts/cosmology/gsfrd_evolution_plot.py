#%%
import numpy as np
import matplotlib.pyplot as plt
import os
from galspy.utility.Figure.Beautification import SetMyStyle
SetMyStyle(12)

CACHE_DIR = "/mnt/home/student/cranit/RANIT/Repo/galspy/study/hpc_proposal"
CACHE_NAME = ["sfrd_L150N2040.txt",
              "sfrd_L250N2040.txt"] 

CACHE = [CACHE_DIR + os.sep + FN for FN in CACHE_NAME]
LABELS = ["L150N2040","L250N2040"]
COLORS = ['m','c']

h=0.6736

plt.figure(figsize=(10,8))

for i,file in enumerate(CACHE):
    z,sfrd,sfrd03 = np.loadtxt(file).T
    sfrd = sfrd*(h**3)
    sfrd03 = sfrd03*(h**3)
    mask = (z<15)
    z,sfrd,sfrd03=z[mask],sfrd[mask],sfrd03[mask]
    plt.plot(z,np.log10(sfrd),c=COLORS[i])
    plt.plot(z,np.log10(sfrd03),ls='--',c=COLORS[i])

# Astrid
az,asfrd = np.loadtxt("/mnt/home/student/cranit/RANIT/Repo/galspy/study/astrid/sfrd.txt",delimiter=',').T
asfrd = asfrd
# plt.plot(az,asfrd,label="Astrid",c='k',ls='-',lw=1)

az,asfrd = np.loadtxt("/mnt/home/student/cranit/RANIT/Repo/galspy/study/astrid/sfrd03.txt",delimiter=',').T
asfrd = asfrd
# plt.plot(az,asfrd,label="Astrid03",c='k',ls='--',lw=1)



# Rough Obs

def PlotObs(path,label):
    obs_z,obs_sfrd,errp,errn=np.loadtxt(path).T
    plt.errorbar(obs_z,obs_sfrd,[errn,errp],label=label,fmt='o',capsize=4)


PlotObs("/mnt/home/student/cranit/RANIT/Repo/galspy/obs/sfrd_vs_z/Bouwens_2023.txt","Bouwens et al. (2023)")
PlotObs("/mnt/home/student/cranit/RANIT/Repo/galspy/obs/sfrd_vs_z/Harikane_2023.txt","Harikane et al. (2023)")




x = np.array([3.0342044352420947, 3.782695611086908, 4.905432651170245, 5.91951722048092, 6.788732565604354, 7.899396249285031])
y = np.array([-1, -1.234468912781581, -1.456913824621949, -1.7154307392859574, -1.8897795097571763, -2.202404635063088])

yerrp = np.array([-0.9158317182029152, -1.1082164212838066, -1.3366732647926334, -1.601202386333691, -1.8176352289013051, -2.124248422538758])-y
yerrn = y-np.array([-1.0721442808558708, -1.348697403338142, -1.5651302459057561, -1.8476954376607817, -1.9498996520675385, -2.262525052582041])


plt.errorbar(x,y,[yerrn,yerrp],fmt='.',capsize=4,label="Oesch et al. (2018)")






# plt.yscale('log')
plt.legend()

plt.xlabel("Redshift $(z)$")
plt.ylabel("log$_{10}$(SFRD) $(M_\odot$ yr$^{-1}$ Mpc$^{-3})$")
plt.xlim(4)
plt.show()


# %%
