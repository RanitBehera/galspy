import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
from typing import Literal


class _FitzpatrickMassa1990:
    MW      = [0.12,0.63,3.26,0.41,4.596,0.96]
    LMC     = [-0.890,0.998,2.719,0.400,4.579,0.934]
    SMC_BAR = [-4.959,2.264,0.389,0.461,4.600,1] 
    EXISTING_MODELS = ["MW","LMC","SMC_BAR"]
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
        FUVR = C4 * self.F(x)       # Far-UV Rise
        return BG + DB + FUVR 




def _calzetti2000_kappa_interpolation(RV):
    lam_l = np.linspace(0.12,0.63,1000)
    lam_u = np.linspace(0.63,2.20,1000)

    _xl = 1/lam_l
    _xu = 1/lam_u

    a1,a2 = -1.857,1.040
    b1,b2,b3,b4 = -2.156,1.509,-0.198,0.011
    c=2.659

    kl = c*(b1 + b2*_xl + b3*(_xl**2) + b4*(_xl**3)) + RV
    ku = c*(a1 + a2*_xu) + RV

    lam = np.concatenate((lam_l,lam_u))
    kappa = np.concatenate((kl,ku))

    ifun = interpolate.interp1d(lam,kappa,fill_value='extrapolate')
    return ifun 



def _Caletti2000_kappa(lam_ang,RV):
    lam_um=np.array(lam_ang)*(1e-10/1e-6)
    interp_f = _calzetti2000_kappa_interpolation(RV)
    return interp_f(lam_um)


    
class DustExtinction:
    def __init__(self) -> None:
        self.RV={"MW":3.1,"LMC":3.1,"SMC_BAR":2.74,"Calzetti":4.05}

    def _ang_to_um(self,wavelengths):
        lam_um=np.array(wavelengths)*(1e-10/1e-6)
        return 1/lam_um

    def get_kappa(self,wavelengths,model:Literal["MW","LMC","SMC_BAR","Calzetti"]):
        """\kappa_\lambda = A_\lambda/E(B-V)"""
        RV = self.RV[model]

        if model in ["Calzetti"]:
            kappa_B = _Caletti2000_kappa([4400],RV)  
            kappa_V = _Caletti2000_kappa([5500],RV)
            kappa = _Caletti2000_kappa(wavelengths,RV)
            # Normalise to k_B-k_V=1 which it should be by definition
            kappa = kappa/(kappa_B-kappa_V)
        elif model in _FitzpatrickMassa1990.EXISTING_MODELS:
            _x = self._ang_to_um(wavelengths)
            FM = _FitzpatrickMassa1990().FM(_x,getattr(_FitzpatrickMassa1990,model))
        else:
            raise ValueError("Unsupported model passed for dust extinction")

        return kappa

    def get_extinction(self,wavelengths,model:Literal["MW","LMC","SMC_BAR","Calzetti"],AV):
        kappa = self.get_kappa(wavelengths,model)
        A_lambda = (AV/self.RV[model])*kappa
        return A_lambda

    def get_optical_depth(self,wavelengths,model:Literal["MW","LMC","SMC_BAR","Calzetti"],AV):
        Alam = self.get_extinction(wavelengths,model,AV)
        tau_lam = Alam/1.086
        return tau_lam


    def get_reddened_spectrum(self,wavelengths,intrinsic_flux,model:Literal["MW","LMC","SMC_BAR","Calzetti"],AV):
        tau_lam = self.get_optical_depth(wavelengths,model,AV)
        reddened_spectrum = intrinsic_flux*np.exp(-tau_lam)
        return wavelengths, reddened_spectrum
