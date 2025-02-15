import os,stat, argparse
from galspy.FileTypes.ConfigFile import ReadAsDictionary
import tqdm,numpy

import galspy.FileTypes.BigFile as bf
import galspy.utility.HaloQuery as hq

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

    snap_list.sort()

    # Use tqdm when no-verbose ... function print needs to be modified
    # for snap in tqdm.tqdm(snap_list):
    for snap in snap_list:
        # print(f"\nWorking on : {snap}")
        _post_process_snap(snap)    

def _post_process_snap(snap):
    _Process_Headers(snap)
    _DumpParticleBlock(snap)
    _HID_To_Blobname_and_IHID(snap)
    _Length_by_Type(snap)
    _Mass_by_Type(snap)
    _Length_And_Mass_By_Type_With_Sub(snap)


# ========== POST PROCESS FUNCTIONS
PP_SNAP_COLOR  = ANSI.FG_CYAN
PP_STEP_COLOR  = ANSI.FG_MAGENTA
PP_HLINE_LENGTH = 72
PP_HLINE_CHAR   = UTF8.DOUBLE_HORIZONTAL

def _log_start(header_name,snap_path):
    print("\n" + ANSI.BOLD + PP_SNAP_COLOR + os.path.basename(snap_path) + ANSI.RESET,end="")
    print(" " + UTF8.LEFT_ANGLE_ORNAMENT + " ",end="")
    print(ANSI.BOLD + PP_STEP_COLOR + f"{header_name} ".ljust(PP_HLINE_LENGTH,PP_HLINE_CHAR) + ANSI.RESET)

def _log_cross_check(msg:str,success:bool,prestring:str):
    print( prestring + f" {msg} - ",end="")
    if success: print(ANSI.FG_GREEN + "PASSED" + ANSI.RESET)
    else:       print(ANSI.FG_RED   + "FAILED"  + ANSI.RESET)

def _log_finish():
    print(UTF8.LIGHT_UP_RIGHT + UTF8.LIGHT_HORIZONTAL + " FINISHED")


def _Process_Headers(snap_path:str):
    _log_start("Headers Merging",snap_path)
    CWL = 40     
    childs = [snap_path+os.sep+child for child in os.listdir(snap_path) if os.path.isdir(snap_path+os.sep+child)]
    for child in childs:
        grands = [child+os.sep+grand for grand in os.listdir(child) if os.path.isdir(child+os.sep+grand)]
        for grand in grands:
            headers = [grand+os.sep+head for head in os.listdir(grand) if head.startswith("header_")]
            nfile = len(headers)

            print(UTF8.LIGHT_VERTICAL_RIGHT+UTF8.LIGHT_HORIZONTAL + f" {os.path.basename(child)}/{os.path.basename(grand)}")
            if nfile==0:
                print(UTF8.LIGHT_VERTICAL + "  " + UTF8.LIGHT_UP_RIGHT + UTF8.LIGHT_HORIZONTAL + " No headers chunk found.")
                continue

            dtype_list = []
            nmemb_list = []
            dataline_list = []
            
            for head in headers:
                with open(head) as h:
                    text = h.read()
                    lines = text.split("\n")
                    dtype = lines[0].split(":")[1].strip()
                    nmemb = int(lines[1].split(":")[1].strip())
                    dtype_list.append(dtype)
                    nmemb_list.append(nmemb)
                    dataline_list.append(lines[2].strip())

            # Crosscheck
            check_dtype = all(el==dtype_list[0] for el in dtype_list)
            check_nmemb = all(el==nmemb_list[0] for el in nmemb_list)
            _log_cross_check("Check 1",check_dtype,UTF8.LIGHT_VERTICAL + "  " + UTF8.LIGHT_VERTICAL_RIGHT + UTF8.LIGHT_HORIZONTAL)
            _log_cross_check("Check 2",check_nmemb,UTF8.LIGHT_VERTICAL + "  " + UTF8.LIGHT_VERTICAL_RIGHT + UTF8.LIGHT_HORIZONTAL)
            
            dataline_list.sort()

            print(UTF8.LIGHT_VERTICAL + "  " + UTF8.LIGHT_VERTICAL_RIGHT + UTF8.LIGHT_HORIZONTAL + " Merging - ",end="")
            with open(os.path.join(grand,"header"),"w") as fp:
                fp.write(f"DTYPE: {dtype_list[0]}\n")
                fp.write(f"NMEMB: {nmemb_list[0]}\n")
                fp.write(f"NFILE: {nfile}\n")
                for dl in dataline_list:
                    fp.write(dl+"\n")
            print(ANSI.FG_GREEN + "DONE" + ANSI.RESET)
            
            print(UTF8.LIGHT_VERTICAL + "  " + UTF8.LIGHT_UP_RIGHT + UTF8.LIGHT_HORIZONTAL + " Cleaning headers chunks - ",end="")
            for head in headers:os.remove(head)
            print(ANSI.FG_GREEN + "DONE" + ANSI.RESET)
            
    _log_finish()



