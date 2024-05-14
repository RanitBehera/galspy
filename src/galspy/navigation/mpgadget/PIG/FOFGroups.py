import os
from galspec.navigation.base.Folder import _Folder
from galspec.IO.Field import _Field

class _FOFGroups(_Folder):
    def __init__(self,path):
        super().__init__(path)

        self.BlackholeAccretionRate      = _Field(os.path.join(self.path,"BlackholeAccretionRate"))
        self.BlackholeMass               = _Field(os.path.join(self.path,"BlackholeMass"))
        self.FirstPos                    = _Field(os.path.join(self.path,"FirstPos"))
        self.GasMetalElemMass            = _Field(os.path.join(self.path,"GasMetalElemMass"))
        self.GasMetalMass                = _Field(os.path.join(self.path,"GasMetalMass"))
        self.GroupID                     = _Field(os.path.join(self.path,"GroupID"))
        self.Imom                        = _Field(os.path.join(self.path,"Imom"))
        self.Jmom                        = _Field(os.path.join(self.path,"Jmom"))
        self.LengthByType                = _Field(os.path.join(self.path,"LengthByType"))
        self.Mass                        = _Field(os.path.join(self.path,"Mass"))
        self.MassByType                  = _Field(os.path.join(self.path,"MassByType"))
        self.MassCenterPosition          = _Field(os.path.join(self.path,"MassCenterPosition"))
        self.MassCenterVelocity          = _Field(os.path.join(self.path,"MassCenterVelocity"))
        self.MassHeIonized               = _Field(os.path.join(self.path,"MassHeIonized"))
        self.MinID                       = _Field(os.path.join(self.path,"MinID"))
        self.StarFormationRate           = _Field(os.path.join(self.path,"StarFormationRate"))
        self.StellarMetalElemMass        = _Field(os.path.join(self.path,"StellarMetalElemMass"))
        self.StellarMetalMass            = _Field(os.path.join(self.path,"StellarMetalMass"))