import os
import galspy
import pickle
from typing import Any, Literal
import galspy.FileTypes.BigFile as bf
import galspy.FileTypes.ConfigFile as cf
# import galspy.Spectra.Templates as tp
from galspy.Spectra.Templates import GetCachedStarsSpecTemplateIndex
import numpy
import bigfile as bigf
from astropy.cosmology import FlatLambdaCDM
from galspy.Spectra.ColumnDensity import GetCentralStarPosition, GetStellarSPHColumnDensity

class _Folder:
    def __init__(self,path:str) -> None:
        self.path = path
        self.name = os.path.basename(self.path)
        self.parent_path = os.path.abspath(os.path.join(path, os.pardir))

class _Node(_Folder):
    def __init__(self, path: str) -> None:
        super().__init__(path)
    
    def Read(self,blobnames:list[str]=None):
        return bf.Column(self.path).Read(blobnames)
    
    def __call__(self, args:list[str]=None, **kwds: Any) -> Any:
        # Its purpose is to call Read() function in a convenient way
        # if args:args=list(args)
        # else:args=None
        return self.Read(args)

class _NodeGroup(_Folder):
    def __init__(self,path):
        super().__init__(path)
    
    def AddNode(self,field_subdir_name):
        return _Node(os.path.join(self.path,field_subdir_name))


class _Units:
    def __init__(self,header:dict):
        # Units are in CGS with h=1
        self.Length             = header["UnitLength_in_cm"]
        self.Mass               = header["UnitMass_in_g"]
        self.Velocity           = header["UnitVelocity_in_cm_per_s"]
        self.Density            = self.Mass/(self.Length**3)
        self.Time               = self.Length/self.Velocity
        self.Energy             = self.Mass * (self.Velocity**2)
        self.InternalEnergy     = self.Energy/self.Mass

    def print(self):
        CELL_WIDTH=16
        print("UNITS (in h=1)",'-'*32)
        print("-","Length".ljust(CELL_WIDTH),':',self.Length,"cm")
        print("-","Mass".ljust(CELL_WIDTH),':',self.Mass,"g")
        print("-","Velocity".ljust(CELL_WIDTH),':',self.Velocity,"cm/s")
        print("-","Density".ljust(CELL_WIDTH),':',self.Density,"g/cm3")
        print("-","Time".ljust(CELL_WIDTH),':',self.Time,"s")
        print("-","Energy".ljust(CELL_WIDTH),':',self.Energy)
        print("-","InternalEnergy".ljust(CELL_WIDTH),':',self.InternalEnergy)
        # CHECKED: the units match with stdout units when h=1


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

    def GetDensityAndTemperature(self,rho,ie,nebynh,Units:_Units):
        rho *=Units.Density
        ie *=Units.InternalEnergy

        MP = 1.67e-27 #Proton mass in grams
        GAMMA = 5/3
        MIN_GAS_TEMP = 5.0 #K
        KB = 1.38e-16
        X = 0.74 

        # From Codes
        mu=4/(X*(3+4*nebynh)+1)
        temp1 = (GAMMA-1)*(MP/KB)*mu*ie 
        
        # From Shared
        Y=1-X
        Ne=nebynh
        temp = 8*MP*ie/(3*KB*(4+4*Ne-4*Y*nebynh-3*Y))

        return rho,temp,temp1



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



class _PARTHeader:
    def __init__(self, path: str) -> None:
        self.path = os.path.join(path,"Header/attr-v2")
        self._header = bf.Attribute(self.path).Read()
        self.Units = _Units(self._header)
        
    def BoxSize(self):                    return self._header["BoxSize"]
    def CMBTemperature(self):             return self._header["CMBTemperature"]
    def CodeVersion(self):                return self._header["CodeVersion"]
    def CompilerSettings(self):           return self._header["CompilerSettings"]
    def DensityKernel(self):              return self._header["DensityKernel"]
    def HubbleParam(self):                return self._header["HubbleParam"]
    def MassTable(self):                  return self._header["MassTable"]
    def Omega0(self):                     return self._header["Omega0"]
    def OmegaBaryon(self):                return self._header["OmegaBaryon"]
    def OmegaLambda(self):                return self._header["OmegaLambda"]
    def RSDFactor(self):                  return self._header["RSDFactor"]
    def Time(self):                       return self._header["Time"]
    def TimeIC(self):                     return self._header["TimeIC"]
    def TotNumPart(self):                 return self._header["TotNumPart"]
    def TotNumPartInit(self):             return self._header["TotNumPartInit"]
    def UnitLength_in_cm(self):           return self._header["UnitLength_in_cm"]
    def UnitMass_in_g(self):              return self._header["UnitMass_in_g"]
    def UnitVelocity_in_cm_per_s(self):   return self._header["UnitVelocity_in_cm_per_s"]
    def UsePeculiarVelocity(self):        return self._header["UsePeculiarVelocity"]
    # ----- Extra
    def Redshift(self):                   return (1/self.Time()) - 1

    def __call__(self):
        return self._header

