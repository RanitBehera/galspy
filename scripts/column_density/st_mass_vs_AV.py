import numpy as np
import galspy as gs
import matplotlib.pyplot as plt
import pickle

PATH_DIR_CD = "/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/column_density/data/"
def DoFor(sim_path:str,avfilepath:str):
    PIG=gs.NavigationRoot(sim_path).PIG(z=7)

    st_mass = PIG.FOFGroups.MassByType().T[4]

    with open(PATH_DIR_CD+avfilepath,"rb") as fp:
        clm_data:dict = pickle.load(fp)

    TGID = list(clm_data.keys())
    TGID = np.int64(TGID)
    AVs = np.array([clm_data[tg][1] for tg in TGID])

    st_mass=st_mass[TGID-1]*1e10/0.6736

    plt.plot(st_mass,AVs,'.',label=f"{PIG.sim_name}",ms=2)



DoFor(gs.NINJA.L250N2040,"L250N2040_z7p0_Av_a1p0.dict")
DoFor(gs.NINJA.L150N2040,"L150N2040_z7p0_Av_a1p0.dict")

plt.xscale("log")
plt.yscale("log")
plt.legend()
plt.show()