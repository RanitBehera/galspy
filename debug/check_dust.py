from galspec.Dust import DustExtinction
import numpy as np
import matplotlib.pyplot as plt


lams = np.arange(1000,10000,1)
de = DustExtinction(lams)


plt.plot(de._x,de.GetMW(),label="MW")
plt.plot(de._x,de.GetLMC(),label="LMC")
plt.plot(de._x,de.GetSMCBar(),label="SMC Bar")
plt.legend()
plt.show()
