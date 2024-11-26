import numpy,os,pickle,itertools, subprocess,time
from concurrent.futures import ThreadPoolExecutor
import threading
import time

BPASS_CACHE_FILE = "/mnt/home/student/cranit/RANIT/Repo/galspy/cache/bpass_chab_300M.ch"
CLOUDY_RUN_ROOT_DIR = "/mnt/home/student/cranit/RANIT/Repo/galspy/scripts_2/cloudy/dump/primodial"
# CLOUDY_TEMPLATE_SCRIPT = "/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/spectral_synthesis/BPASS/bpass_cloudy.in"
CACHE_OUT_DIR = "/mnt/home/student/cranit/RANIT/Repo/galspy/cache"
SUFFIX = "primodial"

# =====================
with open(BPASS_CACHE_FILE,"rb") as fp:
    specs:dict = pickle.load(fp)
Z_KEYS = specs["Z_KEYS"]
T_KEYS = specs["T_KEYS"]
ZT_COMBS = list(itertools.product(Z_KEYS, T_KEYS))


# =====================
def CreateDir(ZT):
    Z,T=ZT
    REL_DIR = f"Z_{Z}" + os.sep + f"T_{T}" 
    CDIR = os.path.join(CLOUDY_RUN_ROOT_DIR,REL_DIR)    
    os.makedirs(CDIR,exist_ok=True)


# =====================
def WriteSEDFile(filepath,angtrom,Flambda):
    # Flambda=np.clip(Flambda,)
    numpy.savetxt(filepath,numpy.column_stack((angtrom,Flambda)),fmt="%d %.7E")
    with open(filepath, 'r') as sed:
        lines = sed.readlines()
    lines[0] = lines[0].strip() + f" Flambda units Angstrom extrapolate" + '\n'
    with open(filepath, 'w') as sed:
        sed.writelines(lines)

def Writefor(ZT):
    Z,T=ZT
    CDIR = CLOUDY_RUN_ROOT_DIR + os.sep + f"Z_{Z}" + os.sep + f"T_{T}" 
    print(f"Z={Z} > log T={T}".ljust(32),end='\r')
    
    Zspecs  = specs[Z]
    Tspec   = Zspecs[T]
    WL      = Zspecs["WL"]
    WriteSEDFile(CDIR + os.sep + f"bpass.sed",WL,Tspec)


# ===========================
TEMPLATE_SCRIPT="""\
table SED "$__SEDFN__.sed"
L(nu) = $__LNORM__ at 456.0 Ryd
#
radius linear parsec 1
sphere
hden 2
#abundances "solar_GASS10.abn"
abundances "primordial.abn"
#
iterate
stop temprature 100
stop pfrac 0.01
#
set save prefix "$__FN__"
save overview ".ovr" last
save continuum ".con" last units Angstrom
save line list column ".lines" "LinesList.dat" last
#
print last
print line sort wavelength range 900 to 10000
"""

LAM_NORM = 2 #In Angstrom
def GenerateCloudyInputs(ZT):
    Z,T=ZT
    CDIR = CLOUDY_RUN_ROOT_DIR + os.sep + f"Z_{Z}" + os.sep + f"T_{T}" 
    print(f"Z={Z} > log T={T}".ljust(32),end='\r')
    
    NORM = specs[Z][T][LAM_NORM-1]
    NORM = NORM * ((LAM_NORM**2)*(3.846e33)/(3e18))
    NORM = numpy.round(numpy.log10(NORM),3)
    
    SCR = TEMPLATE_SCRIPT
    SCR=SCR.replace("$__SEDFN__",f"bpass")
    SCR=SCR.replace("$__FN__",f"bpass")
    SCR=SCR.replace("$__LNORM__",str(NORM))

    with open(CDIR+os.sep+f"script.in","w") as fp:
        fp.write(SCR)



# ========================
LINES_LIST = """\
H  1     4861.32A   # H Ba-beta
H  1     6562.80A   # H Ba-alpha
N  2     6583.45A   # [NII] - BPT
O  3     5006.84A   # [OIII] - BPT
"""

def GenLinesList(ZT):
    Z,T=ZT
    CDIR = CLOUDY_RUN_ROOT_DIR + os.sep + f"Z_{Z}" + os.sep + f"T_{T}" 
    print(f"Z={Z} > log T={T}".ljust(32),end='\r')
    
    with open(CDIR+os.sep+f"LinesList.dat","w") as fp:
        fp.write(LINES_LIST)




