import os,stat, argparse
from galspy.IO.ConfigFile import ReadAsDictionary
import tqdm,numpy

import galspy.IO.BigFile as bf

import galterm.ansi as ANSI
import galterm.utfsym as UTF8

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
        _DumpParticleBlock(snap)
        _HID_To_Blobname_and_IHID(snap)


                
def _Process_Headers(snap_path:str,verbose:bool=False):
    CWL = 40     
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
            
                print(f"  Cleaning Header Chunks :".ljust(  CWL)+f"{os.path.basename(child)}/{os.path.basename(grand)}")
            for head in headers:
                os.remove(head)




# ========== POST PROCESS FUNCTIONS
PP_STAGE_COLOR  = ANSI.FG_MAGENTA
PP_HLINE_LENGTH = 40
PP_HLINE_CHAR   = UTF8.DOUBLE_HORIZONTAL

def _log_start(header_name):
    print(ANSI.BOLD + PP_STAGE_COLOR + f"{header_name} ".ljust(PP_HLINE_LENGTH,PP_HLINE_CHAR) + ANSI.RESET)

def _log_cross_check(msg:str,success:bool,prestring:str):
    print( prestring + f" {msg} - ",end="")
    if success: print(ANSI.FG_GREEN + "PASSED" + ANSI.RESET)
    else:       print(ANSI.FG_RED   + "FAILED"  + ANSI.RESET)

def _log_finish():
    print(UTF8.LIGHT_UP_RIGHT + UTF8.LIGHT_HORIZONTAL + " FINISHED")


def _DumpParticleBlock(snap_path:str):
    _log_start("PP_ParticleBlock")

    halo_ihid_path = snap_path + os.sep + "RKSHalos/InternalHaloID"
    header =bf.Header(halo_ihid_path + os.sep + "header").Read()
    filenames = [("{:X}".format(i)).upper().rjust(6,'0') for i in range(header["NFILE"])]
    part_ihid_path = snap_path + os.sep + "RKSParticles/InternalHaloID"

    perblob_datalen = [header[fn] for fn in filenames]
    perblob_status  = numpy.zeros(len(filenames))
    for n,fn in enumerate(filenames):
        print(UTF8.LIGHT_VERTICAL_RIGHT+UTF8.LIGHT_HORIZONTAL+" BLOB",fn)
        halo_ihids=bf.Blob(halo_ihid_path + os.sep + fn).Read()
        outblob_data = -1 * numpy.ones((len(halo_ihids),3),dtype='int64')
        outblob_data[:,0] = halo_ihids.astype('int64')

        part_ihids=bf.Blob(part_ihid_path + os.sep + fn).Read()
        val,start,count = numpy.unique(part_ihids,return_index=True,return_counts=True)
        _log_cross_check("Check 1",max(val)<len(halo_ihids),UTF8.LIGHT_VERTICAL + "  " + UTF8.LIGHT_VERTICAL_RIGHT + UTF8.LIGHT_HORIZONTAL)
        _log_cross_check("Check 2",all(start>=0),UTF8.LIGHT_VERTICAL + "  " + UTF8.LIGHT_VERTICAL_RIGHT + UTF8.LIGHT_HORIZONTAL)
        
        start = start.astype('int64')
        count = count.astype('int64')

        for v,s,c in zip(val,start,count):
            outblob_data[v,1:3] = s,c

        print(UTF8.LIGHT_VERTICAL + "  " + UTF8.LIGHT_UP_RIGHT + UTF8.LIGHT_HORIZONTAL + " Dumping Data - ",end="")
        status = bf.Blob(snap_path + os.sep + "RKSHalos/PP_ParticleBlock" + os.sep + fn).Write(outblob_data,'Overwrite') 
        if status == 0:print(ANSI.FG_GREEN + "SUCCESS" + ANSI.RESET)
        elif status == 1: print(ANSI.FG_YELLOW + "SKIPPED" + ANSI.RESET)
        else: print(ANSI.RED + " ERROR" + ANSI.RESET)
        perblob_status[n]=status


    print(UTF8.LIGHT_VERTICAL_RIGHT+UTF8.LIGHT_HORIZONTAL+" HEADER - ",end="")
    if all(not s for s in perblob_status):
        bf.Header(snap_path + os.sep + "RKSHalos/PP_ParticleBlock" + os.sep + "header").WriteFromArg(bf.Get_DTYPE(outblob_data[0]),3,header["NFILE"],perblob_datalen)
        print(ANSI.FG_GREEN + "CREATED" + ANSI.RESET)
    else:
        print(ANSI.FG_RED + "FAILED" + ANSI.RESET)

    _log_finish()
    


