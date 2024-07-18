import os
from typing import Any
import galspy.IO.BigFile as bf
import galspy.utility.HaloQuery as rs


class _Folder:
    def __init__(self,path:str) -> None:
        self.path = path
        self.name = os.path.basename(self.path)
        self.parent_path = os.path.abspath(os.path.join(path, os.pardir))

class _Node(_Folder):
    def __init__(self, path: str) -> None:
        super().__init__(path)
    
    def _ReadWithNumpy(self):
        return bf.Column(self.path).Read()
    
    def _ReadWithBigFile(self):
        raise NotImplementedError
    
    def Read(self):
        return self._ReadWithNumpy()
    
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.Read()

class _NodeGroup(_Folder):
    def __init__(self,path):
        super().__init__(path)
    
    def AddNode(self,field_subdir_name):
        return _Node(os.path.join(self.path,field_subdir_name))

class _Gas(_NodeGroup):
    def __init__(self,path):
        super().__init__(path)
    
        self.DelayTime                   = self.AddNode("DelayTime")
        self.Density                     = self.AddNode("Density")
        self.EgyWtDensity                = self.AddNode("EgyWtDensity")
        self.ElectronAbundance           = self.AddNode("ElectronAbundance")
        self.Generation                  = self.AddNode("Generation")
        self.GroupID                     = self.AddNode("GroupID")
        self.HeIIIIonized                = self.AddNode("HeIIIIonized")
        self.ID                          = self.AddNode("ID")
        self.InternalEnergy              = self.AddNode("InternalEnergy")
        self.Mass                        = self.AddNode("Mass")
        self.Metallicity                 = self.AddNode("Metallicity")
        self.Metals                      = self.AddNode("Metals")
        self.NeutralHydrogenFraction     = self.AddNode("NeutralHydrogenFraction")
        self.Position                    = self.AddNode("Position")
        self.Potential                   = self.AddNode("Potential")
        self.SmoothingLength             = self.AddNode("SmoothingLength")
        self.StarFormationRate           = self.AddNode("StarFormationRate")
        self.Velocity                    = self.AddNode("Velocity")

class _DarkMatter(_NodeGroup):
    def __init__(self,path):
        super().__init__(path)

        self.GroupID                     = self.AddNode("GroupID")
        self.ID                          = self.AddNode("ID")
        self.Mass                        = self.AddNode("Mass")
        self.Position                    = self.AddNode("Position")
        self.Potential                   = self.AddNode("Potential")
        self.Velocity                    = self.AddNode("Velocity")

class _Neutrino(_NodeGroup):
    def __init__(self,path):
        super().__init__(path)

        self.GroupID                     = self.AddNode("GroupID")
        self.ID                          = self.AddNode("ID")
        self.Mass                        = self.AddNode("Mass")
        self.Position                    = self.AddNode("Position")
        self.Potential                   = self.AddNode("Potential")
        self.Velocity                    = self.AddNode("Velocity")

class _Star(_NodeGroup):
    def __init__(self,path):
        super().__init__(path)

        self.BirthDensity                = self.AddNode("BirthDensity")
        self.Generation                  = self.AddNode("Generation")
        self.GroupID                     = self.AddNode("GroupID")
        self.ID                          = self.AddNode("ID")
        self.LastEnrichmentMyr           = self.AddNode("LastEnrichmentMyr")
        self.Mass                        = self.AddNode("Mass")
        self.Metallicity                 = self.AddNode("Metallicity")
        self.Metals                      = self.AddNode("Metals")
        self.Position                    = self.AddNode("Position")
        self.Potential                   = self.AddNode("Potential")
        self.SmoothingLength             = self.AddNode("SmoothingLength")
        self.StarFormationTime           = self.AddNode("StarFormationTime")
        self.TotalMassReturned           = self.AddNode("TotalMassReturned")
        self.Velocity                    = self.AddNode("Velocity")

