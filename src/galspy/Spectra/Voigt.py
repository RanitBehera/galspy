import numpy as np
from scipy.special import wofz
from typing import Literal
import matplotlib.pyplot as plt
import matplotlib

# ----- Physical Constants (CGS Units)-----
c = 3e10            # Speed of light [cm/s]
q = 4.8e-10         # Elementary charge [esu]
me = 9.1e-28        # Electron mass [g]
m_H = 1.67e-24      # Hydrogen atom mass [g]
k_B = 1.38e-16      # Boltzmann constant [erg/K]

class Line:
    def __init__(self,lambda0_A:float,gamma:float,f:float,label:str=""):
        """
        This class provides a convenient way to store and access the properties 
        of a spectral line.

        Args:
            lambda0_A (float) : Central wavelength of the spectral line in Angstroms.
            gamma (float) : Damping constant of the spectral line due to natural broadening in s^-1 or Hz.
            f (float) : Oscillator strength of the spectral line.
            label (str) : An optional tag or label for the spectral line.
        
        Attributes:
            lambda0 : Central wavelength of the spectral line in centimeters.
            nu0 : Central frequency of the spectral line in Hz.
            sigma : Cross section in cm^2.

        """
        self.lambda0_A = lambda0_A                      # Line central wavelength [A]
        self.gamma = gamma                              # Natural broadening [s^-1]
        self.f = f                                      # Oscillator strength for the Line
        self.label = label
        # -----
        self.lambda0 = self.lambda0_A*1e-8              # Line central wavelength [cm]
        self.nu0 = c/self.lambda0                       # Line central frequency [Hz]
        self.sigma = ((np.pi*(q**2))/(me*c))*self.f     # Cross Section [cm^2]

LINE_BANK ={
    "LyA" : Line(1215.67,6.265e8,0.4162,"LyA")
}



class AbsorbingCloud:
    def __init__(self,temperature:float,absorber_weight:float=1):
        self.absorber_weight = absorber_weight
        self.absorber_mass = absorber_weight * m_H
        self.M = self.absorber_mass
        self.set_temperature(temperature)

    def set_temperature(self,temperature):
        self.temperature = temperature
        self.T = self.temperature
        self.b = np.sqrt(2*k_B*self.T/self.M)           # Doppler parameter [cm/s] (WM : Eq - 3.45)


CLOUD_BANK = {
    "Hydrogen_10000K" : AbsorbingCloud(10000,1)
} 




class Voigt:
    def __init__(self,line:Line,cloud:AbsorbingCloud):
        self.cloud = cloud
        self.line = line

        self.Delta_nu_D = cloud.b/line.lambda0          # Doppler width [Hz] (WM : Eq - 3.47)
        self.a = line.gamma/(4*np.pi*self.Delta_nu_D)   # (WM : Eq - 3.54)

    def _hjerting(a, u):
        # https://arxiv.org/pdf/1504.00322
        z = u + 1j * a
        return np.real(wofz(z))
    
    def get_tau(self,N_A,lambda_A):
        nu = c / (lambda_A * 1e-8)
        u = (nu-self.line.nu0)/self.Delta_nu_D              # (WM : Eq - 3.55)
        H=Voigt._hjerting(self.a,u)
        phi_nu = H/(np.sqrt(np.pi)*self.Delta_nu_D)         # (WM : Eq - 3.52)
        # CHECKED : phi_nu is already normalised.
        tau = N_A*self.line.sigma*phi_nu                    # (WM : Eq - 3.38)
        return tau

    def show_column_density_trend(self,log10_columns,lambda_A_range:float=5,lambda_A_resolution=10000):
        log10_columns=np.float64(log10_columns)
        lambda_A = np.linspace(self.line.lambda0_A - lambda_A_range, self.line.lambda0_A + lambda_A_range, lambda_A_resolution)
        for N in log10_columns:
            tau=self.get_tau(10**N,lambda_A)
            trans = np.exp(-tau)
            plt.plot(lambda_A,trans,label=f"N={int(N)}")
        plt.xlabel("Wavelength ($\\AA$)",fontsize=12)
        plt.ylabel("Transmission",fontsize=12)
        plt.legend(frameon=False,ncols=8,loc="upper center",bbox_to_anchor=(0.5,1.1))
        plt.axvline(self.line.lambda0_A,ls='--',lw=1,color='k')
        plt.ylim(0,1.2)
        plt.show()

    def show_b_parameter_trend(self,log10_column,b_parameters_km_s,lambda_A_range:float=5,lambda_A_resolution=10000):
        log10_column=np.float64(log10_column)
        lambda_A = np.linspace(self.line.lambda0_A - lambda_A_range, self.line.lambda0_A + lambda_A_range, lambda_A_resolution)
        for bkms in b_parameters_km_s:
            b=bkms*1e5
            Delta_nu_D = b/self.line.lambda0          # Doppler width [Hz] (WM : Eq - 3.47)
            a = self.line.gamma/(4*np.pi*Delta_nu_D)
            nu = c / (lambda_A * 1e-8)
            u = (nu-self.line.nu0)/Delta_nu_D
            H=Voigt._hjerting(a,u)
            phi_nu = H/(np.sqrt(np.pi)*Delta_nu_D)
            tau = (10**log10_column)*self.line.sigma*phi_nu
            trans = np.exp(-tau)
            plt.plot(lambda_A,trans,label=f"b={b/1e5:.01f}")
        
        plt.xlabel("Wavelength ($\\AA$)",fontsize=12)
        plt.ylabel("Transmission",fontsize=12)
        plt.legend(frameon=False,ncols=8,loc="upper center",bbox_to_anchor=(0.5,1.1),title="km/s")
        plt.axvline(self.line.lambda0_A,ls='--',lw=1,color='k')
        plt.ylim(0,1.2)
        plt.show()


if __name__ == "__main__":
    line = LINE_BANK["LyA"]
    cloud = CLOUD_BANK["Hydrogen_10000K"]
    vgt=Voigt(line,cloud)
    vgt.show_column_density_trend(np.arange(13,21,1),2)

