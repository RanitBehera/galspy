import numpy as np
import matplotlib.pyplot as plt
from typing import Literal

# Gordon et. al. (2003)
# DOI: 10.1086/376774
# https://arxiv.org/abs/astro-ph/0305257
# Fitzpatrick & Massa (1990)
# https://ui.adsabs.harvard.edu/abs/1990ApJS...72..163F/abstract
class _FitzpatrickMassa1990:
    MW      = [0.12,0.63,3.26,0.41,4.596,0.96]
    LMC     = [-0.890,0.998,2.719,0.400,4.579,0.934]
    SMC_BAR = [-4.959,2.264,0.389,0.461,4.600,1] 

    def __init__(self) -> None:
        pass

    def D(self,x,g,x0):
        return (x**2)/((((x**2)-(x0**2))**2)+((x**2)*(g**2)))
    
    def F(self,x):
        f=0.5392*((x-5.9)**2)+0.05644*((x-5.9)**3)
        return np.where(x>=5.9,f,0*f)

    def FM(self,x,parameters):
        # Input x in 1/micron
        C1,C2,C3,C4,x0,g = parameters
        BG = C1 + C2*x              # Linear Background Term
        DB = C3*self.D(x,g,x0)      # Drude Bump for 2175A
        FUVR = C4 * self.F(x)      # Far-UV Rise
        return BG + DB + FUVR 



    
class DustExtinction:

    def __init__(self) -> None:
        pass

    def _wave_to_x(self,waves):
        return 1/(waves*1e-10/1e-6)

    def FM(self,wavelengths,model:Literal["MW","LMC","SMC_BAR"]):
        x = self._wave_to_x(wavelengths)
        if model=="MW":
            FM = _FitzpatrickMassa1990().FM(x,_FitzpatrickMassa1990.MW)
        elif model=="LMC":
            FM = _FitzpatrickMassa1990().FM(x,_FitzpatrickMassa1990.LMC)
        elif model=="SMC_BAR":
            FM = _FitzpatrickMassa1990().FM(x,_FitzpatrickMassa1990.SMC_BAR)
        else:
            raise ValueError("Unknown Model.")
        return x,FM


    def ALam(self,wavelengths,model:Literal["MW","LMC","SMC_BAR"],AV,RV):
        x,FM = self.FM(wavelengths,model)
        _,FM_V = self.FM(np.array([5500]),model)
        Alam = AV*(1+(FM/RV))/(1+(FM_V/RV))
        return Alam

    def ALam_b_AV(self,wavelengths,model:Literal["MW","LMC","SMC_BAR"],AV,RV):
        x,FM = self.FM(wavelengths,model)
        _,FM_V = self.FM(np.array([5500]),model)
        Alam_b_AV = (1+(FM/RV))/(1+(FM_V/RV))
        return x,Alam_b_AV

    def GetOpticalDepth(self,wavelengths,model:Literal["MW","LMC","SMC_BAR"],AV,RV):
        Alam = self.ALam(wavelengths,model,AV,RV)
        tau_lam = Alam/1.086
        return tau_lam