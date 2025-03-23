import galspy as gs
import numpy as np
import matplotlib.pyplot as plt

SIM=gs.NavigationRoot(gs.NINJA.L150N2040_WIND_WEAK)

SN = SIM.SnapNumFromRedshift(8)
PIG=SIM.PIG(SN)


sm = PIG.FOFGroups.MassByType().T[4]
mask = sm>10*PIG.Header.MassTable()[4]
gids = PIG.FOFGroups.GroupID()[mask]

spm=gs.PIGSpectrophotometry(PIG)

# spm.get_light_dict(np.arange(1,100))
# spm.get_light_dict([2])
# spm.get_light_dict([int(gids[0]),int(gids[1])])
spm.get_light_dict(gids)


















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






