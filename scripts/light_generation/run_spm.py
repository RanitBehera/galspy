import galspy as gs
import numpy as np

SIM=gs.NavigationRoot(gs.NINJA.L150N2040_WIND_WEAK)
SN = SIM.SnapNumFromRedshift(14)
PIG=SIM.PIG(SN)


sm = PIG.FOFGroups.MassByType().T[4]
mask = sm>6*PIG.Header.MassTable()[4]
gids = PIG.FOFGroups.GroupID()[mask]

spm=gs.PIGSpectrophotometry(PIG)

DUMP_DIR = "/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/light_generation/data"
# spm.get_light_dict(np.arange(1,100))
# spm.get_light_dict([2])
# spm.get_light_dict([int(gids[0]),int(gids[1])],)
spm.get_light_dict(gids, DUMP_DIR)
