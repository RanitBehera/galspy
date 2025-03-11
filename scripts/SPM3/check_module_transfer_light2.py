import galspy as gs
import numpy as np
import matplotlib.pyplot as plt

root=gs.NavigationRoot(gs.NINJA.L150N2040)
PIG=root.PIG(43)


sm = PIG.FOFGroups.MassByType().T[4]
mask = sm>50*PIG.Header.MassTable()[4]
gids = PIG.FOFGroups.GroupID()[mask]

spm=gs.PIGSpectrophotometry(PIG)

# spm.get_light_dict(np.arange(1,100))
# spm.get_light_dict([2])
spm.get_light_dict(gids[0])



# ------------- Image
# imgs=spm.get_photometry_image(2)
# b = imgs["F150W"].T
# g = imgs["F200W"].T
# r = imgs["F356W"].T
# b=b/np.max(b)
# g=g/np.max(g)
# r=r/np.max(r)
# rgb = np.stack([r, g, b], axis=-1)

# plt.imshow(rgb,origin="lower")
# plt.gca().set_aspect("equal")
# plt.show()






