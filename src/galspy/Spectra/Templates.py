import os
import hoki.load
import numpy
import pickle
from typing import Literal


class BPASS:
    BPASS_DATADIR = "/mnt/home/student/cranit/Data/BPASS/BPASSv2.2.1_release-07-18-Tuatara/"
    BPASS_VERSION = "2.2.1"

    AVAIL_MODEL = Literal[
        "SALPETER_UPTO_100M",
        "KROUPA_UPTO_100M",
        "KROUPA_UPTO_300M",
        "KROUPA_UPTO_100M_TOP_HEAVY",
        "KROUPA_UPTO_300M_TOP_HEAVY",
        "KROUPA_UPTO_100M_BOTTOM_HEAVY",
        "KROUPA_UPTO_300M_BOTTOM_HEAVY",
        "CHABRIER_UPTO_100M",
        "CHABRIER_UPTO_300M"
        ]
    
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
            raise ValueError("BPASS ERROR : Unknown 'IMF' Option.") 
        if self.system not in ["Single","Binary"]:
            raise ValueError("BPASS ERROR : Unknown 'System' Option.") 
        if self.metallicity not in BPASS.AVAIL_METALLICITY:
            raise ValueError("BPASS ERROR : Unknown 'Metallicity' Option.") 

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

    def _get_filename(self,imf:BPASS.AVAIL_MODEL,system:Literal["Single","Binary"],prefix:str=""):
        filename=f"{prefix}_{Templates._model_name_to_filename[imf]}_{system.lower()[0:3]}.specs"
        return filename

    def _CreateStellarCache(self,imf,system):
        pass
    
    def _CreateNebularCache(self,imf,system):
        pass



    def GetStellarTemplates(self,imf:BPASS.AVAIL_MODEL,system:Literal["Single","Binary"]):
        filename = self._get_filename(imf,system,"stellar")
        filepath = Templates.CACHE_DIR + os.sep + filename

        if not os.path.exists(filepath):
            print(f"Cache not found.\nCreating Cache : {filename}")
            self._CreateStellarCache(imf,system)
        
        print(f"Using Cache : {filename}")
        with open(filepath,"rb") as fp:
            return pickle.load(fp)
        




    def GetNebularTemplates(self,imf:BPASS.AVAIL_MODEL,system:Literal["Single","Binary"]):
        filename = self._get_filename(imf,system,"nebular")
        filepath = Templates.CACHE_DIR + os.sep + filename
        
        if not os.path.exists(filepath):
            print(f"Cache not found.\nCreating Cache : {filename}")
            self._CreateNebularCache(imf,system)
        
        print(f"Using Cache : {filename}")
        with open(filepath,"rb") as fp:
            return pickle.load(fp)



if __name__=="__main__":
    tmp=Templates()
    tmp.GetStellarTemplates("CHABRIER_UPTO_300M","Binary")