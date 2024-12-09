import galspy
import numpy,os
import matplotlib.pyplot as plt
from galspec.SPM import SpectroPhotoMetry
from concurrent.futures import ThreadPoolExecutor

MPGADGET_OUTPUT_DIR = "/mnt/home/student/cranit/NINJA/simulations/L250N2040/SNAPS" #<-------
GROUP_OFFSET = 0

print("SPM")

# SUFFIX = "solar"      #<-------
SUFFIX = "primordial"   #<-------

BOX = "L250N2040"       #<-------


STELLAR_FILE = f"/mnt/home/student/cranit/RANIT/Repo/galspy/cache/cloudy_chab_300M_{SUFFIX}.in"
NEBULAR_FILE = f"/mnt/home/student/cranit/RANIT/Repo/galspy/cache/cloudy_chab_300M_{SUFFIX}.out"


root = galspy.NavigationRoot(MPGADGET_OUTPUT_DIR)

RED = 10                 #<-------
SNAP_NUM = root.SnapNumFromZ(RED)


PIG = root.PIG(SNAP_NUM)


def DoFor(GO):
    try:
        print(GO)
        spm=SpectroPhotoMetry(MPGADGET_OUTPUT_DIR,SNAP_NUM)
        spm.target_PIG_Group(1+GO)
        spm.project_to_plane()
        spm.generate_pixelwise_grid(grid_resolution=(1,1),mode="NGB")
        MAB_S,MAB_S_red,MAB_T,MAB_T_red, beta_S,beta_S_red,beta_T,beta_T_red = spm.get_table(1200,2600,1500,STELLAR_FILE,NEBULAR_FILE)
    except:
        MAB_S,MAB_S_red,MAB_T,MAB_T_red, beta_S,beta_S_red,beta_T,beta_T_red = 0,0,0,0,0,0,0,0
    
    with open(FILE, 'a') as f:
        numpy.savetxt(f, numpy.column_stack((GO+1,MAB_S,MAB_S_red,MAB_T,MAB_T_red, beta_S,beta_S_red,beta_T,beta_T_red)),
                        fmt='%d %.03f %.03f %.03f %.03f %.03f %.03f %.03f %.03f')

    return 0



# =============================

FILE = f"/mnt/home/student/cranit/RANIT/Repo/galspy/scripts_2/galaxy_statistics/data/table2_{SUFFIX}_{BOX}_{RED}.txt"

# DoFor(0)

with open(FILE,"w") as fp:
    fp.write("#ID(0) MAB_ST(1) MAB_ST_RED(2) MAB_TOT(3) MAB_TOT_RED(4) beta_ST(5) beta_ST_RED(6) beta_TOT(7) beta_TOT_RED(8)\n")

# 
from multiprocessing import Pool

if __name__=="__main__":
    with Pool(24) as pool:
        result=pool.map(DoFor,range(0,30001))

