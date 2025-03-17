from typing import Literal
from galspy.Utility.Visualization import Cube3D
from galspy.Utility.MassFunction import MassFunction, MassFunctionLiterature, LMF_OPTIONS
from galspy.Spectra.Utility import LuminosityFunction

# The purpose of this class is to
# easily access the existing functions in other areas of utility.
# So match the signatures.
# No extra logic should be written here.
class _Utility:
    def __init__(self):
        pass

    def MassFunction(self,mass_list,box_size,LogBinStep=0.5):
        return MassFunction(mass_list,box_size,LogBinStep)
    
    def MassFunctionLiterature(self,model_name:LMF_OPTIONS,cosmology:dict,redshift,mass_range,output:Literal["dn/dlnM","(M2/rho0)*(dn/dm)"]):
        return MassFunctionLiterature(model_name,cosmology,redshift,mass_range,output)
    
    def LumimosityFunction(self,MUVAB,VOLUME,LogBinStep):
        return LuminosityFunction(MUVAB,VOLUME,LogBinStep)


