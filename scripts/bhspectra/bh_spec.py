import numpy as np
import matplotlib.pyplot as plt
from galspec.AGN import ThinDisk

TD1 = ThinDisk(1e8,1,3,30000,0)

freq=np.logspace(-2,20,1000)
L1 = TD1.SpectralLuminosity(freq)
plt.plot(freq,L1*(1e7/1e24))











plt.xscale("log")
plt.yscale("log")
plt.ylim(1,1e7)
plt.xlim(10**9,10**19)
plt.show()



# X-RAY --------
#region
if False:
    def Lnu(nu):
        ax=0.9
        nu_h = 2.417990504024e+18
        nu_l = 3.289846307256e+14
        ecut_h = numpy.exp(-nu/nu_h)
        ecut_l = numpy.exp(-nu_l/nu)
        return nu**(-ax) * ecut_h * ecut_l

    xray = Lnu(freq)

    # normalise
    beta = 0.721
    C =  4.531
    def ang_to_Hz(ang):
        return 3e8/(ang*1e-10)
    def kev_to_Hz(kev):
        h = 4.135667696e-15 # ev / Hz
        return kev * 1000 / h

    nu_2500 = ang_to_Hz(2500)
    nu_2kev = kev_to_Hz(2)

    L_2500 = TD1.SpectralLuminosity(numpy.array([nu_2500]))*1e7
    L_2kev = Lnu(nu_2kev)*1e7


    norm = C*(L_2500**beta)/L_2kev


    plt.plot(freq,xray*norm/1e24)
#endregion

# --------------

# plt.xscale("log")
# plt.yscale("log")
# # plt.ylim(bottom=1e0)
# # plt.xlim(10**12,10**20)
# plt.show()