class _PIGHeader(_Folder):
    def __init__(self, path: str) -> None:
        self.path = os.path.join(path,"Header/attr-v2")
        self._header = bf.Attribute(self.path).Read()
        self.Units   = _PART(path.replace("PIG","PART")).Header.Units
        # Simple replace will not work for secondarty snapshots where PART is deleted
        # self.Units   = _PART(os.path.abspath(path+"/../PART_000")).Header.Units



    def BoxSize(self):                    return self._header["BoxSize"]
    def CMBTemperature(self):             return self._header["CMBTemperature"]
    def HubbleParam(self):                return self._header["HubbleParam"]
    def MassTable(self):                  return self._header["MassTable"]
    def NumFOFGroupsTotal(self):          return self._header["NumFOFGroupsTotal"]
    def NumPartInGroupTotal(self):        return self._header["NumPartInGroupTotal"]
    def Omega0(self):                     return self._header["Omega0"]
    def OmegaBaryon(self):                return self._header["OmegaBaryon"]
    def OmegaLambda(self):                return self._header["OmegaLambda"]
    def RSDFactor(self):                  return self._header["RSDFactor"]
    def Time(self):                       return self._header["Time"]
    def UsePeculiarVelocity(self):        return self._header["UsePeculiarVelocity"]
    # ----- Extra
    def Redshift(self):                   return (1/self.Time()) - 1

    def __call__(self):
        return self._header



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

        self.Header     = _PARTHeader(self.path)
        self.sim_name   = os.path.basename(os.path.abspath(self.path + "../../../"))
        self.snap_name  = os.path.basename(os.path.abspath(self.path))
        self.redshift_name  = f"z{self.Header.Redshift():.02f}".replace(".",'p')

    def print_box_info(self,cell_width=8):
        print("- Simulation".ljust(cell_width),":",self.sim_name)
        print("- Snapshot".ljust(cell_width),":",self.snap_name)
        print("- Redshift".ljust(cell_width),":",f"{self.Header.Redshift():.02f}")

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
    CACHE_DIR = "/mnt/home/student/cranit/RANIT/Repo/galspy/cache/simulations"
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

        self.Header     = _PIGHeader(self.path)
        self.FOFGroups  = _FOFGroups(os.path.join(self.path,"FOFGroups"))
        self.sim_name   = os.path.basename(os.path.abspath(self.path + "../../../"))
        self.snap_name  = os.path.basename(os.path.abspath(self.path))
        self.redshift_name  = f"z{self.Header.Redshift():.02f}".replace(".",'p')

    def print_box_info(self,cell_width=8):
        print("- Simulation".ljust(cell_width),":",self.sim_name)
        print("- Snapshot".ljust(cell_width),":",self.snap_name)
        print("- Redshift".ljust(cell_width),":",f"{self.Header.Redshift():.02f}")

    def GetStarsSpecIndex(self):
        SEARCH_DIR = _PIG.CACHE_DIR
        SEARCH_DIR += os.sep + self.sim_name + os.sep + self.snap_name
        FILENAME = "StarSpecTemplateIndex.dict"
        FILEPATH = SEARCH_DIR + os.sep + FILENAME

        return GetCachedStarsSpecTemplateIndex(
            FILEPATH,
            self.Star.ID(),
            self.Star.StarFormationTime(),
            self.Star.Metallicity(),
            FlatLambdaCDM(H0=self.Header.HubbleParam()*100, Om0=self.Header.Omega0()),
            self.Header.Redshift()
        )
    
    def GetCentralStarPosition(self):
        SEARCH_DIR = _PIG.CACHE_DIR
        SEARCH_DIR += os.sep + self.sim_name + os.sep + self.snap_name
        FILENAME = "CentralStarLocation.dict"
        FILEPATH = SEARCH_DIR + os.sep + FILENAME

        return GetCentralStarPosition(FILEPATH,self,num_pool_worker=24)

    def GetStellarSPHColumnDensity(self):
        SEARCH_DIR = _PIG.CACHE_DIR
        SEARCH_DIR += os.sep + self.sim_name + os.sep + self.snap_name
        FILENAME = "StellarSPHColumnDensity.dict"
        FILEPATH = SEARCH_DIR + os.sep + FILENAME

        # return GetStellarSPHColumnDensity(FILEPATH,self,num_pool_worker=24)




