import numpy as np
import matplotlib.pyplot as plt
import os

LyL = 930 #Lyman Limit in Angstrom


# ===== Utility Functions
def HighPass(lam,lam0=LyL,sigma=0.1):
    curve = 1/(1+np.exp(-((lam-lam0)/sigma)))
    return curve

def LowPass(lam,lam0=LyL,sigma=0.01):
    return 1-HighPass(lam,lam0,sigma)

def GetArea(fe,ff,a,b,lam_low=int(LyL/4),lam_high=1e11):
    area1=0
    area2=0

    if a==-1:area1=fe*np.log(912/lam_low)
    else:area1=fe*((912**(a+1))-(lam_low**(a+1)))/(a+1)

    if b==-1:area2=ff*np.log(lam_high/912)
    else:area2=ff*((lam_high**(b+1))-(912**(b+1)))/(b+1)
    
    return area1+area2

# ===== SED Segments
def FUV(lam,fuv0,beta):
    return fuv0*(lam/LyL)**beta

def EUV(lam,euv0,alpha):
    return euv0*(lam/LyL)**alpha

SOLAR = 1e33
def GenSED(lam,euv0,fuv0,alpha,beta):
    Fuv = FUV(lam,fuv0,beta)
    Euv = EUV(lam,euv0,alpha)
    sed = Euv*LowPass(lam)*HighPass(lam,int(LyL/4)) + Fuv*HighPass(lam)

    # print(GetArea(euv0,fuv0,alpha,beta))

    return np.clip(sed,1e-10,None)

def SaveSED(path,lam,euv0,fuv0,alpha,beta):
    sed = GenSED(lam,euv0,fuv0,alpha,beta)
    np.savetxt(path,np.column_stack((lam,sed)),fmt="%d %.15f")

    with open(path, 'r') as file:
        lines = file.readlines()
    lines[0] = lines[0].strip() + f" Flambda units Angstrom extrapolate" + '\n'

    with open(path, 'w') as file:
        file.writelines(lines)


# ===== Generate SED
lam = np.arange(100,100000,1)

#region
if False:
    fig,axs = plt.subplots(2,2)
    ax11,ax12,ax21,ax22 = np.ravel(axs)

    ax11.plot(lam,GenSED(lam,1,1e3,0,-2))
    ax11.plot(lam,GenSED(lam,(10)**0.5,1e3,0,-2))
    ax11.plot(lam,GenSED(lam,10,1e3,0,-2))
    ax11.plot(lam,GenSED(lam,(1000)**0.5,1e3,0,-2))
    ax11.plot(lam,GenSED(lam,100,1e3,0,-2))

    ax21.plot(lam,GenSED(lam,10,1e3,2,-2))
    ax21.plot(lam,GenSED(lam,10,1e3,1,-2))
    ax21.plot(lam,GenSED(lam,10,1e3,0,-2))
    ax21.plot(lam,GenSED(lam,10,1e3,-1,-2))
    ax21.plot(lam,GenSED(lam,10,1e3,-2,-2))

    ax12.plot(lam,GenSED(lam,1,10,0,-2))
    ax12.plot(lam,GenSED(lam,1,(1e3)**0.5,0,-2))
    ax12.plot(lam,GenSED(lam,1,100,0,-2))
    ax12.plot(lam,GenSED(lam,1,(1e5)**0.5,0,-2))
    ax12.plot(lam,GenSED(lam,1,1e3,0,-2))

    ax22.plot(lam,GenSED(lam,1,100,0,-1))
    ax22.plot(lam,GenSED(lam,1,100,0,-1.5))
    ax22.plot(lam,GenSED(lam,1,100,0,-2))
    ax22.plot(lam,GenSED(lam,1,100,0,-2.5))
    ax22.plot(lam,GenSED(lam,1,100,0,-3))

    for ax in [ax11,ax12,ax21,ax22]:
        ax.set_yscale('log')
        ax.set_xscale('log')
        ax.set_xlim(min(lam),max(lam)) 
        ax.set_ylim(1e-1,1e5)
        ax.set_xlabel("Wavelength ($\lambda$) $\AA$")
        ax.axvline(912,ls='--',color='k',lw=1)

    plt.show()
#endregion


if False:
    OUT = "/mnt/home/student/cranit/RANIT/Repo/galspy/study/cloudy/uveffect/EH" + os.sep
    SaveSED(OUT + "eh1.sed",lam,1,1e3,0,-2)
    SaveSED(OUT + "eh2.sed",lam,(28.28427)**0.5,1e3,0,-2)
    SaveSED(OUT + "eh3.sed",lam,28.28427,1e3,0,-2)
    SaveSED(OUT + "eh4.sed",lam,(28.28427*800)**0.5,1e3,0,-2)
    SaveSED(OUT + "eh5.sed",lam,800,1e3,0,-2)

if False:
    OUT = "/mnt/home/student/cranit/RANIT/Repo/galspy/study/cloudy/uveffect/ES" + os.sep
    SaveSED(OUT + "es1.sed",lam,500,1e3,2,-2)
    SaveSED(OUT + "es2.sed",lam,500,1e3,1,-2)
    SaveSED(OUT + "es3.sed",lam,500,1e3,0,-2)
    SaveSED(OUT + "es4.sed",lam,500,1e3,-1,-2)
    SaveSED(OUT + "es5.sed",lam,500,1e3,-2,-2)

if False:
    OUT = "/mnt/home/student/cranit/RANIT/Repo/galspy/study/cloudy/uveffect/FH" + os.sep
    SaveSED(OUT + "fh1.sed",lam,1,10,0,-2)
    SaveSED(OUT + "fh2.sed",lam,1,(1e3)**0.5,0,-2)
    SaveSED(OUT + "fh3.sed",lam,1,100,0,-2)
    SaveSED(OUT + "fh4.sed",lam,1,(1e5)**0.5,0,-2)
    SaveSED(OUT + "fh5.sed",lam,1,1e3,0,-2)

if True:
    OUT = "/mnt/home/student/cranit/RANIT/Repo/galspy/study/cloudy/uveffect/FS" + os.sep
    # SaveSED(OUT + "fs1.sed",lam,10,1e3,0,-3)
    # SaveSED(OUT + "fs2.sed",lam,10,1e3,0,-2.5)
    # SaveSED(OUT + "fs3.sed",lam,10,1e3,0,-2)
    # SaveSED(OUT + "fs4.sed",lam,10,1e3,0,-1.5)
    # SaveSED(OUT + "fs5.sed",lam,10,1e3,0,-1)

    SaveSED(OUT + "fs1.sed",lam,10,1e3,0,-1.5)
    SaveSED(OUT + "fs2.sed",lam,10,1e3,0,-1.4)
    SaveSED(OUT + "fs3.sed",lam,10,1e3,0,-1.3)
    SaveSED(OUT + "fs4.sed",lam,10,1e3,0,-1.2)
    SaveSED(OUT + "fs5.sed",lam,10,1e3,0,-1.1)




# ================





if __name__=="__main__":
    exit()
    sed = GenSED(lam,1,1e3,0,-2)
    path = "/mnt/home/student/cranit/RANIT/Repo/galspy/study/cloudy/uveffect/Test/eh1.sed"
    np.savetxt(path,
               np.column_stack((lam,sed)),fmt="%d %.15f")

    with open(path, 'r') as file:
        lines = file.readlines()
    lines[0] = lines[0].strip() + f" Flambda units Angstrom extrapolate" + '\n'

    with open(path, 'w') as file:
        file.writelines(lines)