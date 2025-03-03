import os, shutil
import time
import hoki.load
import numpy
import pickle
from typing import Literal
import subprocess
from concurrent.futures import ThreadPoolExecutor



class BPASS:
    BPASS_DATADIR = "/mnt/home/student/cranit/Data/BPASS/BPASSv2.2.1_release-07-18-Tuatara/"
    BPASS_VERSION = "2.2.1"

    AVAIL_MODEL_HINT = Literal["SALPETER_UPTO_100M","KROUPA_UPTO_100M","KROUPA_UPTO_300M","KROUPA_UPTO_100M_TOP_HEAVY","KROUPA_UPTO_300M_TOP_HEAVY","KROUPA_UPTO_100M_BOTTOM_HEAVY","KROUPA_UPTO_300M_BOTTOM_HEAVY","CHABRIER_UPTO_100M","CHABRIER_UPTO_300M"]
    # Because you can't itterate over a Literal hint, duplicate list is needed
    AVAIL_MODEL = ["SALPETER_UPTO_100M","KROUPA_UPTO_100M","KROUPA_UPTO_300M","KROUPA_UPTO_100M_TOP_HEAVY","KROUPA_UPTO_300M_TOP_HEAVY","KROUPA_UPTO_100M_BOTTOM_HEAVY","KROUPA_UPTO_300M_BOTTOM_HEAVY","CHABRIER_UPTO_100M","CHABRIER_UPTO_300M"]
    
    AVAIL_METALLICITY = [0.00001,0.0001,
                        0.001,0.002,0.003,0.004,0.006,0.008,
                        0.010,0.014,0.020,0.030,0.040]

    _model_name_imf_string = {
        "SALPETER_UPTO_100M":"135all_100",
        "KROUPA_UPTO_100M":"135_100",
        "KROUPA_UPTO_300M":"135_300",
        "KROUPA_UPTO_100M_TOP_HEAVY":"100_100",
        "KROUPA_UPTO_300M_TOP_HEAVY":"100_300",
        "KROUPA_UPTO_100M_BOTTOM_HEAVY":"170_100",
        "KROUPA_UPTO_300M_BOTTOM_HEAVY":"170_300",
        "CHABRIER_UPTO_100M":"_chab100",
        "CHABRIER_UPTO_300M":"_chab300"
    }

    def __init__(self,imf:str,system:Literal["Single","Binary"],metallicity):
        self.datadir        = f"{BPASS.BPASS_DATADIR}"
        self.version        = f"{BPASS.BPASS_VERSION}"
        self.imf            = imf
        self.system         = system
        self.metallicity    = metallicity

        self._validate_options()
    
    def _validate_options(self):
        if self.imf not in BPASS.AVAIL_MODEL:
            raise ValueError(f"BPASS ERROR : Unknown 'IMF' Option : {self.imf}") 
        if self.system not in ["Single","Binary"]:
            raise ValueError(f"BPASS ERROR : Unknown 'System' Option : {self.system}") 
        if self.metallicity not in BPASS.AVAIL_METALLICITY:
            raise ValueError(f"BPASS ERROR : Unknown 'Metallicity' Option : {self.metallicity}") 

    def _get_filepath(self,quantity:Literal["colours","hrs","ionizing","lick","mlratio","numbers","spectra","starmass","supernova","yields"]):
        imf_str = f"imf{BPASS._model_name_imf_string[self.imf]}"
        if numpy.round(self.metallicity,5)==0.00001:metal_str="em5"
        elif numpy.round(self.metallicity,4)==0.0001:metal_str="em4"
        else:metal_str=str(numpy.round(self.metallicity,3)).split(".")[-1].ljust(3,"0")
    
        filepath = BPASS.BPASS_DATADIR + os.sep
        filepath += f"bpass_v{BPASS.BPASS_VERSION}_{imf_str}" + os.sep
        filepath += f"{quantity}-{self.system.lower()[0:3]}-{imf_str}.z{metal_str}.dat"

        return filepath 


    def GetFlux(self):
        """
        Returns Flux in Solar Luminosity per Angstrom
        """
        specpath = self._get_filepath("spectra")
        spectra = hoki.load.model_output(specpath)
        return spectra





