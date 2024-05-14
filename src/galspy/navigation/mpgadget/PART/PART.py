import os
from galspec.navigation.base.Folder import _Folder
from galspec.navigation.MPGADGET.PART.Gas import _Gas
from galspec.navigation.MPGADGET.PART.DarkMatter import _DarkMatter
from galspec.navigation.MPGADGET.PART.Neutrino import _Neutrino
from galspec.navigation.MPGADGET.PART.Star import _Star
from galspec.navigation.MPGADGET.PART.Blackhole import _BlackHole
from galspec.navigation.MPGADGET.PART.PARTAttribute import _PARTAttribute

class _PART(_Folder):
    def __init__(self,path):
        super().__init__(path)


        self.Gas        = _Gas(os.path.join(self.path,"0"))
        self.DarkMatter = _DarkMatter(os.path.join(self.path,"1"))
        self.Neutrino   = _Neutrino(os.path.join(self.path,"2"))
        self.Star       = _Star(os.path.join(self.path,"4"))
        self.BlackHole  = _BlackHole(os.path.join(self.path,"5"))

        self.Attribute     = _PARTAttribute(self.path + os.sep + "Header" + os.sep + "attr-v2")

    # def ReadAttribute(self):
    #     return mp.ReadAttribute(self)
    
    # def OutputRockstarHDF5(self,savepath,filename:str="",include_gas:bool=False,include_dm:bool=True,include_star:bool=False,include_bh:bool=False):
    #     if filename=="":filename="PART_"+'{:03}'.format(self.snap_num)+".hdf5"
    #     if not filename[-5:]==".hdf5":filename += ".hdf5"
    #     if not savepath[-1]==os.sep:savepath += os.sep
    #     filepath=savepath+filename
    #     mp.OutputRockstarHDF5(self,filepath,include_gas,include_dm,include_star,include_bh)
    #     return filepath

    # def OutputRockstarConfig(self,filename:str):
    #     pass
        
