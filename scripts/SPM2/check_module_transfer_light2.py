import galspy as gs
import numpy as np

root=gs.NavigationRoot(gs.NINJA.L150N2040)

PIG=root.PIG(43)

spm=gs.PIGSpectrophotometry(PIG)

spm.get_spectrum_dict(np.arange(1,100))







