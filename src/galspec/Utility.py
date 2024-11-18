import numpy
from scipy.optimize import curve_fit

def ContinnumFinder(X,Y,Xs:float,Xe:float,N:int=10,mask:callable=None,sigma=0.001):
    """
    Finds the approximate continnum for a noisy data.
    - X : Array for the X data.
    - Y : Array for the Y data.
    - Xs : X starting boundary.
    - Xe : X ending boundary.
    - N  : Number of left right points for averaging.
    - mask : filter out regions.
    """

    # find array for X start and end
    X, Y = numpy.row_stack((X,Y))

    ind_start = numpy.argmin(numpy.abs(X-Xs))
    ind_end = numpy.argmin(numpy.abs(X-Xe))

    # Moving Average
    data_X  = X[ind_start:ind_end+1]
    data_Y  = Y[ind_start:ind_end+1]
    kernel = numpy.ones(int(2*N+1)) / int(2*N+1)
    avg_Y   = numpy.convolve(data_Y,kernel,mode="same")
    
    # Moving Y-Weighted Average
    CX,CY=[],[]
    for i in range(N,len(data_X)-N-1):
        chunk       = data_Y[i-N:i+N+1]
        chunk_avg   = avg_Y[i]
        chunk_max   = max(chunk)
        delta       = (chunk - chunk_max)
        weights     = numpy.exp(-(delta**2)/sigma)
        # weights     = numpy.exp(delta/sigma)
        chunk_wavg  = numpy.sum(chunk * weights) / numpy.sum(weights) 

        CX.append(data_X[i])
        CY.append(chunk_wavg)

    CX,CY = numpy.row_stack((CX,CY))
    return CX,CY


def SlopeFinder(ang,flam,ang_start,ang_end,ang_repr,flam_repr,guess):
    log_ang = numpy.log10(ang)
    log_flam = numpy.log10(flam)
    ang_start,ang_end,ang_repr = numpy.log10(numpy.row_stack((ang_start,ang_end,ang_repr)))
    CX,CY = ContinnumFinder(log_ang,log_flam,ang_start,ang_end,100)
    
    log_flam_repr = numpy.log10(flam_repr)
    def logflam(log_lam,beta):
        return log_flam_repr + beta*(log_lam-ang_repr)

    X_HR = numpy.linspace(10**ang_start,10**ang_end,100)
    popt,pcov = curve_fit(logflam,CX,CY,guess)
    beta=popt[0]
    Y_HR = logflam(numpy.log10(X_HR),beta)

    SX = X_HR
    SY = 10**Y_HR
    return SX,SY,beta


def BandFluxFinder(ang,flam,ang_repr,ang_range):
    mask1 = (ang>=ang_repr-ang_range)
    mask2 = (ang<=ang_repr+ang_range)
    mask = mask1 & mask2

    band_ang = ang[mask]
    band_flam = flam[mask]

    sort = numpy.argsort(band_ang)
    band_lam = band_ang[sort]
    band_flam = band_flam[sort]


    dlam = numpy.diff(band_lam)
    avg_flux = numpy.sum(band_flam[:-1] * dlam)/(band_lam[-1]-band_lam[0])

    return avg_flux

def TwoBandSlopeFinder(ang,flam,lam1,lam2,range1,range2):
    # Make sure lam1<lam2
    if lam1>lam2:
        lam1,lam2 = lam2,lam1
        range1,range2 = range2,range1
    
    flx1 = BandFluxFinder(ang,flam,lam1,range1)
    flx2 = BandFluxFinder(ang,flam,lam2,range2)

    log10_flux_ratio = numpy.log10(flx1/flx2)
    log10_lam_ratio = numpy.log10(lam1/lam2)

    return log10_flux_ratio/log10_lam_ratio


def LuminosityToABMagnitude(lum_erg_s_A,lam_repr):
    area = 4 * numpy.pi * (10 * 3.086e18)**2
    lam = 1400 #UV
    f_lam = lum_erg_s_A/area
    f_nu_Jy = (3.34e4*(lam_repr)**2)*f_lam

    M_AB = -2.5*numpy.log10(f_nu_Jy/3631)
    return M_AB




def LuminosityFunction(MUVAB,VOLUME,LogBinStep):
    MUVAB = MUVAB[MUVAB!=0]
    
    # log10_Mass=numpy.log10(MUVAB)
    # Will exponent on e in front-end to get back mass, So no confilict with log10
    log_MUVAB=numpy.log(MUVAB)

    log_bin_start=numpy.floor(min(log_MUVAB))
    log_bin_end=numpy.ceil(max(log_MUVAB))

    BinCount=numpy.zeros(int((log_bin_end-log_bin_start)/LogBinStep))

    for lm in log_MUVAB:
        i=int((lm-log_bin_start)/LogBinStep)
        BinCount[i]+=1

    log_L=numpy.arange(log_bin_start,log_bin_end,LogBinStep)+(LogBinStep/2)
    dn_dlogL=BinCount/(VOLUME*LogBinStep)
    error=numpy.sqrt(BinCount)/(VOLUME*LogBinStep)

    return log_L,dn_dlogL,error