def _DumpParticleBlock(snap_path:str):
    _log_start("PP_ParticleBlock",snap_path)

    halo_ihid_path = snap_path + os.sep + "RKSHalos/InternalHaloID"
    header =bf.Header(halo_ihid_path + os.sep + "header").Read()
    filenames = [("{:X}".format(i)).upper().rjust(6,'0') for i in range(header["NFILE"])]
    part_ihid_path = snap_path + os.sep + "RKSParticles/InternalHaloID"

    outcolumn_data = []
    for n,fn in enumerate(filenames):
        print(UTF8.LIGHT_VERTICAL_RIGHT+UTF8.LIGHT_HORIZONTAL+" BLOB",fn)
        halo_ihids=bf.Blob(halo_ihid_path + os.sep + fn).Read()
        outblob_data = -1 * numpy.ones((len(halo_ihids),3),dtype='int64')
        outblob_data[:,0] = halo_ihids.astype('int64')

        if len(halo_ihids)==0:
            print(UTF8.LIGHT_VERTICAL + "  " + UTF8.LIGHT_UP_RIGHT + UTF8.LIGHT_HORIZONTAL + " Empty Blob - " + ANSI.FG_YELLOW + "YES" + ANSI.RESET)
        else:
            print(UTF8.LIGHT_VERTICAL + "  " + UTF8.LIGHT_VERTICAL_RIGHT + UTF8.LIGHT_HORIZONTAL + " Empty Blob - " + ANSI.FG_GREEN + "NO" + ANSI.RESET)
            part_ihids=bf.Blob(part_ihid_path + os.sep + fn).Read()
            val,start,count = numpy.unique(part_ihids,return_index=True,return_counts=True)
            _log_cross_check("Check 1",max(val)<len(halo_ihids),UTF8.LIGHT_VERTICAL + "  " + UTF8.LIGHT_VERTICAL_RIGHT + UTF8.LIGHT_HORIZONTAL)
            _log_cross_check("Check 2",all(start>=0),UTF8.LIGHT_VERTICAL + "  " + UTF8.LIGHT_VERTICAL_RIGHT + UTF8.LIGHT_HORIZONTAL)
        
            start = start.astype('int64')
            count = count.astype('int64')

            for v,s,c in zip(val,start,count):
                outblob_data[v,1:3] = s,c
        
        outcolumn_data.append(outblob_data)


    print(UTF8.LIGHT_VERTICAL_RIGHT + UTF8.LIGHT_HORIZONTAL + " Dumping Data - ",end="")
    bf.Column(snap_path+os.sep+"RKSHalos/PP_ParticleBlock").Write(outcolumn_data,"Overwrite")
    print(ANSI.FG_GREEN + "SUCCESS" + ANSI.RESET)

    _log_finish()
    

def _HID_To_Blobname_and_IHID(snap_path:str):
    _log_start("PP_HaloIDLinked",snap_path)
    hid_path = os.path.join(snap_path,"RKSHalos/HaloID")
    ihid_path = os.path.join(snap_path,"RKSHalos/InternalHaloID")

    nfile = bf.Header(hid_path + os.sep + "header").Read()["NFILE"]
    filenames = [("{:X}".format(i)).upper().rjust(6,'0') for i in range(nfile)]
    data=[]
    for fn in filenames:
        print(UTF8.LIGHT_VERTICAL_RIGHT+UTF8.LIGHT_HORIZONTAL+" BLOB",fn)
        blobnum = int(fn,16) 
        hids = bf.Blob(hid_path+os.sep+fn).Read()
        ihids = bf.Blob(ihid_path+os.sep+fn).Read()
        mask = ~(hids==-1)
        hids = numpy.array(hids[mask],dtype=numpy.int64)
        blobname = blobnum*numpy.ones(len(hids),dtype=numpy.int64)
        ihids = numpy.array(ihids[mask],dtype=numpy.int64)

        blobdata = numpy.column_stack((hids,blobname,ihids))
        data.append(blobdata)
    
    print(UTF8.LIGHT_VERTICAL_RIGHT + UTF8.LIGHT_HORIZONTAL + " Dumping Data - ",end="")
    bf.Column(snap_path+os.sep+"RKSHalos/PP_HaloIDLinked").Write(data,"Overwrite")
    print(ANSI.FG_GREEN + "SUCCESS" + ANSI.RESET)

    _log_finish()

