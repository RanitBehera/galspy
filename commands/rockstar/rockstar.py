import os,stat, argparse
from galspy.IO.ConfigFile import ReadAsDictionary
import tqdm,numpy

import galspy.IO.BigFile as bf

def completion(env:dict):
    iodir = {"-d":None,"--dir":None}
    return {
        "-t":iodir,
        "--template":iodir,
        "-p":iodir,
        "--postprocess":iodir,
        "-v":None,
        "--verbose":None,
    }


def main(env:dict):
    ap = argparse.ArgumentParser()
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument('-t','--template', action='store_true')
    group.add_argument('-p','--postprocess', action='store_true')
    ap.add_argument("-d","--dir",type=str)
    ap.add_argument("-v","--verbose",action='store_true')
    args = ap.parse_args()

    iodir = args.dir
    if not iodir==None and not os.path.exists(iodir):
        print(f'The path "{iodir}" does not exist.')
        return
    if iodir==None:
        # TODO : Check symfile. If fails set PWD
        iodir = env["PWD"]

    if args.template:
        _rockstar_galaxies_template(iodir)
    elif args.postprocess:
        _rockstar_galaxies_postprocess(env,iodir,args.verbose)

        
            
                    
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



def _rockstar_galaxies_postprocess(env:dict,search_dir:str,verbose:bool=False):
    snap_list=[]
    if os.path.basename(search_dir).startswith("RSG_"):
        snap_list.append(search_dir)
    else:
        childs = os.listdir(search_dir)
        for c in childs:
            full_dir = os.path.join(search_dir,c)
            if os.path.isdir(full_dir) and os.path.basename(c).startswith("RSG_"):
                snap_list.append(full_dir)

    if len(snap_list)==0:
        print(f"No snapshot found.:{search_dir}")
        return

    print(f"Found {len(snap_list)} snapshots.")

    for snap in tqdm.tqdm(snap_list):
        # print(f"\nWorking on : {snap}")
        _Process_Headers(snap,verbose)
        _DumpParticleStart(snap)


                
CWL = 40     
def _Process_Headers(snap_path:str,verbose:bool=False):
    childs = [os.path.join(snap_path,child) for child in os.listdir(snap_path) if os.path.isdir(os.path.join(snap_path,child))]
    for child in childs:
        grands = [os.path.join(child,grand) for grand in os.listdir(child) if os.path.isdir(os.path.join(child,grand))]
        for grand in grands:
            headers = [os.path.join(grand,head) for head in os.listdir(grand) if head.startswith("header_")]
            nfile = len(headers)
            if nfile==0:continue

            if verbose:
                print(f"  Joining Header :".ljust(40) +f"{os.path.basename(child)}/{os.path.basename(grand)}")

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

            if verbose:
                print(f"  Cleaning Header Chunks :".ljust(CWL)+f"{os.path.basename(child)}/{os.path.basename(grand)}")
            
            for head in headers:
                os.remove(head)

def _DumpParticleStart(snap_path:str):
    hid_path = os.path.join(snap_path,"RKSParticles/HaloID")

    header =bf.Header(os.path.join(hid_path,"header")).Read()
    dtype = header["DTYPE"]
    nmemb = header["NMEMB"]
    nfile = header["NFILE"]
    filenames = [("{:X}".format(i)).upper().rjust(6,'0') for i in range(nfile)]
    pstart = []
    for fn in filenames:
        blob_path = os.path.join(hid_path,fn)
        blob_HaloID=bf.Blob(blob_path,dtype).Read()

        val,start,count = numpy.unique(blob_HaloID,return_index=True,return_counts=True)
        pstart.append(start)

    psi = bf.Column(os.path.join(snap_path,"RKSHalos/PP_ParticleStartIndex"))
    psi.Write(pstart,"Overwrite")