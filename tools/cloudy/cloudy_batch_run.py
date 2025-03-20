import numpy
import subprocess
import time
import os
import pickle
import shutil
from concurrent.futures import ThreadPoolExecutor

# Temporary directory where cloudy will dump data
# before this scripts gathers spectrum to dictionary
TEMPDIR="/mnt/home/student/cranit/RANIT/Repo/galspy/study/cloudy/cloudy_cache_temp"


STELLAR_FILE = "/mnt/home/student/cranit/RANIT/Repo/galspy/cache/spectra/array/stellar_kroupa300bh_bin.specs"



# ===================== CLOUDY BATCH RUN
def RunCloudyInstance(specindex:int):
    if specindex==0:return

    while not os.path.exists(TEMPDIR+os.sep+f"spec{specindex}.in"):
        print("[ WAITING ]",f"for spec{specindex}.in",flush=True)
        time.sleep(1)
    
    while not os.path.exists(TEMPDIR+os.sep+"LinesList.dat"):
        print("[ WAITING ]","for LinesList.dat",flush=True)
        time.sleep(1)

    print("[ STRATING ]",f"spec{specindex}",flush=True)

    os.chdir(TEMPDIR)
    s=time.time()
    result = subprocess.run(["cloudy","-r",f"spec{specindex}"],
            stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    e=time.time()

    print(f"[ FINISHED in {round(e-s)}s]",f"spec{specindex}",flush=True)

    if result.stdout:print(f"[ spec{specindex} ] >",result.stdout.decode())
    if result.stderr:print(f"[ spec{specindex} ] >",result.stderr.decode())



def _CreateNebularCache(stellar_filepath:str):
    # takes a stellar array cache file
    filepath=stellar_filepath

    print("Reading Input Spectrums ... ",end="")
    with open(filepath,"rb") as fp:
        stellar_specs = pickle.load(fp)
    wl=stellar_specs[0]
    print("Done")

    print("Evaluating Normalisation ... ",end="")
    LAM_NORM=2  #in Angstrom
    NORM = stellar_specs[:,LAM_NORM-1]
    NORM[0]=0   #Skip wavelength slice
    NORM = NORM * ((LAM_NORM**2)*(3.846e33)/(3e18))
    NORM[1:] = numpy.round(numpy.log10(NORM[1:]),3)
    print("Done")

    print("Reading Cloudy Input Script ... ",end="")
    INP_SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__)) +os.sep + "cloudy.in"
    with open(INP_SCRIPT_PATH,'r') as fp:
        CLOUDY_TEMPLATE_SCRIPT = fp.read()
    print("Done")
    
    
    print("Creating spectrums and input scripts ... ")
    for i,spec in enumerate(stellar_specs):
        if i==0:continue
        print(f"\r{i}/{len(stellar_specs)-1}",end='',flush=True)

        filepath = TEMPDIR+os.sep+f"spec{i}.sed"

        if not os.path.exists(filepath):
            numpy.savetxt(filepath,numpy.column_stack((wl[0],spec[0])),fmt="%d %.7E",
                        newline=" Flambda units Angstrom extrapolate\n")
            with open(filepath,'a') as fp:
                numpy.savetxt(fp,numpy.column_stack((wl[1:],spec[1:])),fmt="%d %.7E")

        INP = CLOUDY_TEMPLATE_SCRIPT
        INP=INP.replace("$__SEDFN__",f"spec{i}.sed")
        INP=INP.replace("$__LNORM__",str(NORM[i]))
        INP=INP.replace("$__FN__",f"spec{i}")

        with open(TEMPDIR+os.sep+f"spec{i}.in","w") as fp:
            fp.write(INP)
    print("")

    print("Copying LinesList.dat file ... ",end="")
    linelist_file = os.path.dirname(os.path.abspath(__file__)) +os.sep + "LinesList.dat"
    shutil.copy(linelist_file,TEMPDIR)
    print("Done")

    print("Running Batch Cloudy ... ")
    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        executor.map(RunCloudyInstance, range(len(stellar_specs)))

    print("Gathering output spectras ... ")
    inspec_list = []
    outspec_list = []
    for i in range(len(stellar_specs)):
        if i==0:continue
        print(f"\r{i} / {len(stellar_specs)-1}",end='')
        con_data=numpy.loadtxt(TEMPDIR+os.sep+f"spec{i}.con",delimiter='\t',usecols=[0,1,3])
        freq,incident,diffout = con_data.T
        incident=incident/freq
        diffout=diffout/freq

        if i==1:
            inspec_list.append(freq)
            outspec_list.append(freq)

        inspec_list.append(incident)
        outspec_list.append(diffout)

    inspec_list=numpy.array(inspec_list)
    outspec_list=numpy.array(outspec_list)
    print("")

    print("Converting to Solar Luminsoity Units ... ",end="")
    LSOL=3.83e33
    inspec_list[1:,:]=inspec_list[1:,:]/LSOL
    outspec_list[1:,:]=outspec_list[1:,:]/LSOL
    print("Done")

    print("Reversing Wavelength Order ... ",end="")
    inspec_list=inspec_list[:,::-1]
    outspec_list=outspec_list[:,::-1]
    print("Done")


    print("Saving Cache ... ",end="")
    with open(stellar_filepath.replace("stellar","nebular_in"),'wb') as fp:
        pickle.dump(inspec_list,fp)

    with open(stellar_filepath.replace("stellar","nebular_out"),'wb') as fp:
        pickle.dump(outspec_list,fp)
    print("Done")
    


if __name__=="__main__":
    _CreateNebularCache(STELLAR_FILE)
