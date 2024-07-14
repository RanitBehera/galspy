import os,stat
from galspy.IO.ConfigFile import ReadAsDictionary


def completion(env:dict):
    return {
        "--template":None,
        "--post-process":{"-o":None}
    }

def help():pass

def main(env:dict,args:list[str]):
    if len(args)<1:return

    if "--template" in args:
        _rockstar_galaxies_template(env["PWD"])
    elif "--post-process" in args:
        _rockstar_galaxies_postprocess(env,args)
        
            
                    


def _rockstar_galaxies_template(out_dir:str):
    with open(os.path.join(out_dir,"snapnames.txt"),"w") as fp: pass
    with open(os.path.join(out_dir,"blocknames.txt"),"w") as fp: pass
    
    with open(os.path.join(out_dir,"runconfig.cfg"),"w") as fp:
        fp.write(
"""# Rockstar-Galaxies User Configuration

# ===== Input/Output Directory
INBASE  = "..."
OUTBASE = "..."

# ===== Input/Output Format
FILE_FORMAT     = "MPGADGET"
OUTPUT_FORMAT   = "MPGADGET"

# ===== Input Snapshot & Block Names
SNAPSHOT_NAMES  = \"""" + os.path.join(out_dir,"snapnames.txt")+"""\"
BLOCK_NAMES     = \"""" + os.path.join(out_dir,"blocknames.txt")+"""\"
FILENAME        = "<snap>.<block>"

# ===== Parallel Input/Output
PARALLEL_IO     = 1
NUM_BLOCKS      = 4     # Also sets the default number of reader tasks.
#NUM_READERS      = 4     # Overrides the default number of reader tasks set by NUM_BLOCKS.
NUM_WRITERS     = 8     # 1 or mutliple of 8. At least 8 if periodic.
FORK_READERS_FROM_WRITERS   = 1
FORK_PROCESSORS_PER_MACHINE = 8

# ===== Other Options
DELETE_BINARY_OUTPUT_AFTER_FINISHED = 1
# FULL_PARTICLE_CHUNKS = 8    # Set equal to NUM_WRITERS

# ===== Initial FOF Finder
FOF_LINKING_LENGTH  = 0.20
FOF_FRACTION        = 0.7
STRICT_SO_MASSES    = 1

# ===== Periodic options
# If periodic, box size should be larger than 5 times the overlap length
PERIODIC = 0
OVERLAP_LENGTH = 1 #Mpc/h


# ===== Halo Definition
MIN_HALO_PARTICLES = 50
MIN_HALO_OUTPUT_SIZE = 50

SUPPRESS_GALAXIES = 0

"""
        )

    master_path = os.path.join(out_dir,"master.sh")
    worker_path = os.path.join(out_dir,"worker.sh") 
    with open(master_path,"w") as fp:
        fp.write("rockstar-galaxies -c runconfig.cfg")

    with open(worker_path,"w") as fp:
        fp.write('rockstar-galaxies -c "./OUT/auto-rockstar.cfg"')

    # Change permission for executable
    st = os.stat(master_path)
    os.chmod(os.path.join(out_dir,"master.sh"),st.st_mode | stat.S_IEXEC)    

    st = os.stat(worker_path)
    os.chmod(os.path.join(out_dir,"worker.sh"),st.st_mode | stat.S_IEXEC)    



def _rockstar_galaxies_postprocess(env:dict,args:list[str]):
    snap_list = _resolve_directory(env,args)
    for snap in snap_list:
        _Process_Headers(snap)



def _resolve_directory(env:dict,args:list[str]):
    # Get Directory
    search_dir  = ""
    if "-o" in args:
        o_index = args.index("-o")
        if o_index<len(args)-1:
            search_dir=args[o_index+1]
            if not os.path.exists(search_dir):
                print(f"Serach directory {search_dir} doesnot exist.")
                search_dir = ""
            if not os.path.isdir(search_dir):
                print(f"Serach directory {search_dir} is not a directory!")
                search_dir = ""
        else:
            print("No search directory given:")
    
    
    if search_dir=="":
        with_pwd = input("Proceed with current directory? [Y/n] :")
        if with_pwd.lower() in ["y",""]:search_dir = env["PWD"]
        else:return

    # Get Snaps to work with
    snap_list=[]
    if os.path.basename(search_dir).startswith("RSG_"):snap_list.append(search_dir)
    else:
        childs = os.listdir(search_dir)
        for c in childs:
            full_dir = os.path.join(search_dir,c)
            if os.path.isdir(full_dir) and os.path.basename(c).startswith("RSG_"):
                snap_list.append(full_dir)
    
    if len(snap_list)==0:
        print(f"No snapshot found.:{search_dir}")
    else:
        print(f"Found {len(snap_list)} snapshots.")

    return snap_list
                

        
def _Process_Headers(snap_path:str):
    childs = [os.path.join(snap_path,child) for child in os.listdir(snap_path) if os.path.isdir(os.path.join(snap_path,child))]
    for child in childs:
        grands = [os.path.join(child,grand) for grand in os.listdir(child) if os.path.isdir(os.path.join(child,grand))]
        for grand in grands:
            headers = [os.path.join(grand,head) for head in os.listdir(grand) if head.startswith("header_")]
            nfile = len(headers)
            if nfile==0:continue

            dtype_list = []
            nmemb_list = []
            datalen_list = []
            
            for head in headers:
                with open(head) as h:
                    text = h.read()
                    lines = text.split("\n")
                    dtype = lines[0].split(":")[1].strip()
                    nmemb = int(lines[1].split(":")[1].strip())
                    datalen = lines[2].strip()
                    dtype_list.append(dtype)
                    nmemb_list.append(nmemb)
                    datalen_list.append(datalen)

            # Crosscheck
            check_dtype = all(el==dtype_list[0] for el in dtype_list)
            check_nmemb = all(el==nmemb_list[0] for el in nmemb_list)

            if not check_dtype:
                print(f"CROSSCHECK ERROR : All dtypes are not same for {grand}")
                continue
            if not check_nmemb:
                print(f"CROSSCHECK ERROR : All nmembs are not same for {grand}")
                continue
            
            datalen_list.sort()

            with open(os.path.join(grand,"header"),"w") as fp:
                fp.write(f"DTYPE: {dtype_list[0]}\n")
                fp.write(f"NMEMB: {nmemb_list[0]}\n")
                fp.write(f"NFILE: {nfile}\n")
                for dl in datalen_list:
                    fp.write(dl+"\n")


            datalen_list.sort()

            for head in headers:
                os.remove(head)

