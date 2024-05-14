import os
from galspec.navigation.base.Folder import _Folder
from galspec.navigation.MPGADGET.PART.Gas import _Gas
from galspec.navigation.MPGADGET.PART.DarkMatter import _DarkMatter
from galspec.navigation.MPGADGET.PART.Neutrino import _Neutrino
from galspec.navigation.MPGADGET.PART.Star import _Star
from galspec.navigation.MPGADGET.PART.Blackhole import _BlackHole
from galspec.navigation.MPGADGET.PIG.FOFGroups import _FOFGroups

class _PIG(_Folder):
    def __init__(self,path):
        super().__init__(path)


        self.Gas        = _Gas(os.path.join(self.path,"0"))
        self.DarkMatter = _DarkMatter(os.path.join(self.path,"1"))
        self.Neutrino   = _Neutrino(os.path.join(self.path,"2"))
        self.Star       = _Star(os.path.join(self.path,"4"))
        self.BlackHole  = _BlackHole(os.path.join(self.path,"5"))
        self.FOFGroups  = _FOFGroups(os.path.join(self.path,"FOFGroups"))

    # def ReadAttribute(self):
    #     return mp.ReadAttribute(self)