class _BlackHole(_NodeGroup):
    def __init__(self,path):
        super().__init__(path)

        self.BlackholeAccretionRate      = self.AddNode("BlackholeAccretionRate")
        self.BlackholeDensity            = self.AddNode("BlackholeDensity")
        self.BlackholeJumpToMinPot       = self.AddNode("BlackholeJumpToMinPot")
        self.BlackholeKineticFdbkEnergy  = self.AddNode("BlackholeKineticFdbkEnergy")
        self.BlackholeMass               = self.AddNode("BlackholeMass")
        self.BlackholeMinPotPos          = self.AddNode("BlackholeMinPotPos")
        self.BlackholeMseed              = self.AddNode("BlackholeMseed")
        self.BlackholeMtrack             = self.AddNode("BlackholeMtrack")
        self.BlackholeProgenitors        = self.AddNode("BlackholeProgenitors")
        self.BlackholeSwallowID          = self.AddNode("BlackholeSwallowID")
        self.BlackholeSwallowTime        = self.AddNode("BlackholeSwallowTime")
        self.Generation                  = self.AddNode("Generation")
        self.GroupID                     = self.AddNode("GroupID")
        self.ID                          = self.AddNode("ID")
        self.Mass                        = self.AddNode("Mass")
        self.Position                    = self.AddNode("Position")
        self.Potential                   = self.AddNode("Potential")
        self.SmoothingLength             = self.AddNode("SmoothingLength")
        self.StarFormationTime           = self.AddNode("StarFormationTime")
        self.Swallowed                   = self.AddNode("Swallowed")
        self.Velocity                    = self.AddNode("Velocity")

class _SnapHeader(_Folder):
    def __init__(self, path: str) -> None:
        super().__init__(path)

    def Read(self):
        return bf.Attribute(os.path.join(self.path,"attr-v2")).Read()
    
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.Read()
        
class _PART(_Folder):
    def __init__(self,path):
        super().__init__(path)

        self.Gas        = _Gas(os.path.join(self.path,"0"))
        self.DarkMatter = _DarkMatter(os.path.join(self.path,"1"))
        self.Neutrino   = _Neutrino(os.path.join(self.path,"2"))
        self.Star       = _Star(os.path.join(self.path,"4"))
        self.BlackHole  = _BlackHole(os.path.join(self.path,"5"))
        self._0         = self.Gas
        self._1         = self.DarkMatter
        self._2         = self.Neutrino
        self._4         = self.Star
        self._5         = self.BlackHole

        self.Header     = _SnapHeader(os.path.join(self.path,"Header"))

class _FOFGroups(_NodeGroup):
    def __init__(self,path):
        super().__init__(path)

        self.BlackholeAccretionRate      = self.AddNode("BlackholeAccretionRate")
        self.BlackholeMass               = self.AddNode("BlackholeMass")
        self.FirstPos                    = self.AddNode("FirstPos")
        self.GasMetalElemMass            = self.AddNode("GasMetalElemMass")
        self.GasMetalMass                = self.AddNode("GasMetalMass")
        self.GroupID                     = self.AddNode("GroupID")
        self.Imom                        = self.AddNode("Imom")
        self.Jmom                        = self.AddNode("Jmom")
        self.LengthByType                = self.AddNode("LengthByType")
        self.Mass                        = self.AddNode("Mass")
        self.MassByType                  = self.AddNode("MassByType")
        self.MassCenterPosition          = self.AddNode("MassCenterPosition")
        self.MassCenterVelocity          = self.AddNode("MassCenterVelocity")
        self.MassHeIonized               = self.AddNode("MassHeIonized")
        self.MinID                       = self.AddNode("MinID")
        self.StarFormationRate           = self.AddNode("StarFormationRate")
        self.StellarMetalElemMass        = self.AddNode("StellarMetalElemMass")
        self.StellarMetalMass            = self.AddNode("StellarMetalMass")

class _PIG(_Folder):
    def __init__(self,path):
        super().__init__(path)

        self.Gas        = _Gas(os.path.join(self.path,"0"))
        self.DarkMatter = _DarkMatter(os.path.join(self.path,"1"))
        self.Neutrino   = _Neutrino(os.path.join(self.path,"2"))
        self.Star       = _Star(os.path.join(self.path,"4"))
        self.BlackHole  = _BlackHole(os.path.join(self.path,"5"))
        self._0         = self.Gas
        self._1         = self.DarkMatter
        self._2         = self.Neutrino
        self._4         = self.Star
        self._5         = self.BlackHole

        self.Header     = _SnapHeader(os.path.join(self.path,"Header"))
        self.FOFGroups  = _FOFGroups(os.path.join(self.path,"FOFGroups"))

class _RSGParticle(_NodeGroup):
    def __init__(self,path):
        super().__init__(path)

        self.HaloID                     = self.AddNode("HaloID")
        self.ID                         = self.AddNode("ID")
        self.Mass                       = self.AddNode("Mass")
        self.Position                   = self.AddNode("Position")
        self.Velocity                   = self.AddNode("Velocity")
        self.Velocity                   = self.AddNode("Type")

