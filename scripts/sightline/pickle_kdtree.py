import galspy, pickle, os, time
from scipy import spatial

# ---- FLAGS
SIM_PATH    = "/mnt/home/student/cranit/Data/MP_Gadget/Nishi/L140N1008"
SNAP_NUM    = 24
SAVE_AT     = "/mnt/home/student/cranit/Repo/galspy/temp/outs"
FILENAME    = None


# ---- AUTO FLAGS
if FILENAME==None: FILENAME = f"{os.path.basename(SIM_PATH)}_S{SNAP_NUM}.ckdtree"
FILEPATH = SAVE_AT + os.sep + FILENAME


sim = galspy.NavigationRoot(SIM_PATH)
start_time = time.time()
def elapsed():return "[" + f"{round(time.time()-start_time)}".rjust(5) + "s]"


print(elapsed() + " Reading Gas Positions ...",flush=True)
gas_pos = sim.PART(SNAP_NUM).Gas.Position()

print(elapsed() + " Building kd-Tree ... ",flush=True)
kdt = spatial.cKDTree(gas_pos)

print(elapsed() + " Saving Pickle ...",flush=True)
with open(FILEPATH,"wb") as fp: pickle.dump(kdt,fp)

print(elapsed() + f" Saved as \"{FILEPATH}\"")
