import os,stat

def completion():
    return {
        "genic":None,
        "gadget":None,
        "rockstar-galaxies":None,
    }

def help():pass

def main(env:dict,args:list[str]):
    if len(args)<1:return
    
    if args[0].lower()=="rockstar-galaxies":_rockstar_galaxies(env["PWD"])
    elif args[0].lower()=="genic":_genic(os.path.join(env["PWD"],"paramfile.genic"))
    elif args[0].lower()=="gadget":_gadget(os.path.join(env["PWD"],"paramfile.genic"))
    


def _genic(out_path:str):
    # with open(out_path,"w") as fh:
    pass

def _gadget(out_path:str):
    pass


# ==============================
# ====== ROKSTAR GALAXIES ======
# ==============================


def _rockstar_galaxies(out_dir:str):
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
#NUM_READER      = 4     # Overrides the default number of reader tasks set by NUM_BLOCKS.
NUM_WRITERS     = 8     # 1 or mutliple of 8. At least 8 if periodic.
FORK_READERS_FROM_WRITERS   = 1
FORK_PROCESSORS_PER_MACHINE = 8

# ===== Other Options
DELETE_BINARY_OUTPUT_AFTER_FINISHED = 1
FULL_PARTICLE_CHUNKS = 8    # Set equal to NUM_WRITERS

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

