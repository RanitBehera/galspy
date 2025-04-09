import pickle
import numpy as np
import galspy as gs
import matplotlib.pyplot as plt

SIM = gs.NavigationRoot(gs.NINJA.L150N2040)
PIG = SIM.PIG(z=7)
UNITS=PIG.Header.Units


# Light
data = np.loadtxt("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/light_generation/data/out_L150N2040_z7p0_st_chabrier300_bin.csv",usecols=(1,5))
tgid,MAB = data.T
tgid = np.int64(tgid)


PATH_DIR = "/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/column_density/data/"
def DoForFile(filepath:str):
    with open(PATH_DIR+filepath,"rb") as fp:
        clm_data:dict = pickle.load(fp)

    avail_tgid = clm_data.keys()
    avail_mask = [tg in avail_tgid for tg in tgid] 

    mtgid = tgid[avail_mask]
    mMAB = MAB[avail_mask]

    cden = np.array([clm_data[tg] for tg in mtgid])

    # Internal to Physical
    # cden *= UNITS.Density*UNITS.Length
    cden *=0.75/1.67e-24
    cden *=(1+PIG.Header.Redshift())**2

    NHI_AV = 10e21
    AV_NHI = 1/NHI_AV

    AV = AV_NHI*cden

    plt.plot(mMAB,AV,'.',ms=1,label=filepath.removeprefix("L150N2040_z7p0_Av_").removesuffix(".dict"))

DoForFile("L150N2040_z7p0_Av_a1p0.dict")
DoForFile("L150N2040_z7p0_Av_a0p7.dict")

plt.yscale("log")
# plt.xscale("log")
plt.xlabel("MAB (Rest Frame)")
# plt.ylabel("Metal Column Density (Physical)")
plt.legend()
plt.show()