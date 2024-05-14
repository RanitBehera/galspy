import os
from galspec.navigation.base.Folder import _Folder
from galspec.IO.Field import _Field

class _BlackHole(_Folder):
    def __init__(self,path):
        super().__init__(path)

        self.BlackholeAccretionRate      = _Field(os.path.join(self.path,"BlackholeAccretionRate"))
        self.BlackholeDensity            = _Field(os.path.join(self.path,"BlackholeDensity"))
        self.BlackholeJumpToMinPot       = _Field(os.path.join(self.path,"BlackholeJumpToMinPot"))
        self.BlackholeKineticFdbkEnergy  = _Field(os.path.join(self.path,"BlackholeKineticFdbkEnergy"))
        self.BlackholeMass               = _Field(os.path.join(self.path,"BlackholeMass"))
        self.BlackholeMinPotPos          = _Field(os.path.join(self.path,"BlackholeMinPotPos"))
        self.BlackholeMseed              = _Field(os.path.join(self.path,"BlackholeMseed"))
        self.BlackholeMtrack             = _Field(os.path.join(self.path,"BlackholeMtrack"))
        self.BlackholeProgenitors        = _Field(os.path.join(self.path,"BlackholeProgenitors"))
        self.BlackholeSwallowID          = _Field(os.path.join(self.path,"BlackholeSwallowID"))
        self.BlackholeSwallowTime        = _Field(os.path.join(self.path,"BlackholeSwallowTime"))
        self.Generation                  = _Field(os.path.join(self.path,"Generation"))
        self.GroupID                     = _Field(os.path.join(self.path,"GroupID"))
        self.ID                          = _Field(os.path.join(self.path,"ID"))
        self.Mass                        = _Field(os.path.join(self.path,"Mass"))
        self.Position                    = _Field(os.path.join(self.path,"Position"))
        self.Potential                   = _Field(os.path.join(self.path,"Potential"))
        self.SmoothingLength             = _Field(os.path.join(self.path,"SmoothingLength"))
        self.StarFormationTime           = _Field(os.path.join(self.path,"StarFormationTime"))
        self.Swallowed                   = _Field(os.path.join(self.path,"Swallowed"))
        self.Velocity                    = _Field(os.path.join(self.path,"Velocity"))
