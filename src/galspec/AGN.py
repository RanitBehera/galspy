import numpy
from scipy.integrate import quad, quad_vec
import matplotlib.pyplot as plt

# Universal Gravitational Constant
G = 6.6743e-11      # SI
# Stefan-Boltzmann Constant
sigma = 5.67e-8     # SI
# Light speed in Vacuume
c = 2.99792458e8    # m/s
# Plank's Constant
h = 6.626e-34       # SI
# Boltzmann Constant
k_B = 1.38e-23        # SI
# Solar Mass
M_solar = 1.988e30  # kg
# Seconds in Year
sec_in_year = 365 * 24 * 3600


class ThinDisk:
    def __init__(self,mass,accretion_rate,inner_edge,outer_edge,axis_inclination:0) -> None:
        """
        Thin Disk Model
        Args:
            mass (float) : Mass of central black hole in units of solar mass.
            accretion_rate : Accretion rate of central black hole in units of solar mass per year.
            inner_edge : Inner edge of disk in units of Schwarzsschild radius
            outer_edge : Outer edge of disk in units of Schwarzsschild radius
        """

        # ===== External Fields
        self.Mass                   = mass  # In Solar Mass
        # self.AccretionRate          = accretion_rate * M_solar / sec_in_year
        self.AccretionEfficiency    = 0.1
        self.AccretionRate          = (2.2e-9/self.AccretionEfficiency) * self.Mass # In Solar Mass per Year
        self.AxisInclination        = axis_inclination
        self.InnerEdge              = inner_edge    # In Schwarschild Radius
        self.OuterEdge              = outer_edge    # In Schwarschild Radius

        
        # ===== SI Units
        self.Mass_SI                 = self.Mass * M_solar
        self.SchwarzschildRadius_SI  = self._get_Rs() 
        self.AccretionRate_SI        = self.AccretionRate * (M_solar / sec_in_year)
        self.InnerEdge_SI            = self.InnerEdge * self.SchwarzschildRadius_SI
        self.OuterEdge_SI            = self.OuterEdge * self.SchwarzschildRadius_SI

    # Schwarzschild Radius
    def _get_Rs(self):
        return 2*G*self.Mass_SI/(c**2)

    # Characteristic Temperature
    def _get_T_Char(self):
        return (3*G*self.Mass_SI*self.AccretionRate_SI)/(8*numpy.pi*sigma)
    
    # needs to be in units of scwraschild radius as external interface
    def Temperature(self,r):
        Tc = self._get_T_Char()
        # print("Tc=",Tc)
        # print("inner=",self.InnerEdge_SI)
        r_SI = r* self.SchwarzschildRadius_SI
        Q = Tc  * (1-((self.InnerEdge_SI/r_SI)**0.5)) / (r_SI**3)
        return Q**0.25

    # def SpectralBrightness(self,r,freq):
    #     C1 = 2*h/(c**2)
    #     C2 = h/k_B
    #     T = self.Temperature(r)
    #     E = (C2 * freq) / T
    #     N = C1 * (freq**3)
    #     D = numpy.exp(E)-1
    #     return N / D
    
    # def SpectralIntensity(self,r,freq):
    #     return numpy.pi * self.SpectralBrightness(r,freq)
    
    def SpectralLuminosity(self,freq):
        Q1 = 4*(numpy.pi**2)*h/(c**2)
        Q2 = Q1 * (freq**3) * numpy.cos(self.AxisInclination)
        Rs_SI = self.SchwarzschildRadius_SI

        def integrand(r_SI,f):
            return (r_SI)/(numpy.exp((h*f)/(k_B*self.Temperature(r_SI/Rs_SI)))-1)


        # r=numpy.logspace(numpy.log10(1.01*self.InnerEdge_SI),numpy.log10(self.OuterEdge_SI),1000)
        # I=integrand(r,freq)
        # plt.plot(r,I)
        # plt.xscale('log')
        # plt.yscale('log')
        # plt.ylim(1e18,1e22)
        # plt.grid()
        # plt.show()

        I = [quad(integrand,self.InnerEdge_SI,self.OuterEdge_SI,args=f)[0] for f in freq]
        return Q2 * I