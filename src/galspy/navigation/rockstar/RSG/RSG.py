import os,numpy
from galspec.navigation.base.Folder import _Folder
from galspec.navigation.MPGADGET.RSG.RSGParticle import _RSGParticle
from galspec.navigation.MPGADGET.RSG.RKSGroups import _RKSGroups
from galspec.navigation.MPGADGET.RSG.RSGAttribute import _RSGAttribute

class _RSG(_Folder):
    def __init__(self,path):
        super().__init__(path)

        self.Gas         = _RSGParticle(os.path.join(self.path,"0"))
        self.DarkMatter  = _RSGParticle(os.path.join(self.path,"1"))
        self.Neutrino    = _RSGParticle(os.path.join(self.path,"2"))
        self.Star        = _RSGParticle(os.path.join(self.path,"4"))
        self.BlackHole   = _RSGParticle(os.path.join(self.path,"5"))
        self.RKSGroups   = _RKSGroups(os.path.join(self.path,"RKSGroups"))

        self.Attribute   = _RSGAttribute(self.path + "/Header/attr-v2")


