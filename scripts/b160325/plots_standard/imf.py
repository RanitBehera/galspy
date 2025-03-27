import numpy
import matplotlib.pyplot as plt

def Salpeter1955(mgrid=None):
    if mgrid==None:
        mgrid = numpy.logspace(-2,2,100)
    xi = mgrid**-2.35
    return mgrid,xi

def Kroupa2001(mgrid=None,include_bin=False):
    if mgrid==None:
        mgrid = numpy.logspace(-2,2,100)
    xi_001_008  = (mgrid**-0.3)*(0.5**-1)*(0.08**-1)
    xi_008_05   = (mgrid**-1.3)*(0.5**-1)
    xi_05_1     = (mgrid**-2.3)*1
    if include_bin:
        xi_1_100    = (mgrid**-2.7)*1
    else:
        xi_1_100    = (mgrid**-2.3)*1

    mask_001_008 = (0.01<=mgrid) & (mgrid<0.08) 
    mask_008_05 = (0.08<=mgrid) & (mgrid<0.5) 
    mask_05_1 = (0.5<=mgrid) & (mgrid<1) 
    mask_1_100 = (1<=mgrid) & (mgrid<=100)

    xi = (xi_001_008 * mask_001_008) + (xi_008_05 * mask_008_05) + (xi_05_1 * mask_05_1) + (xi_1_100 * mask_1_100)
    return mgrid,xi

def Chabrier2003(mgrid=None,imf_type="gal-disk"):
    if mgrid==None:
        mgrid = numpy.logspace(-2,2,100)

    # xi(m) = xi(log m) / m ln 10
    def chab_left(m,A,mc,sigma):
        return  (A/(m*numpy.log(10)))* numpy.exp((-(numpy.log10(m)-numpy.log10(mc))**2)/(2*(sigma**2)))
    def chab_right(m,A,x):
        return  (A/(m*numpy.log(10)))*(m**-x)


    if imf_type == "gal-disk":
        mnorm=1
        xi_l = chab_left(mgrid,0.158,0.08,0.69)
        xi_r = chab_right(mgrid,4.4e-2,1.3)
        mask_l = mgrid<=mnorm
        mask_r = mgrid>mnorm
        xi = (xi_l*mask_l)+(xi_r*mask_r)
        return mgrid, xi/(4.4e-2/numpy.log(10))
    
    if imf_type == "binary":
        mnorm=1
        xi_l = chab_left(mgrid,0.086,0.22,0.57)      
        xi_r = chab_right(mgrid,4.4e-2,1.3)
        mask_l = mgrid<=mnorm
        mask_r = mgrid>mnorm
        xi = (xi_l*mask_l)+(xi_r*mask_r)
        return mgrid, xi/(4.4e-2/numpy.log(10))
    
    if imf_type == "spheroid":
        mnorm=0.7
        xi_l = chab_left(mgrid,3.6e-4,0.22,0.33)      
        xi_r = chab_right(mgrid,7.1e-5,1.3)
        mask_l = mgrid<=mnorm
        mask_r = mgrid>mnorm
        xi = (xi_l*mask_l)+(xi_r*mask_r)
        return mgrid, xi/(7.1e-5/numpy.log(10))
    
    if imf_type == "globular":
        mnorm=0.9
        xi_l = chab_left(mgrid,1,0.33,0.34)      
        xi_r = chab_right(mgrid,1,1.3)
        mask_l = mgrid<=mnorm
        mask_r = mgrid>mnorm
        xi = (xi_l*mask_l) * (chab_right(mnorm,1,1.3)/chab_left(mnorm,1,0.33,0.34))   +(xi_r*mask_r)
        return mgrid, xi/(1/numpy.log(10))



fig,ax = plt.subplots(1,2)

# COMPARE
if True:
    m,xi = Salpeter1955()
    ax[0].plot(m,xi,label="Salpeter (1955)")

    m,xi = Kroupa2001()
    ax[0].plot(m,xi,label="Kroupa (2001)")

    m,xi = Kroupa2001(include_bin=True)
    ax[0].plot(m,xi,label="Kroupa (2001) - UB",ls='--')

    m,xi = Chabrier2003(imf_type="gal-disk")
    ax[0].plot(m,xi,label="Chabrier (2003) - Galactic Disk")

    m,xi = Chabrier2003(imf_type="binary")
    ax[0].plot(m,xi,label="Chabrier (2003) - Stellar Binary")

    m,xi = Chabrier2003(imf_type="spheroid")
    ax[0].plot(m,xi,label="Chabrier (2003) - Spheroid")

    m,xi = Chabrier2003(imf_type="globular")
    ax[0].plot(m,xi,label="Chabrier (2003) - Globular")


# Chabrier Segmentaion
if True:
    m,xi = Kroupa2001()
    ax[1].plot(m,xi,label="Kroupa (2001)",color='b')

    m,xi = Chabrier2003(imf_type="gal-disk")
    # m,xi = Chabrier2003(imf_type="globular")
    ax[1].plot(m,xi,color='r',label="Chabrier (2003) - Galactic Disk")

    # def Chabrier_Disk(m):
    #     mnorm=1
    #     def chab_left(m,A=0.158,mc=0.08,sigma=0.69):
    #         return  (A/(m*numpy.log(10)))* numpy.exp((-(numpy.log10(m)-numpy.log10(mc))**2)/(2*(sigma**2)))
    #     def chab_right(m,A=4.4e-2,x=1.3):
    #         return  (A/(m*numpy.log(10)))*(m**-x)
        
    #     if m<mnorm: return chab_left(m) / (4.4e-2/numpy.log(10))
    #     else: return chab_right(m)/(4.4e-2/numpy.log(10))


    mass_boundaries=numpy.append(numpy.logspace(-2,0,10),100)
    imf_val=[Chabrier2003(m)[1] for m in mass_boundaries]
    # imf_val=[Chabrier2003(m,"globular")[1] for m in mass_boundaries]

    ax[1].plot(mass_boundaries,imf_val,'r.',ms=10)
    # ax[1].plot(mass_boundaries,imf_val,'m.',ms=10)

    alpha=[]
    for i in range(len(mass_boundaries)-1):
        a=-((numpy.log10(imf_val[i]/imf_val[i+1]))/(numpy.log10(mass_boundaries[i]/mass_boundaries[i+1])))
        alpha.append(numpy.round(a,2))
    alpha=numpy.array(alpha)

    alp = "".join([str(numpy.round(a,2))+"," for a in alpha])[:-1]
    bnd = "".join([str(numpy.round(m,2))+"," for m in mass_boundaries])[:-1]

    print("EXPONENT :",alp)
    print("BOUNDARIES :",bnd)

for axi in [ax[0],ax[1]]:
    axi.set_xscale("log")
    axi.set_yscale("log")
    axi.set_xlabel("$M/M_\odot$",fontsize=12)
    axi.set_ylabel("$\\xi(M/M_\odot)$",fontsize=12)
    axi.legend()
    axi.axvline(1,color="k",ls='--',lw=1,alpha=0.2)
    axi.axhline(1,color="k",ls='--',lw=1,alpha=0.2)

# ax[1].set_title("EXPONENT : "+alp+"\n"+"BOUNDARIES : "+bnd,fontsize=8)

plt.show()