class _RKSGroups(_NodeGroup):
    def __init__(self,path):
        super().__init__(path)

        self.A                          = self.AddNode("A")
        self.A2                         = self.AddNode("A2")
        self.AlternateMasses            = self.AddNode("AlternateMasses")
        self.AngularMomentum            = self.AddNode("AngularMomentum")
        self.AverageDensity             = self.AddNode("AverageDensity")
        self.BlackholeMass              = self.AddNode("BlackholeMass")
        self.b_to_a                     = self.AddNode("b_to_a")
        self.b_to_a2                    = self.AddNode("b_to_a2")
        self.BulkVelocity               = self.AddNode("BulkVelocity")
        self.BulkVelocityUncertainty    = self.AddNode("BulkVelocityUncertainty")
        self.BullockSpin                = self.AddNode("BullockSpin")
        self.Child                      = self.AddNode("Child")
        self.ChildParticleLength        = self.AddNode("ChildParticleLength")
        self.child_r                    = self.AddNode("child_r")
        self.CoreLength                 = self.AddNode("CoreLength")
        self.CoreVelocity               = self.AddNode("CoreVelocity")
        self.c_to_a                     = self.AddNode("c_to_a")
        self.c_to_a2                    = self.AddNode("c_to_a2")
        self.Descendant                 = self.AddNode("Descendant")
        self.Energy                     = self.AddNode("Energy")
        self.GasMass                    = self.AddNode("GasMass")
        self.HaloID                     = self.AddNode("HaloID")
        self.InternalHaloID             = self.AddNode("InternalHaloID")
        self.KineticToPotentialRatio    = self.AddNode("KineticToPotentialRatio")
        self.klypin_rs                  = self.AddNode("klypin_rs")
        self.mgrav                      = self.AddNode("mgrav")
        self.m_pe_b                     = self.AddNode("m_pe_b")
        self.m_pe_d                     = self.AddNode("m_pe_d")
        self.NextCochild                = self.AddNode("NextCochild")
        self.ParticleLength             = self.AddNode("ParticleLength")
        self.ParticleStartIndex         = self.AddNode("ParticleStartIndex")
        self.PeakDensity                = self.AddNode("PeakDensity")
        self.ph                         = self.AddNode("ph")
        self.Position                   = self.AddNode("Position")
        self.PositionOffset             = self.AddNode("PositionOffset")
        self.PositionUncertainty        = self.AddNode("PositionUncertainty")
        self.PrevCochild                = self.AddNode("PrevCochild")
        self.rs                         = self.AddNode("rs")
        self.rvmax                      = self.AddNode("rvmax")
        self.Spin                       = self.AddNode("Spin")
        self.StellarMass                = self.AddNode("StellarMass")
        self.Sub_of                     = self.AddNode("Sub_of")
        self.Type                       = self.AddNode("Type")
        self.Velocity                   = self.AddNode("Velocity")
        self.VelocityOffset             = self.AddNode("VelocityOffset")
        self.VelocityUncertainty        = self.AddNode("VelocityUncertainty")
        self.VirialMass                 = self.AddNode("VirialMass")
        self.VirialRadius               = self.AddNode("VirialRadius")
        self.Vmax                       = self.AddNode("Vmax")
        self.vmax_r                     = self.AddNode("vmax_r")
        self.Vrms                       = self.AddNode("Vrms")

        # Post-Processed

class _RSG(_Folder):
    def __init__(self,path):
        super().__init__(path)

        self.RKSParticles   = _RSGParticle(os.path.join(self.path,"RKSParticles"))
        self.Header         = _SnapHeader(os.path.join(self.path,"Header"))
        self.RKSHalos      = _RKSGroups(os.path.join(self.path,"RKSHalos"))


class _Sim(_Folder):
    def __init__(self, path: str) -> None:
        super().__init__(path)

    def PART(self,snap_num:int):
        if not isinstance(snap_num,int):raise TypeError
        return _PART(os.path.join(self.path,"PART_" + self._FixedFormatSnapNumber(snap_num)))

    def PIG(self,snap_num:int):
        if not isinstance(snap_num,int):raise TypeError
        return _PIG(os.path.join(self.path,"PIG_" + self._FixedFormatSnapNumber(snap_num)))
    
    def RSG(self,snap_num:int):
        if not isinstance(snap_num,int):raise TypeError
        return _RSG(os.path.join(self.path,"RSG_" + self._FixedFormatSnapNumber(snap_num)))
    
    def _FixedFormatSnapNumber(self, snap_num):
        return '{:03}'.format(snap_num)

def NavigationRoot(path:str):
    if not os.path.isdir(path):
        print("ERROR : Navigation Root Directory")
    return _Sim(path)

def RSGRoot(path:str):
    if not os.path.isdir(path):
        print("ERROR : RSG Root Directory")
    return _RSG(path)