def _Length_by_Type(snap_path:str):
    _log_start("PP_LengthByType",snap_path)
    ihid_path   = snap_path + os.sep + "RKSHalos/InternalHaloID"
    pquery_path = snap_path + os.sep + "RKSHalos/PP_ParticleBlock"
    ptype_path  = snap_path + os.sep + "RKSParticles/Type"

    header = bf.Header(ihid_path + os.sep + "header").Read()
    filenames = [("{:X}".format(i)).upper().rjust(6,'0') for i in range(header["NFILE"])]

    outcolumn_data=[]
    for n,fn in enumerate(filenames):
        print(UTF8.LIGHT_VERTICAL_RIGHT+UTF8.LIGHT_HORIZONTAL+" BLOB",fn)
        ihids = bf.Blob(ihid_path + os.sep + fn).Read()
        pquerys = bf.Blob(pquery_path + os.sep + fn).Read()

        okay = len(ihids)==len(pquerys)
        _log_cross_check("Check 1",okay,UTF8.LIGHT_VERTICAL + "  " + UTF8.LIGHT_VERTICAL_RIGHT + UTF8.LIGHT_HORIZONTAL)
        if not okay : continue

        outblob_data = numpy.zeros((len(ihids),6),'int64')
        parttype = bf.Blob(ptype_path + os.sep + fn).Read()
        for qr in pquerys:
            ihid,start,count = qr
            part_block = parttype[start:start+count]
            ptype,pcount = numpy.unique(part_block,return_counts=True)

            # Rockstar types to Mpgadget type conversion
            rock_to_mpg = {0:1,1:0,2:4,3:5}
            ptype = numpy.array([rock_to_mpg[t] for t in ptype])

            for ptype,pcount in zip(ptype,pcount):
                outblob_data[ihid,ptype] = pcount

        outcolumn_data.append(outblob_data)

    
    print(UTF8.LIGHT_VERTICAL_RIGHT + UTF8.LIGHT_HORIZONTAL + " Dumping Data - ",end="")
    bf.Column(snap_path+os.sep+"RKSHalos/PP_LengthByType").Write(outcolumn_data,"Overwrite")
    print(ANSI.FG_GREEN + "SUCCESS" + ANSI.RESET)

    _log_finish()



def _Mass_by_Type(snap_path:str):
    _log_start("PP_MassByType",snap_path)
    ihid_path   = snap_path + os.sep + "RKSHalos/InternalHaloID"
    pquery_path = snap_path + os.sep + "RKSHalos/PP_ParticleBlock"
    ptype_path  = snap_path + os.sep + "RKSParticles/Type"
    pmass_path  = snap_path + os.sep + "RKSParticles/Mass"

    header = bf.Header(ihid_path + os.sep + "header").Read()
    filenames = [("{:X}".format(i)).upper().rjust(6,'0') for i in range(header["NFILE"])]

    outcolumn_data = []
    for n,fn in enumerate(filenames):
        print(UTF8.LIGHT_VERTICAL_RIGHT+UTF8.LIGHT_HORIZONTAL+" BLOB",fn)
        ihids = bf.Blob(ihid_path + os.sep + fn).Read()
        pquerys = bf.Blob(pquery_path + os.sep + fn).Read()

        okay = len(ihids)==len(pquerys)
        _log_cross_check("Check 1",okay,UTF8.LIGHT_VERTICAL + "  " + UTF8.LIGHT_VERTICAL_RIGHT + UTF8.LIGHT_HORIZONTAL)
        if not okay : continue

        outblob_data = numpy.zeros((len(ihids),6))
        parttype = bf.Blob(ptype_path + os.sep + fn).Read()
        partmass = bf.Blob(pmass_path + os.sep + fn).Read()
        for qr in pquerys:
            ihid,start,count = qr
            parttype_block = parttype[start:start+count]
            partmass_block = partmass[start:start+count]
            
            dm_mass = numpy.sum(partmass_block[parttype_block==0])           
            gas_mass = numpy.sum(partmass_block[parttype_block==1])           
            star_mass = numpy.sum(partmass_block[parttype_block==2])           
            bh_mass = numpy.sum(partmass_block[parttype_block==3])

            outblob_data[ihid,[0,1,4,5]] = numpy.array([gas_mass,dm_mass,star_mass,bh_mass])/1e10


        outcolumn_data.append(outblob_data)

    print(UTF8.LIGHT_VERTICAL_RIGHT + UTF8.LIGHT_HORIZONTAL + " Dumping Data - ",end="")
    bf.Column(snap_path+os.sep+"RKSHalos/PP_MassByType").Write(outcolumn_data,"Overwrite")
    print(ANSI.FG_GREEN + "SUCCESS" + ANSI.RESET)

    _log_finish()



