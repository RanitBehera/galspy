import galspy as gs
import numpy as np

# SIM=gs.NavigationRoot(gs.NINJA.L250N2040)
# SN = SIM.SnapNumFromRedshift(7)
# PIG=SIM.PIG(SN)

SIM=gs.NavigationRoot("/mnt/home/student/cranit/Data/MP_Gadget/Nishi/L50N1008/SNAPS")
PIG=SIM.PIG(42)


sm = PIG.FOFGroups.MassByType().T[4]
mask = sm>16*PIG.Header.MassTable()[4]
gids = PIG.FOFGroups.GroupID()[mask]

spm=gs.PIGSpectrophotometry(PIG)

DUMP_DIR = "/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/light_generation/data"
# spm.get_light_dict(np.arange(1,100))
# spm.get_light_dict([2])
# spm.get_light_dict([int(gids[0]),int(gids[1])],)
spm.get_light_dict(gids, DUMP_DIR)
