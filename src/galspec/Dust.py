import numpy as np
import matplotlib.pyplot as plt

# Gordon et. al. (2003)
# DOI: 10.1086/376774
# https://arxiv.org/abs/astro-ph/0305257
# Fitzpatrick & Massa (1990)
# https://ui.adsabs.harvard.edu/abs/1990ApJS...72..163F/abstract
class _FitzpatrickMassa1990:
    def __init__(self,C1,C2,C3,C4,x0,g) -> None:
        self.parameters = [C1,C2,C3,C4,x0,g]

    def D(self,x,g,x0):
        return (x**2)/((((x**2)-(x0**2))**2)+((x**2)*(g**2)))

    def F(self,x):
        f=0.5392*((x-5.9)**2)+0.05644*((x-5.9)**3)
        return np.where(x>=5.9,f,0*f)


    def Get(self,x):
        """
        Input x in 1/micron
        """
        C1,C2,C3,C4,x0,g = self.parameters

        

        # Linear Background Term
        BG = C1 + C2*x
        # Drude Bump for 2175A
        DB = C3*self.D(x,g,x0)
        # Far-UV Curvature term
        FUVCT = C4 * self.F(x)

        return BG + DB + FUVCT 



    


class DustExtinction:
    def __init__(self,wavelengths) -> None:
        """
        Wavelengths in Angstrom
        """
        self._waves = wavelengths
        self._x = 1/(self._waves*1e-10/1e-6)


    def GetLMC(self):
        return _FitzpatrickMassa1990(-0.890,0.998,2.719,0.400,4.579,0.934).Get(self._x)
    
    def GetSMCBar(self):
        return _FitzpatrickMassa1990(-4.959,2.264,0.389,0.461,4.600,1).Get(self._x)
        
    def GetMW(self):
        return _FitzpatrickMassa1990(0.12,0.63,3.26,0.41,4.596,0.96).Get(self._x)