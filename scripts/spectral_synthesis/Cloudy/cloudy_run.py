import os,pathlib,shutil,subprocess

# SET PATHS
INPUT_FILE  = "/mnt/home/student/cranit/RANIT/Repo/galspy/study/cloudy/uveffect/HII.in"
OUTPUT_PATH = "/mnt/home/student/cranit/RANIT/Repo/galspy/study/cloudy/uveffect/EH"
TEMP_PATH   = "/mnt/home/student/cranit/RANIT/Repo/galspy/study/cloudy/uveffect/temp2"
DATA_PATH   = OUTPUT_PATH

# Create the TEMP_PATH if it doesn't exist
pathlib.Path(TEMP_PATH).mkdir(parents=True,exist_ok=True)

# Copy the input script to TEMP_PATH
shutil.copy(INPUT_FILE,TEMP_PATH)

# Run cloudy with CLOUDY_DATA_PATH env set
filename=INPUT_FILE.split(os.sep)[-1].removesuffix(".in")
if isinstance(DATA_PATH,str):DATA_PATH=[DATA_PATH]
CLOUDY_DATA_PATH = "+:"+":".join(DATA_PATH)
menv = os.environ.copy()
menv["CLOUDY_DATA_PATH"]=CLOUDY_DATA_PATH
os.chdir(TEMP_PATH)
# ========
if True:
    print("Running Cloudy on TEMP_PATH:\n\t",TEMP_PATH,flush=True)
    result = subprocess.run(["cloudy","-r",filename],
                    stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                    env=menv,shell=False)

    if result.stdout:print(result.stdout.decode())
    if result.stderr:print(result.stderr.decode())
    print("Cloudy Exited.")
# ========

# Copy output files.
# EXTENSIONS=["out","con","ovr"]
# childs = os.listdir(TEMP_PATH)
# childs = [c for c in childs if os.path.isfile(TEMP_PATH + os.sep + c)]
# tocopy = [c for c in childs if c.split(".")[-1] in EXTENSIONS]
# tocopy = [TEMP_PATH + os.sep + f for f in tocopy]

# for file in tocopy:
#     shutil.copy(file,OUTPUT_PATH)



