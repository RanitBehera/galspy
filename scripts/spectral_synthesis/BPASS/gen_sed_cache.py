from galspec.bpass import BPASSCache
import os
import numpy

# Mimic BPASS for now
CLOUDY_OUTDIR = "/mnt/home/student/cranit/RANIT/Repo/galspy/study/cloudy/bpass_sed"
CACHE_FILEPATH = "/mnt/home/student/cranit/RANIT/Repo/galspy/cache/cloudy_chab_300M.ch"

def Cache(filepath,overwrite:bool=True):
    if os.path.isfile(filepath) and not overwrite:
        print("Using existing cache: \""+filepath +"\"")
        return
    
    Z_foots=[1e-5,1e-4,1e-3,2e-3,3e-3,4e-3,6e-3,8e-3,1e-2,1.4e-2,2e-2,3e-2,4e-2]
    T_foots = numpy.arange(6,11.1,0.1)

    Z_KEYS = [f"{zf:.5f}".rstrip('0') for zf in Z_foots]
    T_KEYS = [str(numpy.round(tf,1)) for tf in T_foots]
        
    CACHE_METALLICITY_DICT = {"Z_KEYS":Z_KEYS,"T_KEYS":T_KEYS}
    for i,Z in enumerate(Z_foots):
        print(" - ",i+1,"/",len(Z_foots),flush=True)

            _BPASS = BPASS("CHABRIER_UPTO_300M","Binary",Z)
            table=_BPASS.Spectra.GetFlux().to_numpy()
            lam,aged_flux = table[:,0],table[:,1:].T

            CACHE_AGE_DICT = {"WL":lam}
            for j,age in enumerate(T_foots):
                CACHE_AGE_DICT[T_KEYS[j]] = aged_flux[j]

            CACHE_METALLICITY_DICT[Z_KEYS[i]] = CACHE_AGE_DICT

    print("Saving Pickle ...",flush=True)
    with open(self.filepath,"wb") as fp: pickle.dump(CACHE_METALLICITY_DICT,fp)

    print(f"Saved as \"{self.filepath}\"")













# class CloudyCache:
#     def __init__(self,filepath:str) -> None:
#         self.filepath=filepath

#     def Cache(self,overwrite=False):
#         if os.path.isfile(self.filepath) and not overwrite:
#             print("Using existing cache: \""+self.filepath +"\"")
#             return
        
#         print("Creating Cache ...")
#         Z_foots=[1e-5,1e-4,1e-3,2e-3,3e-3,4e-3,6e-3,8e-3,1e-2,1.4e-2,2e-2,3e-2,4e-2]
#         T_foots = numpy.arange(6,11.1,0.1)

#         Z_KEYS = [f"{zf:.5f}".rstrip('0') for zf in Z_foots]
#         T_KEYS = [str(numpy.round(tf,1)) for tf in T_foots]
        
#         CACHE_METALLICITY_DICT = {"Z_KEYS":Z_KEYS,"T_KEYS":T_KEYS}
#         for i,Z in enumerate(Z_foots):
#             print(" - ",i+1,"/",len(Z_foots),flush=True)

#             _BPASS = BPASS("CHABRIER_UPTO_300M","Binary",Z)
#             table=_BPASS.Spectra.GetFlux().to_numpy()
#             lam,aged_flux = table[:,0],table[:,1:].T

#             CACHE_AGE_DICT = {"WL":lam}
#             for j,age in enumerate(T_foots):
#                 CACHE_AGE_DICT[T_KEYS[j]] = aged_flux[j]

#             CACHE_METALLICITY_DICT[Z_KEYS[i]] = CACHE_AGE_DICT

#         print("Saving Pickle ...",flush=True)
#         with open(self.filepath,"wb") as fp: pickle.dump(CACHE_METALLICITY_DICT,fp)

#         print(f"Saved as \"{self.filepath}\"")

#     def Read(self):
#         self.Cache(False)
#         with open(self.filepath,"rb") as fp:
#             cache = pickle.load(fp)
#         return cache