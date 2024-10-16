import numpy as np
import matplotlib.pyplot as plt
import os

LyL = 912 #Lyman Limit in Angstrom


# ===== Utility Functions
def HighPass(lam,lam0=LyL,sigma=0.1):
    curve = 1/(1+np.exp(-((lam-lam0)/sigma)))
    return curve

def LowPass(lam,lam0=LyL,sigma=0.1):
    return 1-HighPass(lam,lam0,sigma)

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
    return np.clip(sed,1e-10,None)

def SaveSED(path,lam,euv0,fuv0,alpha,beta):
    sed = GenSED(lam,euv0,fuv0,alpha,beta)
    np.savetxt(path,np.column_stack((lam,sed)),fmt="%d %.15f")

    with open(path, 'r') as file:
        lines = file.readlines()
    lines[0] = lines[0].strip() + f" units Angstrom Flambda extrapolate" + '\n'

    with open(path, 'w') as file:
        file.writelines(lines)

# ===== Generate SED
lam = np.arange(100,100000,1)
 
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

def GetLogMiddle(a,b):return (a*b)**0.5

OUT = "/mnt/home/student/cranit/RANIT/Repo/galspy/study/cloudy/uveffect/FH" + os.sep
SaveSED(OUT + "fh1.sed",lam,1,10,0,-2)
SaveSED(OUT + "fh2.sed",lam,1,(1000)**0.5,0,-2)
SaveSED(OUT + "fh3.sed",lam,1,100,0,-2)
SaveSED(OUT + "fh4.sed",lam,1,(1e5)**0.5,0,-2)
SaveSED(OUT + "fh5.sed",lam,1,100,0,-2)