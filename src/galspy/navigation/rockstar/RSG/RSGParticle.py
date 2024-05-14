import os
from galspec.navigation.base.Folder import _Folder
from galspec.IO.Field import _Field

class _RSGParticle(_Folder):
    def __init__(self,path):
        super().__init__(path)

        self.HaloID                     = _Field(os.path.join(self.path,"HaloID"))
        self.InternalHaloID             = _Field(os.path.join(self.path,"InternalHaloID"))
        self.AssignedInternalHaloID     = _Field(os.path.join(self.path,"AssignedInternalHaloID"))
        self.ID                         = _Field(os.path.join(self.path,"ID"))
        self.Mass                       = _Field(os.path.join(self.path,"Mass"))
        self.Position                   = _Field(os.path.join(self.path,"Position"))
        self.Velocity                   = _Field(os.path.join(self.path,"Velocity"))