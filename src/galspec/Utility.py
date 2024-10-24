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
