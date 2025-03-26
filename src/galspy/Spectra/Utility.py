import numpy
from scipy.optimize import curve_fit

def ContinnumFinder(X,Y,Xs:float,Xe:float,N:int=10,mask:callable=None):
    """
    Finds the approximate continnum for a noisy data.
    - X : Array for the X data.
    - Y : Array for the Y data.
    - Xs : X starting boundary.
    - Xe : X ending boundary.
    - N  : Number of left right points for averaging.
    - mask : filter out regions.
    """

    # Indices of finding region
    ind_start = numpy.argmin(numpy.abs(X-Xs))
    ind_end = numpy.argmin(numpy.abs(X-Xe))

    # Data of finding region
    data_X  = X[ind_start:ind_end+1]
    data_Y  = Y[ind_start:ind_end+1]
        
    # Moving Average
    kernel = numpy.ones(int(2*N+1)) / int(2*N+1)
    avg_Y   = numpy.convolve(data_Y,kernel,mode="same")

  
    # Moving Y-Weighted Average
    CX,CY=[],[]
    for i in range(N,len(data_X)-N-1):
        chunk       = data_Y[i-N:i+N+1]
        chunk_avg   = avg_Y[i]
        chunk_var   = numpy.var(chunk)
        chunk_max   = numpy.max(chunk)
        delta       = (chunk - chunk_avg)
        weights     = numpy.exp(-(delta**2)/chunk_var)
        # weights     = numpy.exp(delta/chunk_var)
        chunk_wavg  = numpy.sum(chunk * weights) / numpy.sum(weights) 

        CX.append(data_X[i])
        CY.append(chunk_wavg)

    CX,CY = numpy.row_stack((CX,CY))
    return CX,CY


def SlopeFinder(ang,flam,ang_start,ang_end,ang_repr,guess):
    mask = flam>0
    ang=ang[mask]
    flam=flam[mask]

    log_ang = numpy.log10(ang)
    log_flam = numpy.log10(flam)
    log_ang_start,log_ang_end,log_ang_repr = numpy.log10(numpy.row_stack((ang_start,ang_end,ang_repr)))
    CX,CY = ContinnumFinder(log_ang,log_flam,log_ang_start,log_ang_end,30)
    

    log_flam_repr = log_flam[numpy.argmin(numpy.abs(log_ang-log_ang_repr))]
    def logflam(log_lam,beta):
        return log_flam_repr + beta*(log_lam-log_ang_repr)

    X_HR = numpy.logspace(log_ang_start,log_ang_end,100)
    popt,pcov = curve_fit(logflam,CX,CY,guess)
    beta=popt[0]
    Y_HR = logflam(numpy.log10(X_HR),beta)

    SX = X_HR
    SY = 10**Y_HR
    return SX,SY,beta



def LuminosityFunction(MAB,VOLUME,bins):
    bin_count,bin_edges = numpy.histogram(MAB,bins=bins)
    bin_center = (bin_edges[1:]+bin_edges[:-1])/2
    bin_span = numpy.diff(bin_edges)
    bin_phi = bin_count / (bin_span * VOLUME)
    error=numpy.sqrt(bin_count) / (bin_span * VOLUME)
    return bin_center,bin_phi,error