import numpy as np
import matplotlib.pyplot as plt
import galspec.Cloudy as cd

import galspec.Utility as gu

PATH = "/mnt/home/student/cranit/RANIT/Repo/galspy/study/cloudy/bpass_sed"
fig,ax = plt.subplots(1,2,figsize=(10,5))


Ha=[]
Hb=[]

for i in range(51):
    print(i)
    cloud = cd.CloudyOutputReader(PATH,f"t{i}")

    li = cloud.Lines
    # ================
    _Ha = li.H_alpha
    _Hb = li.H_beta 
    Ha.append(_Ha)
    Hb.append(_Hb)

Ha = np.array(Ha)
Hb = np.array(Hb)

# ============================
x=6+(np.array(range(51))/10)

# Line Intensity
ax[0].plot(x,Ha,label="$H\\alpha$",c='r')
ax[0].plot(x,Hb,label="$H\\beta$",c='b')
ax[0].legend()


# Beautify
for a in ax:
    a.set_xlim(6,9.5)
    a.set_xlabel("Log Age (Year)")

ax[0].set_ylabel("Line Intensity\nReative to $H\\beta$")
plt.suptitle("IMF : Chab_300M \nZ=0.00001")


plt.show()
