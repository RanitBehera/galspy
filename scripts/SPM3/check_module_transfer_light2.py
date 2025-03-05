import galspy as gs
import numpy as np
import matplotlib.pyplot as plt

root=gs.NavigationRoot(gs.NINJA.L150N2040)

PIG=root.PIG(43)

spm=gs.PIGSpectrophotometry(PIG)

# spm.get_light_dict(np.arange(1,100))
# spm.get_light_dict([1,2])

spm.get_image(1)


plt.show()