class _Param_GenIC:
    def __init__(self,path) -> None:
        genic = cf.ReadAsDictionary(path)
        # ===== RESOLUTION =====
        self.BoxSize                    = genic["BoxSize"]
        self.Ngrid                      = genic["Ngrid"]
        self.ProduceGas                 = genic["ProduceGas"]
        # ===== COSMOLOGY =====
        self.HubbleParam                = genic["HubbleParam"]
        self.OmegaLambda                = genic["OmegaLambda"]
        self.Omega0                     = genic["Omega0"]
        self.OmegaBaryon                = genic["OmegaBaryon"]
        self.CMBTemperature             = genic["CMBTemperature"]
        # ===== CLASS =====
        self.WhichSpectrum              = genic["WhichSpectrum"]
        self.FileWithInputSpectrum      = genic["FileWithInputSpectrum"]
        self.DifferentTransferFunctions = genic["DifferentTransferFunctions"]
        self.FileWithTransferFunction   = genic["FileWithTransferFunction"]
        self.Redshift                   = genic["Redshift"]
        self.Sigma8                     = genic["Sigma8"]
        self.PrimordialAmp              = genic["PrimordialAmp"]
        self.PrimordialIndex            = genic["PrimordialIndex"]
        # ===== OUTPUT =====
        self.Seed                       = genic["Seed"]
        self.OutputDir                  = genic["OutputDir"]
        self.FileBase                   = genic["FileBase"]
        # ===== UNITS =====
        self.UnitLength_in_cm           = genic["UnitLength_in_cm"]
        self.UnitMass_in_g              = genic["UnitMass_in_g"]
        self.UnitVelocity_in_cm_per_s   = genic["UnitVelocity_in_cm_per_s"]
        # ===== RESOURCE =====
        self.MaxMemSizePerNode          = genic["MaxMemSizePerNode"]


# class _Param_Gadget:
#     def __init__(self,path) -> None:
#         gadget = cf.ReadAsDictionary(path)

        # ===== COSMOLOGY =====
        # HubbleParam
        # OmegaLambda
        # Omega0
        # OmegaBaryon
        # CMBTemperature

        # RadiationOn
        # MassiveNuLinRespOn


        # =================
        # ===== INPUT =====
        # =================
        # InitCondFile


        # ==================
        # ===== OUTPUT =====
        # ==================
        # TimeMax
        # OutputList

        # OutputDir
        # # SnapshotFileBase
        # # FOFFileBase
        # EnergyFile =
        # CpuFile =


        # ====================
        # ===== RESOURCE =====
        # ====================
        # TimeLimitCPU
        # MaxMemSizePerNode
        # SlotsIncreaseFactor

        # ===================
        # ===== GRAVITY =====
        # ===================
        # # TreeGravOn
        # # GravitySoftening


        # ===============
        # ===== SPH =====
        # ===============
        # HydroOn
        # # DensityOn
        # DensityIndependentSphOn
        # SplitGravityTimestepsOn
        # DensityKernelType


        # ==================
        # ===== COOLING ====
        # ==================
        # CoolingOn
        # TreeCoolFile
        # MetalCoolFile
        # # CoolingRates
        # # RecombRates
        # # SelfShieldingOn
        # MinGasTemp

        # ----- PhotoIonization -----
        # # PhotoIonizationOn
        # # PhotoIonizeFactor

        # ----- Reionization -----
        # ReionHistFile =
        # UVFluctuationFile =
        # HIReionTemp =
        # UVRedshiftThreshold =


        # ==========================
        # ===== STAR FORMATION =====
        # ==========================
        # StarformationOn
        # StarformationCriterion
        # CritOverDensity
        # CritPhysDensity
        # # FactorSN
        # # FactorEVP
        # # TempSupernova
        # # TempClouds
        # # Generations
        # MetalReturnOn
        # QuickLymanAlphaProbability


        # =================
        # ===== WINDS =====
        # =================
        # WindOn
        # WindModel
        # WindEfficiency
        # WindEnergyFraction
        # WindSpeedFactor
        # WindSigma0
        # WindFreeTravelLength
        # WindFreeTravelDensFac
        # MaxWindFreeTravelTime
        # MinWindVelocity =
        # WindThermalFactor =


        # =====================
        # ===== BLACKHOLE =====
        # =====================
        # BlackHoleOn
        # BlackHoleFeedbackMethod
        # BlackHoleNgbFactor

        # ----- Seeding ------
        # MinFoFMassForNewSeed
        # MinMStarForNewSeed
        # SeedBlackHoleMass
        # MaxSeedBlackHoleMass
        # SeedBlackHoleMassIndex

        # ----- Dynamical Friction ------
        # BH_DynFrictionMethod
        # SeedBHDynMass

        # ----- Accretion ------
        # BlackHoleAccretionFactor
        # BlackHoleEddingtonFactor

        # ----- Feedback (Thermal) -----
        # BlackHoleFeedbackFactor
        # TimeBetweenSeedingSearch

        # ----- Feedback (Kinetic) -----
        # BlackHoleKineticOn
        # BHKE_EddingtonThrFactor
        # BHKE_EddingtonMFactor
        # BHKE_EddingtonMPivot
        # BHKE_EddingtonMIndex
        # BHKE_EffRhoFactor
        # BHKE_EffCap
        # BHKE_InjEnergyThr

        # ----- Extra -----
        # WriteBlackHoleDetails


        # =====================
        # ===== FOF Halos =====
        # =====================
        # SnapshotWithFOF
        # FOFHaloLinkingLength
        # FOFHaloMinLength
        # # FOFSaveParticles




