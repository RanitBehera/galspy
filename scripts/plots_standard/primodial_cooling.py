import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

# REFERENCE
# https://arxiv.org/pdf/astro-ph/9509107




T = np.logspace(3.5,8,1000)



# RECOMBINARION RATES
def alpha_HII(T):
    val=8.4e-11
    val*=T**(-1/2)
    val*=(T/1e3)**(-0.2)
    val*=(1+(T/1e6)**0.7)**(-1)
    return val

def alpha_HeII(T):
    val = 1.5e-10
    val*=T**-0.6353
    return val

def alpha_d(T):
    val=1.9e-3
    val*=T**(-1.5)
    val*=np.exp(-470000.0/T)
    val*=(1+0.3*np.exp(-94000.0/T))
    return val

def alpha_HeIII(T):
    val=3.36e-10
    val*=T**(-1/2)
    val*=(T/1e3)**(-0.2)
    val*=(1+(T/1e6)**0.7)**(-1)
    return val

a_HII   = alpha_HII(T)
a_HeII  = alpha_HeII(T)
a_d     = alpha_d(T)
a_HeIII = alpha_HeIII(T)



# COLLISIONAL-INOIZATION RATES
def Gamma_eHI(T):
    val = 5.85e-11
    val*=T**(1/2)
    val*=np.exp(-157809.1/T)
    val*=(1+(T/1e5)**(1/2))**(-1)
    return val

def Gamma_eHeI(T):
    val = 2.38e-11
    val*=T**(1/2)
    val*=np.exp(-285335.4/T)
    val*=(1+(T/1e5)**(1/2))**(-1)
    return val

def Gamma_eHeII(T):
    val = 5.68e-12
    val*=T**(1/2)
    val*=np.exp(-631515.0/T)
    val*=(1+(T/1e5)**(1/2))**(-1)
    return val

G_eHI   = Gamma_eHeI(T)
G_eHeI  = Gamma_eHI(T)
G_eHeII = Gamma_eHeII(T)


# PHOTO-IONIZATION RATES

h = 6.626176e-27 #CGS

def J(nu):
    return 0

def sigma(nu):
    return 0

def Gamma_gamma_i(nu_i):
    def integrand(nu):
        4*np.pi*J(nu)/(h*nu) * sigma(nu)

    return quad(integrand,nu_i,np.inf)

G_gHI = 0
G_gHeI = 0
G_gHeII = 0


# ION ABUNDANCE
rho = 2.89e-6
X   = 0.76
Y   = 0.24 
mp  = 1.6726231e-24 #CGS
y   = Y/(4-4*Y) 
n_H = rho * X /mp

# Photoionisation off
def ion_abun_pi_off():
    n_HI    = n_H*a_HII/(a_HII+G_eHI)
    n_HII   = n_H-n_HI 
    n_HeII  = y*n_H/(1+((a_HeII+a_d)/(G_eHeI))+((G_eHeII)/(a_HeIII)))
    n_HeI   = n_HeII*(a_HeII+a_d)/G_eHeI
    n_HeIII = n_HeII*(G_eHeII)/a_HeIII
    n_e     = n_HII + n_HeII + 2*n_HeIII

    return n_HI,n_HII,n_HeI,n_HeII,n_HeIII,n_e

def ion_abun_pi_on(n_e_input,iter):
    if iter>5:return n_e_input
    # TODO : recursive call



# COOLING
n_HI,n_HII,n_HeI,n_HeII,n_HeIII,n_e = ion_abun_pi_off()

# Free-Free - all ions
def g_ff(T):
    return 1.1 + 0.34*np.exp(-((5.5-np.log10(T))**2)/3.0)

def free_free(T):
    val = 1.42e-27
    val*= g_ff(T)
    val*= T**(1/2)
    val*=(n_HII+n_HeII+4*n_HeIII)
    val*=n_e
    return val

def col_exc_HI(T):
    val = 7.50e-19
    val*=np.exp(-118348/T)
    val*=(1+(T/1e5)**(1/2))**(-1)
    val*=n_e*n_HI
    return val




# PLOTTING
plt.figure()
plt.plot(np.log10(T),np.log10(free_free(T)/(n_H**2)))
plt.plot(np.log10(T),np.log10(col_exc_HI(T)/(n_H**2)))

plt.ylim(-25,-21)






# REFERENCE PLOT
x = [4.051596942993235, 4.051596942993235, 4.081080862215374, 4.110565118855478, 4.1400493754955825, 4.1916459810708515, 4.228501470579965, 4.250614494351061, 4.294840541893252, 4.346437147468522, 4.442260475421913, 4.597051641819583, 4.641277689361774, 4.722358551577148, 4.788697622890434, 4.825553112399548, 4.869779159941739, 4.936118231255026, 5.0245703263394095, 5.164619026999061, 5.334152659134747, 5.481572592663408, 5.724815854145461, 6.004913930300696, 6.299754472193948, 6.653562852531477, 7.058968513280208, 7.434889917388835, 7.810811321497461, 8.009828535437322]
y = [-24.99187016680958, -24.693767020372842, -24.227642276422763, -23.523035313055768, -22.86178861788618, -22.216802085318218, -21.913279091439595, -21.83739837398374, -21.799457953228213, -21.87533867068407, -22.097560975609756, -22.379403711334476, -22.471544715447155, -22.536585365853657, -22.4823849065517, -22.3739837398374, -22.265582573123094, -22.211382113821138, -22.29268292682927, -22.579945882161457, -22.878048780487806, -23.073170731707318, -23.19783206102325, -23.252032520325205, -23.203252032520325, -23.127371191009274, -22.98102972759464, -22.840108483787475, -22.677506857771213, -22.601626016260163]
plt.plot(x,y,'k')








plt.show()
