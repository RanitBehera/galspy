import os
from galspec.navigation.base.Folder import _Folder
from galspec.IO.Field import _Field

class _Star(_Folder):
    def __init__(self,path):
        super().__init__(path)

        self.BirthDensity                = _Field(os.path.join(self.path,"BirthDensity"))
        self.Generation                  = _Field(os.path.join(self.path,"Generation"))
        self.GroupID                     = _Field(os.path.join(self.path,"GroupID"))
        self.ID                          = _Field(os.path.join(self.path,"ID"))
        self.LastEnrichmentMyr           = _Field(os.path.join(self.path,"LastEnrichmentMyr"))
        self.Mass                        = _Field(os.path.join(self.path,"Mass"))
        self.Metallicity                 = _Field(os.path.join(self.path,"Metallicity"))
        self.Metals                      = _Field(os.path.join(self.path,"Metals"))
        self.Position                    = _Field(os.path.join(self.path,"Position"))
        self.Potential                   = _Field(os.path.join(self.path,"Potential"))
        self.SmoothingLength             = _Field(os.path.join(self.path,"SmoothingLength"))
        self.StarFormationTime           = _Field(os.path.join(self.path,"StarFormationTime"))
        self.TotalMassReturned           = _Field(os.path.join(self.path,"TotalMassReturned"))
        self.Velocity                    = _Field(os.path.join(self.path,"Velocity"))