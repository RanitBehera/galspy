import numpy as np
import matplotlib.pyplot as plt
from typing import Literal




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


class _Caletti2000:
    def __init__(self) -> None:
        pass

    def k(self,lam_ang,RV):
        lam=np.array(lam_ang)*1e-10/1e-6
        a1,a2 = -1.857,1.040
        b1,b2,b3,b4 = -2.156,1.509,-0.198,0.011
        c=2.659
        mask1=(0.63<=lam) & (lam<=2.20)
        mask2=(0.12<=lam) & (lam<2.20)
        
        _x = 1/lam
        k1 = c*(a1 + a2*_x) + RV
        k2 = c*(b1 + b2*_x + b3*(_x**2) + b4*(_x**3)) + RV

        k = 0*(mask1 * k1) + (mask2 * k2)
        return k

    
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


    def ALam(self,wavelengths,model:Literal["MW","LMC","SMC_BAR","Calzetti"],AV,RV):
        if model in ["MW","LMC","SMC_BAR"]:
            x,FM = self.FM(wavelengths,model)
            _,FM_V = self.FM(np.array([5500]),model)
            Alam = AV*(1+(FM/RV))/(1+(FM_V/RV))
        elif model in ["Calzetti"]:
            A_lam_V = (AV/RV)*_Caletti2000().k([5500],RV)
            Alam = (AV/RV)*_Caletti2000().k(wavelengths,RV) / ((AV/RV)*A_lam_V)
        return Alam

    # def ALam_b_AV(self,wavelengths,model:Literal["MW","LMC","SMC_BAR"],AV,RV):
    #     x,FM = self.FM(wavelengths,model)
    #     _,FM_V = self.FM(np.array([5500]),model)
    #     Alam_b_AV = (1+(FM/RV))/(1+(FM_V/RV))
    #     return x,Alam_b_AV

    def GetOpticalDepth(self,wavelengths,model:Literal["MW","LMC","SMC_BAR"],AV,RV):
        Alam = self.ALam(wavelengths,model,AV,RV)
        tau_lam = Alam/1.086
        return tau_lam