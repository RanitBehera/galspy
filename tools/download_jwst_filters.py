import os, requests, tarfile, numpy

NSTEPS = 5

# 1. Create Folder -----------------------
SAVE_DIR = "/mnt/home/student/cranit/RANIT/Repo/galspy/cache/filters"
SUBDIR = "jwst"
SAVE_DIR = os.path.join(SAVE_DIR,SUBDIR)
print(f"1/{NSTEPS}\tCreating sub-folder:\n\t{SAVE_DIR}")
os.makedirs(SAVE_DIR,exist_ok=True)


# 2. Get targip ---------------------------
URL = "https://jwst-docs.stsci.edu/files/97978094/281939693/1/1720022158424/nircam_throughputs_16May2024_v6.tar.gz"
FILEPATH = os.path.join(SAVE_DIR,URL.split('/')[-1])
if os.path.exists(FILEPATH):
    print(f"\n2/{NSTEPS}\tUsing existing tarzip:\n\t{FILEPATH}")
else:
    print(f"\n2/{NSTEPS}\tDownloading tarzip from:\n\t{URL}")
    response = requests.get(URL, stream=True)
    if response.status_code == 200:
        with open(FILEPATH, 'wb') as f:
            f.write(response.raw.read())
    print(f"\tSaved TarZip To:\n\t{FILEPATH}")


# 3. Extract tarzip --------------------------
print(f"\n3/{NSTEPS}\tExtracting tarzip:\n\t{FILEPATH}")
tar = tarfile.open(FILEPATH, "r:gz")
tar.extractall(SAVE_DIR)
tar.close()


# 4. Creating gitignore file --------------------------
print(f"\n4/{NSTEPS}\tCreating gitignore file in:\n\t{SAVE_DIR}")
with open(SAVE_DIR + os.sep + ".gitignore","w") as fp:
    fp.write(URL.split(os.sep)[-1])
    fp.write("\nnircam_throughputs")

# 5. Copy files and process to bagfile format
print(f"\n5/{NSTEPS}\tProcessing filters for BAGPIPES usage and Copying to:\n\t{SAVE_DIR}")

SEARCH_DIR = os.path.join(SAVE_DIR,"nircam_throughputs/mean_throughputs")
FILTERS = [f for f in os.listdir(SEARCH_DIR)
           if os.path.isfile(os.path.join(SEARCH_DIR,f)) and
           f.endswith("mean_system_throughput.txt") and
           not f.startswith('.')] 

for filt in FILTERS:
    print(f"\t\t{filt.ljust(36)}  >  ",end="")
    FILEPATH = os.path.join(SEARCH_DIR,filt)
    microns,thputs = numpy.loadtxt(FILEPATH,skiprows=1).T
    angstrom = microns*1e4
    
    outfile_path = os.path.join(SAVE_DIR,filt.split('_')[0])
    numpy.savetxt(outfile_path,numpy.column_stack((angstrom,thputs)),
                  header=f"Angstrom Throughputs")

    print(filt.split('_')[0])


print("\nFinished")