class _Run(_Folder):
    def __init__(self,path):
        super().__init__(path)




class _IC(_Folder):
    def __init__(self,path):
        super().__init__(path)




class _Sim:
    def __init__(self, mpgadget_outdir: str,rockstar_outbase:str=None) -> None:
        self.mpgadget_outdir = mpgadget_outdir
        self.rockstar_outbase = rockstar_outbase
        self.sim_name = os.path.basename(os.path.abspath(self.mpgadget_outdir + "../../"))

    def PART(self,snap_num:int=None,z:float=None):
        if snap_num is None:
            if z is None:raise ValueError("Either Snapnumber or Redshift is needed.")
            else:snap_num = self.SnapNumFromRedshift(z)

        if not isinstance(snap_num,int):raise TypeError
        return _PART(os.path.join(self.mpgadget_outdir,"PART_" + self._FixedFormatSnapNumber(snap_num)))

    def PIG(self,snap_num:int=None,z:float=None):
        if snap_num is None:
            if z is None:raise ValueError("Either Snapnumber or Redshift is needed.")
            else:snap_num = self.SnapNumFromRedshift(z)
            
        if not isinstance(snap_num,int):raise TypeError
        return _PIG(os.path.join(self.mpgadget_outdir,"PIG_" + self._FixedFormatSnapNumber(snap_num)))
    
    def _FixedFormatSnapNumber(self, snap_num):
        return '{:03}'.format(snap_num)
    
    def GetCosmology(self):
        COSMOLOGY   = {
                # Get these from simulation run files
                'flat': True,
                'H0': 67.36,
                'Om0': 0.3153,
                'Ob0': 0.0493,
                'sigma8': 0.811,
                'ns': 0.9649
                }
        return COSMOLOGY
    
    def GetAstropyFlatLCDM(self):
        cosmology = self.GetCosmology()
        return FlatLambdaCDM(H0=cosmology["H0"],Om0=cosmology["Om0"])
    
    def SnapNumFromRedshift(self,redshift):
        # Get Snapnumbers and Scale Factors
        sn,a = numpy.loadtxt(self.mpgadget_outdir+os.sep+"Snapshots.txt").T
        # Convert Snapnumbers type to "integer"
        sn = [int(sni) for sni in sn]
        # Convert Scale Factors to Redshifts
        z = (1/a)-1
        # Get indices where the difference between requested redshift and table row is less then tolerance
        _TOLERANCE = 0.001
        indices = numpy.array([i for i, zi in enumerate(z) if abs(zi - redshift) <= _TOLERANCE])

        if len(indices)==1:
            # If only one element --> requested redshift exists
            return sn[indices[0]]
        elif len(indices)==0:
            # If zero element --> requested redshift doesn't exists
            return None
        else:
            # If more than one element --> requested redshift appears twice, check it.
            RuntimeError("More than one box found. Try decereasing the tolerance or check for duplicate snaps.")
            return None
        



def NavigationRoot(path:str,rsg_path:str=None):
    if not os.path.isdir(path):
        print("ERROR : Navigation Root Directory.\n",path)
    
    folder = _Folder(path)
    if rsg_path==None:
        rsg_path = folder.parent_path + os.sep + "OUT_" + folder.name

    return _Sim(path,rsg_path)
