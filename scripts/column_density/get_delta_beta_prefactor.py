

import numpy as np
from galspy.Spectra.Dust import DustExtinction


de = DustExtinction()


A1500=de.get_extinction([1500],"Calzetti",1)
A2500=de.get_extinction([2500],"Calzetti",1)

dbeta = (A2500-A1500)/(2.5*np.log10(3/5))

print(dbeta)