def _Length_And_Mass_By_Type_With_Sub(snap_path):
    _log_start("PP_LengthByTypeWithSub & PP_MassByTypeWithSub",snap_path)

    ihid_path = snap_path + os.sep + "RKSHalos/InternalHaloID"
    lbt_path = snap_path + os.sep + "RKSHalos/PP_LengthByType"
    mbt_path = snap_path + os.sep + "RKSHalos/PP_MassByType"

    qr = hq.RSGQuery(snap_path)
    header = bf.Header(ihid_path + os.sep + "header").Read()
    filenames = [("{:X}".format(i)).upper().rjust(6,'0') for i in range(header["NFILE"])]

    outcolumn_length = []
    outcolumn_mass = []
    for fn in filenames:
        print(UTF8.LIGHT_VERTICAL_RIGHT+UTF8.LIGHT_HORIZONTAL+" BLOB",fn)
        blob_ihid = bf.Blob(ihid_path + os.sep + fn).Read()
        blob_lbt = bf.Blob(lbt_path + os.sep + fn).Read()
        blob_mbt = bf.Blob(mbt_path + os.sep + fn).Read()

        desc_with_ihid = list(map(lambda ihid:[ihid] + list(qr.get_descendant_halos_of(ihid,fn)),blob_ihid))
        
        outblob_length = numpy.zeros((len(blob_ihid),6),dtype='int64')
        outblob_mass = numpy.zeros((len(blob_ihid),6))
        for ihid,desc in zip(blob_ihid,desc_with_ihid):
            outblob_length[ihid]=numpy.sum(blob_lbt[desc],axis=0)
            outblob_mass[ihid]=numpy.sum(blob_mbt[desc],axis=0)
        
        outcolumn_length.append(outblob_length)
        outcolumn_mass.append(outblob_mass)
    
    print(UTF8.LIGHT_VERTICAL_RIGHT + UTF8.LIGHT_HORIZONTAL + " Dumping Data Length - ",end="")
    bf.Column(snap_path+os.sep+"RKSHalos/PP_LengthByTypeWithSub").Write(outcolumn_length,"Overwrite")
    print(ANSI.FG_GREEN + "SUCCESS" + ANSI.RESET)

    print(UTF8.LIGHT_VERTICAL_RIGHT + UTF8.LIGHT_HORIZONTAL + " Dumping Data Mass - ",end="")
    bf.Column(snap_path+os.sep+"RKSHalos/PP_MassByTypeWithSub").Write(outcolumn_mass,"Overwrite")
    print(ANSI.FG_GREEN + "SUCCESS" + ANSI.RESET)

    _log_finish()