class Templates:
    CACHE_DIR = "/mnt/home/student/cranit/RANIT/Repo/galspy/cache/spectra/array"
    _model_name_to_filename = {
        "SALPETER_UPTO_100M":"salpeter100",
        "KROUPA_UPTO_100M":"kroupa100",
        "KROUPA_UPTO_300M":"kroupa300",
        "KROUPA_UPTO_100M_TOP_HEAVY":"kroupa100th",
        "KROUPA_UPTO_300M_TOP_HEAVY":"kroupa300th",
        "KROUPA_UPTO_100M_BOTTOM_HEAVY":"kroupa100bh",
        "KROUPA_UPTO_300M_BOTTOM_HEAVY":"kroupa300bh",
        "CHABRIER_UPTO_100M":"chabrier100",
        "CHABRIER_UPTO_300M":"chabrier300"
    }

    def __init__(self):
        pass

    def _get_filename(self,imf:BPASS.AVAIL_MODEL_HINT,system:Literal["Single","Binary"],prefix:str=""):
        filename=f"{prefix}_{Templates._model_name_to_filename[imf]}_{system.lower()[0:3]}.specs"
        return filename

    def _CreateStellarCache(self,filepath,imf,system):
        Z_foots=[1e-5,1e-4,1e-3,2e-3,3e-3,4e-3,6e-3,8e-3,1e-2,1.4e-2,2e-2,3e-2,4e-2]
        T_foots = numpy.arange(6,11.1,0.1)
    
        spec_list=numpy.zeros((1+len(Z_foots)*len(T_foots),100000))
        for Z_index,Z in enumerate(Z_foots):
            _BPASS = BPASS(imf,system,Z)
            table=_BPASS.GetFlux().to_numpy()
            lam,aged_flux = table[:,0],table[:,1:].T
            for T_index,T in enumerate(T_foots):
                spec_index=1+(Z_index*len(T_foots)+T_index)
            
                if spec_index==1:spec_list[0]=lam
                spec_list[spec_index]=aged_flux[T_index]

                print(f"\r{spec_index}","/",len(Z_foots)*len(T_foots),end="")

        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath,"wb") as fp: pickle.dump(spec_list,fp)


    def GetStellarTemplates(self,imf:BPASS.AVAIL_MODEL_HINT,system:Literal["Single","Binary"]):
        filename = self._get_filename(imf,system,"stellar")     #< This will use BPASS
        filename = self._get_filename(imf,system,"nebular_in")     #< This will use Cloudy out   - Automate them
        filepath = Templates.CACHE_DIR + os.sep + filename

        if not os.path.exists(filepath):
            print("Cache not found.")
            print(f"Creating Cache : {filename}")
            self._CreateStellarCache(filepath,imf,system)
        
        print(f"Using Cache : {filename}")
        with open(filepath,"rb") as fp:
            return pickle.load(fp)
        

    def GetNebularTemplates(self,imf:BPASS.AVAIL_MODEL_HINT,system:Literal["Single","Binary"],prefix_str:str="out"):
        filename = self._get_filename(imf,system,f"nebular_{prefix_str}")
        filepath = Templates.CACHE_DIR + os.sep + filename
        
        if not os.path.exists(filepath):
            print("Cache not found.")
            print("Go to tools and generate the cache.")
        else:
            print(f"Using Cache : {filename}")
            with open(filepath,"rb") as fp:
                return pickle.load(fp)


    def GetTemplates(self,filepath):
        if not os.path.exists(filepath):
            print("Cache not found.")
        else:
            with open(filepath,"rb") as fp:
                return pickle.load(fp)


# CACHE STAR index from the templates
from astropy.cosmology import FlatLambdaCDM
def map_to_closest(array1, array2):
    # Find the closest value in array1 for each value in array2
    indices = numpy.abs(array2[:, None] - array1).argmin(axis=1)
    return array1[indices]

def GetCachedStarsSpecTemplateIndex(filepath,ids,birthtimes,metallicities,cosmology,snap_redshift):
    if not os.path.exists(filepath):
        print("Template index cache not found ...")
        print("Creating Cache ...")
        age_uni_snap = cosmology.age(snap_redshift).value*1000 #in Myr

        z_sft = (1/birthtimes)-1
        age_uni_sft = cosmology.age(z_sft).value*1000 #in Myr 
        age_star = age_uni_snap-age_uni_sft

        age_star = numpy.clip(age_star,1,None)
        age_star = numpy.round(numpy.log10(age_star)+6,1)


        Z_foots=numpy.array(BPASS.AVAIL_METALLICITY)
        met_stars = map_to_closest(Z_foots,metallicities)
        Z_foots = list(Z_foots)

        T_foots = numpy.arange(6,11.1,0.1)

        Z_ind_map=dict(zip(Z_foots,range(len(Z_foots))))
        T_ind_map=dict(zip(numpy.round(T_foots,1),range(len(T_foots))))

        Z_keys = met_stars
        T_keys = age_star

        Z_index = numpy.array([Z_ind_map.get(key, None) for key in Z_keys])
        T_index = numpy.array([T_ind_map.get(float(f"{key:.1f}"), None) for key in T_keys])

        spec_index = 1+(Z_index*len(T_foots)+T_index)
        id_index_map = dict(zip(ids,spec_index))

        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath,"wb") as fp:
            pickle.dump(id_index_map,fp)

    print(f"Using Template Index Cache : {filepath}")
    with open(filepath,"rb") as fp:
        return pickle.load(fp)