def _HID_To_Blobname_and_IHID(snap_path:str):
    hid_path = os.path.join(snap_path,"RKSHalos/HaloID")
    ihid_path = os.path.join(snap_path,"RKSHalos/InternalHaloID")

    nfile = bf.Header(hid_path + os.sep + "header").Read()["NFILE"]
    filenames = [("{:X}".format(i)).upper().rjust(6,'0') for i in range(nfile)]
    data=[]
    for fn in filenames:
        blobnum = int(fn,16) 
        hids = bf.Blob(hid_path+os.sep+fn).Read()
        ihids = bf.Blob(ihid_path+os.sep+fn).Read()
        mask = ~(hids==-1)
        hids = numpy.array(hids[mask],dtype=numpy.int64)
        blobname = blobnum*numpy.ones(len(hids),dtype=numpy.int64)
        ihids = numpy.array(ihids[mask],dtype=numpy.int64)

        blobdata = numpy.column_stack((hids,blobname,ihids))
        data.append(blobdata)
    
    bf.Column(snap_path+os.sep+"RKSHalos/PP_HaloIDLinked").Write(data,"Overwrite")


def _Length_by_Type(snap_path:str):
    _log_start("PP_LengthByType")
    ihid_path   = snap_path + os.sep + "RKSHalos/InternalHaloID"
    pquery_path = snap_path + os.sep + "RKSHalos/PP_ParticleBlock"
    ptype_path  = snap_path + os.sep + "RKSParticles/Type"

    header = bf.Header(ihid_path + os.sep + "header").Read()
    filenames = [("{:X}".format(i)).upper().rjust(6,'0') for i in range(header["NFILE"])]

    perblob_datalen = [header[fn] for fn in filenames]
    perblob_status  = numpy.zeros(len(filenames))
    for n,fn in enumerate(filenames):
        print(UTF8.LIGHT_VERTICAL_RIGHT+UTF8.LIGHT_HORIZONTAL+" BLOB",fn)
        ihids = bf.Blob(ihid_path + os.sep + fn).Read()
        pquerys = bf.Blob(pquery_path + os.sep + fn).Read()

        okay = len(ihids)==len(pquerys)
        _log_cross_check("Check 1",okay,UTF8.LIGHT_VERTICAL + "  " + UTF8.LIGHT_VERTICAL_RIGHT + UTF8.LIGHT_HORIZONTAL)
        if not okay : continue

        outblob_data = numpy.zeros((len(ihids),6),'int64')
        parttype = bf.Blob(ptype_path + os.sep + fn).Read()
        for i,qr in enumerate(pquerys):
            ihid,start,count = qr
            part_block = parttype[start:start+count]
            ptype,pcount = numpy.unique(part_block,return_counts=True)

            # Rockstar types to Mpgadget type conversion
            rock_to_mpg = {0:1,1:0,2:4,3:5}
            ptype = numpy.array([rock_to_mpg[t] for t in ptype])

            for ptype,pcount in zip(ptype,pcount):
                outblob_data[ihid,ptype] = pcount


        print(UTF8.LIGHT_VERTICAL + "  " + UTF8.LIGHT_UP_RIGHT + UTF8.LIGHT_HORIZONTAL + " Dumping Data - ",end="")
        status = bf.Blob(snap_path + os.sep + "RKSHalos/PP_LengthByType" + os.sep + fn).Write(outblob_data,'Overwrite') 
        if status == 0:print(ANSI.FG_GREEN + "SUCCESS" + ANSI.RESET)
        elif status == 1: print(ANSI.FG_YELLOW + "SKIPPED" + ANSI.RESET)
        else: print(ANSI.RED + " ERROR" + ANSI.RESET)
        perblob_status[n]=status

    print(UTF8.LIGHT_VERTICAL_RIGHT+UTF8.LIGHT_HORIZONTAL+" HEADER - ",end="")
    if all(not s for s in perblob_status):
        bf.Header(snap_path + os.sep + "RKSHalos/PP_LengthByType" + os.sep + "header").WriteFromArg(bf.Get_DTYPE(outblob_data[0]),6,header["NFILE"],perblob_datalen)
        print(ANSI.FG_GREEN + "CREATED" + ANSI.RESET)
    else:
        print(ANSI.FG_RED + "FAILED" + ANSI.RESET)

    _log_finish()




if __name__=="__main__":


    # _DumpParticleBlock("/mnt/home/student/cranit/Work/test_para_rock/OUT_L10N64/RSG_017")
    _Length_by_Type("/mnt/home/student/cranit/Work/test_para_rock/OUT_L10N64/RSG_017")