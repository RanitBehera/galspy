import os
from galspec.navigation.base.Folder import _Folder
from galspec.IO.Field import _Field

class _Gas(_Folder):
    def __init__(self,path):
        super().__init__(path)

        self.DelayTime                   = _Field(os.path.join(self.path,"DelayTime"))
        self.Density                     = _Field(os.path.join(self.path,"Density"))
        self.EgyWtDensity                = _Field(os.path.join(self.path,"EgyWtDensity"))
        self.ElectronAbundance           = _Field(os.path.join(self.path,"ElectronAbundance"))
        self.Generation                  = _Field(os.path.join(self.path,"Generation"))
        self.GroupID                     = _Field(os.path.join(self.path,"GroupID"))
        self.HeIIIIonized                = _Field(os.path.join(self.path,"HeIIIIonized"))
        self.ID                          = _Field(os.path.join(self.path,"ID"))
        self.InternalEnergy              = _Field(os.path.join(self.path,"InternalEnergy"))
        self.Mass                        = _Field(os.path.join(self.path,"Mass"))
        self.Metallicity                 = _Field(os.path.join(self.path,"Metallicity"))
        self.Metals                      = _Field(os.path.join(self.path,"Metals"))
        self.NeutralHydrogenFraction     = _Field(os.path.join(self.path,"NeutralHydrogenFraction"))
        self.Position                    = _Field(os.path.join(self.path,"Position"))
        self.Potential                   = _Field(os.path.join(self.path,"Potential"))
        self.SmoothingLength             = _Field(os.path.join(self.path,"SmoothingLength"))
        self.StarFormationRate           = _Field(os.path.join(self.path,"StarFormationRate"))
        self.Velocity                    = _Field(os.path.join(self.path,"Velocity"))
