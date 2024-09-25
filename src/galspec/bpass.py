import hoki.load
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import Literal
import os
import hoki


# INTERNAL
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

_model_name_imf_sting = {
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

AVAIL_METALLICITY = [0.00001,0.0001,
                     0.001,0.002,0.003,0.004,0.006,0.008,
                     0.010,0.020,0.030,0.040]

# TODO: functions for left and right nearest metallicity neighbour



BPASS_DIR = "/mnt/home/student/cranit/Data/BPASS/BPASSv2.2.1_release-07-18-Tuatara/"
BPASS_VERSION = "2.2.1"


# Intermidiate Interface
class _Spectra:
    def __init__(self,filepath) -> None:
        self.filepath = filepath
    
    def GetFlux(self,wavelength_lower:int=1,wavelength_higher:int=100000):
        spectra = hoki.load.model_output(self.filepath)
        if (not wavelength_lower==1) or (not wavelength_higher==100000):
            spectra_masked = spectra[(spectra.WL>=wavelength_lower)&(spectra.WL<=wavelength_higher)]
        return spectra_masked




class _Supernova:
    def __init__(self,filepath) -> None:
        self.filepath = filepath





# EXTERNAL INTERFACE
class BPASS:
    def __init__(self,
                 imf:AVAIL_MODEL,
                 system:Literal["Single","Binary"],
                 metallicity
                ) -> None:
        self.imf            = imf
        self.system         = system
        self._set_metallicity(metallicity)

        self.Spectra        = _Spectra(self._get_file_path("spectra"))
        self.Supernova = None
        
    def _set_metallicity(self,metallicity):
        self.metallicity    = metallicity
        # This will not be useful for interpolation
        if self.metallicity not in AVAIL_METALLICITY:
            avail_Z     = np.array(AVAIL_METALLICITY)
            diff        = np.abs(avail_Z-self.metallicity)
            min_diff    = np.min(diff)
            closest     = avail_Z[np.where(diff==min_diff)]
            self.metallicity    = closest[0]
        # print(self.metallicity)
    
    def _get_file_path(self,quantity:Literal["colours","hrs","ionizing","lick","mlratio","numbers","spectra","starmass","supernova","yields"]):
        imf_str = f"imf{_model_name_imf_sting[self.imf]}"
        if np.round(self.metallicity,5)==0.00001:metal_str="em5"
        elif np.round(self.metallicity,4)==0.0001:metal_str="em4"
        else:metal_str=str(np.round(self.metallicity,3)).split(".")[-1].ljust(3,"0")
    
        filepath = BPASS_DIR + os.sep
        filepath += f"bpass_v{BPASS_VERSION}_{imf_str}" + os.sep
        filepath += f"{quantity}-{self.system.lower()[0:3]}-{imf_str}.z{metal_str}.dat"

        return filepath

    

    # def GetColours(self,metallicity):
    #     self._set_metallicity(metallicity)

    # def GetHR(self,metallicity):
    #     self._set_metallicity(metallicity)

    # def GetInput(self,metallicity):
    #     self._set_metallicity(metallicity)

    # def GetIonizing(self,metallicity):
    #     self._set_metallicity(metallicity)

    # def GetLick(self,metallicity):
    #     self._set_metallicity(metallicity)

    # def GetMassToLightRatio(self,metallicity):
    #     self._set_metallicity(metallicity)

    # def GetNumbers(self,metallicity):
    #     self._set_metallicity(metallicity)


    # def GetStarMass(self,metallicity):
    #     self._set_metallicity(metallicity)

    # def GetSupernova(self,metallicity):
    #     self._set_metallicity(metallicity)

    # def GetYields(self,metallicity):
    #     self._set_metallicity(metallicity)