# ========================
def RunCloudyInstance(ZT):
    Z,T=ZT
    CDIR = CLOUDY_RUN_ROOT_DIR + os.sep + f"Z_{Z}" + os.sep + f"T_{T}"
    
    while not os.path.exists(CDIR+os.sep+"script.in"):
        print("[ WAITING ]",RDIR,"for script.in")
        time.sleep(1)
    
    while not os.path.exists(CDIR+os.sep+"LinesList.dat"):
        print("[ WAITING ]",RDIR,"for LinesList.dat")
        time.sleep(1)
    
    RDIR = f"Z={Z} > log T={T}"
    print("[ STRATING ]",RDIR)
    

    os.chdir(CDIR)
    s=time.time()
    result = subprocess.run(["cloudy","-r","script"],
            stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    e=time.time()
    
    print(f"[ FINISHED in {round(e-s)}s]",RDIR)

    if result.stdout:print(f"[ {RDIR} ] >",result.stdout.decode())
    if result.stderr:print(f"[ {RDIR} ] >",result.stderr.decode())


# ========================
def VarifyCloudyRunStatus(ZT):
    Z,T=ZT
    CDIR = CLOUDY_RUN_ROOT_DIR + os.sep + f"Z_{Z}" + os.sep + f"T_{T}"
    nfiles = len([item for item in os.listdir(CDIR)
                if os.path.isfile(os.path.join(CDIR, item))])

    if nfiles<7:
        print(f"Check : Z={Z} > log T={T}")

# ======================================
plock = threading.Lock()
def print_lock(msg,**kwargs):
    with plock:
        print(msg,**kwargs)

with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
    print_lock("Creating Directories ...")
    # executor.map(CreateDir, ZT_COMBS)

    print_lock("Coverting BPASS SEDs to Cloudy Format ...")
    # executor.map(Writefor, ZT_COMBS)
    # print_lock("".ljust(32),end='\r')
    
    print_lock("Generating Cloudy input scripts ...")
    # executor.map(GenerateCloudyInputs, ZT_COMBS)
    # print_lock("".ljust(32),end='\r')

    print_lock("Generating LinesList file ...")
    # executor.map(GenLinesList, ZT_COMBS)
    # print_lock("".ljust(32),end='\r')

    print_lock("Running Batch Cloudy ...")
    # executor.map(RunCloudyInstance, ZT_COMBS)

    print_lock("Varifyting Status ...")
    # executor.map(VarifyCloudyRunStatus, ZT_COMBS)

# =========================
# May be cloudy getting run before the input script is created
# fix this. Cloudy not outputting in few folder mostly in Z_0.00001 which run first
# exit()
print("Storing Cache ...")

# ========================
from galspec.Cloudy import CloudyOutputReader

# Diffuseout
CACHE_METALLICITY_DICT1 = {"Z_KEYS":Z_KEYS,"T_KEYS":T_KEYS}
CACHE_METALLICITY_DICT2 = {"Z_KEYS":Z_KEYS,"T_KEYS":T_KEYS}
for Z in Z_KEYS:
    CACHE_METALLICITY_DICT1[Z]={"WL":None}
    CACHE_METALLICITY_DICT2[Z]={"WL":None}
    for T in T_KEYS:
        CDIR = CLOUDY_RUN_ROOT_DIR + os.sep + f"Z_{Z}" + os.sep + f"T_{T}"
        print(f"Z={Z} > log T={T}")
        cout = CloudyOutputReader(CDIR,"bpass").Spectrum.Continuum
        CACHE_METALLICITY_DICT1[Z][T]=cout.DiffuseOut[::-1]
        CACHE_METALLICITY_DICT2[Z][T]=cout.Incident[::-1]
    CACHE_METALLICITY_DICT1[Z]["WL"]=cout.Frequency[::-1]
    CACHE_METALLICITY_DICT2[Z]["WL"]=cout.Frequency[::-1]

    

print("Saving Pickle ...")
filename = BPASS_CACHE_FILE.split("/")[-1].removesuffix(".ch").replace("bpass","cloudy")

with open(CACHE_OUT_DIR + os.sep + f"{filename}_{SUFFIX}.out","wb") as fp:
    pickle.dump(CACHE_METALLICITY_DICT1,fp)

with open(CACHE_OUT_DIR + os.sep + f"{filename}_{SUFFIX}.in","wb") as fp:
    pickle.dump(CACHE_METALLICITY_DICT2,fp)

print("Saved At :",CACHE_OUT_DIR)










