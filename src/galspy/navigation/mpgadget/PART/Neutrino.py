import os
from galspec.navigation.base.Folder import _Folder
from galspec.IO.Field import _Field

class _Neutrino(_Folder):
    def __init__(self,path):
        super().__init__(path)

        self.GroupID                     = _Field(os.path.join(self.path,"GroupID"))
        self.ID                          = _Field(os.path.join(self.path,"ID"))
        self.Mass                        = _Field(os.path.join(self.path,"Mass"))
        self.Position                    = _Field(os.path.join(self.path,"Position"))
        self.Potential                   = _Field(os.path.join(self.path,"Potential"))
        self.Velocity                    = _Field(os.path.join(self.path,"Velocity"))