def _Mass_By_Type_With_Sub_In_Rvir(snap_path):
    _log_start("PP_MassByTypeWithSubInRvir",snap_path)

    # Halo ID Dict
    ihid_path   = snap_path + os.sep + "RKSHalos/InternalHaloID"
    rvir_path   = snap_path + os.sep + "RKSHalos/VirialRadius"
    hpos_path   = snap_path + os.sep + "RKSHalos/Position"
    
    
    pquery_path = snap_path + os.sep + "RKSHalos/PP_ParticleBlock"
    ptype_path  = snap_path + os.sep + "RKSParticles/Type"
    pmass_path  = snap_path + os.sep + "RKSParticles/Mass"
    ppos_path   = snap_path + os.sep + "RKSParticles/Position"

    






    # qr = hq.RSGQuery(snap_path)
    # header = bf.Header(ihid_path + os.sep + "header").Read()
    # filenames = [("{:X}".format(i)).upper().rjust(6,'0') for i in range(header["NFILE"])]

    # outcolumn_data = []
    # for n,fn in enumerate(filenames):
    #     print(UTF8.LIGHT_VERTICAL_RIGHT+UTF8.LIGHT_HORIZONTAL+" BLOB",fn)
    #     ihids = bf.Blob(ihid_path + os.sep + fn).Read()
    #     pquerys = bf.Blob(pquery_path + os.sep + fn).Read()        
    #     rvir = bf.Blob(rvir_path + os.sep + fn).Read()        
    #     hpos = bf.Blob(hpos_path + os.sep + fn).Read()        

    #     okay1 = len(ihids)==len(pquerys)
    #     okay2 = len(ihids)==len(rvir)
    #     okay3 = len(ihids)==len(hpos)
    #     okay  = okay1 * okay2 * okay3
    #     _log_cross_check("Check 1",okay,UTF8.LIGHT_VERTICAL + "  " + UTF8.LIGHT_VERTICAL_RIGHT + UTF8.LIGHT_HORIZONTAL)
    #     if not okay : continue

    #     outblob_data = numpy.zeros((len(ihids),6))
    #     parttype = bf.Blob(ptype_path + os.sep + fn).Read()
    #     partmass = bf.Blob(pmass_path + os.sep + fn).Read()
    #     partpos  = bf.Blob(ppos_path + os.sep +fn).Read()

    #     desc_with_ihid = list(map(lambda ihid:[ihid] + list(qr.get_descendant_halos_of(ihid,fn)),ihids))
    #     for ihid,desc,rv,hp in zip(ihids,desc_with_ihid,rvir,hpos):
    #         chunk_pos,chunk_mass,chunk_type = qr.get_child_particle_position_and_mass_and_type(desc,fn)

    #         mask = numpy.linalg.norm(chunk_pos - numpy.tile(hp,(len(chunk_pos),1)),axis=1)<rv
    #         chunk_mass = chunk_mass[mask]
    #         chunk_type = chunk_type[mask]

    #         dm_mass = numpy.sum(chunk_mass[chunk_type==0])           
    #         gas_mass = numpy.sum(chunk_mass[chunk_type==1])           
    #         star_mass = numpy.sum(chunk_mass[chunk_type==2])           
    #         bh_mass = numpy.sum(chunk_mass[chunk_type==3])

    #         outblob_data[ihid,[0,1,4,5]] += numpy.array([gas_mass,dm_mass,star_mass,bh_mass])/1e10    

    #     outcolumn_data.append(outblob_data)

    # print(UTF8.LIGHT_VERTICAL_RIGHT + UTF8.LIGHT_HORIZONTAL + " Dumping Data - ",end="")
    # bf.Column(snap_path+os.sep+"RKSHalos/PP_MassByTypeWithSubInRvir").Write(outcolumn_data,"Overwrite")
    # print(ANSI.FG_GREEN + "SUCCESS" + ANSI.RESET)

    _log_finish()

if __name__=="__main__":
    # _post_process_snap("/mnt/home/student/cranit/Work/test_para_rock/OUT_L10N64/RSG_017")
    # _Process_Headers("/mnt/home/student/cranit/Work/test_para_rock/OUT_L10N64/RSG_000")
    # _DumpParticleBlock("/mnt/home/student/cranit/Work/test_para_rock/OUT_L10N64/RSG_000")
    # _Length_by_Type("/mnt/home/student/cranit/Work/test_para_rock/OUT_L10N64/RSG_017")
    # _Mass_by_Type("/mnt/home/student/cranit/Work/test_para_rock/OUT_L10N64/RSG_017")
    # _Length_By_Type_With_Sub("/mnt/home/student/cranit/Work/test_para_rock/OUT_L10N64/RSG_017")
    # _Mass_By_Type_With_Sub_In_Rvir("/mnt/home/student/cranit/RANIT/Work/test_para_rock/OUT_L50N640z0/RSG_171")
    pass