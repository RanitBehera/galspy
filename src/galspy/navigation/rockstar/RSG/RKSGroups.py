import os
from galspec.navigation.base.Folder import _Folder
from galspec.IO.Field import _Field

class _RKSGroups(_Folder):
    def __init__(self,path):
        super().__init__(path)

        self.HaloID             = _Field(os.path.join(self.path,"HaloID"))
        self.InternalHaloID     = _Field(os.path.join(self.path,"InternalHaloID"))
        self.Length             = _Field(os.path.join(self.path,"Length"))
        self.VirialMass         = _Field(os.path.join(self.path,"VirialMass"))
        self.VirialRadius       = _Field(os.path.join(self.path,"VirialRadius"))
        self.Position           = _Field(os.path.join(self.path,"Position"))
        self.Velocity           = _Field(os.path.join(self.path,"Velocity"))

        # Post Processed
        self.LengthByTypeWC         = _Field(os.path.join(self.path,"LengthByTypeWC"))
        self.LengthByTypeInRvirWC   = _Field(os.path.join(self.path,"LengthByTypeInRvirWC"))
        self.MassByTypeInRvirWC     = _Field(os.path.join(self.path,"MassByTypeInRvirWC"))
        self.StarFormationRate      = _Field(os.path.join(self.path,"StarFormationRate"))