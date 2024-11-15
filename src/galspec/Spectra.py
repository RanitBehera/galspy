import numpy
import pickle


# ==================================================================
def GetFromDictWithKeyList(target_dict:dict,key_list:list[str]):
    value=target_dict
    for key in key_list:
        value = value.get(key)
    return value


CACHE_FILE_PATH = ""    # Get from env or config file etc, or hardcode
class _CacheFile:
    cache = None
    def __init__(self, cache_filepath) -> None:
        pass

    def Get(self,key_list:list[str]):
        if _CacheFile.cache is None:
            print("Reading Cache File.")
            with open(CACHE_FILE_PATH,"rb") as fp:
                _CacheFile.cache = pickle.load(fp)
        
        return GetFromDictWithKeyList(self.cache,key_list)




# ==================================================================
class _Source:
    def __init__(self) -> None:
        self.Wavelengths = ""
    
    def StellarFlux(self):
        pass
    
    def NebularFlux(self):
        pass
    
    def TotalFlux(self):
        pass

# ==================================================================
class _Age:
    def __init__(self,key_list:list[str]) -> None:
        self._key_list = key_list
        # -----
        self.T_60 = _Source(self._key_list + ["T_60"])
        self.T_61 = _Source(self._key_list + ["T_61"])
        self.T_62 = _Source(self._key_list + ["T_62"])
        self.T_63 = _Source(self._key_list + ["T_63"])
        self.T_64 = _Source(self._key_list + ["T_64"])
        self.T_65 = _Source(self._key_list + ["T_65"])
        self.T_66 = _Source(self._key_list + ["T_66"])
        self.T_67 = _Source(self._key_list + ["T_67"])
        self.T_68 = _Source(self._key_list + ["T_68"])
        self.T_69 = _Source(self._key_list + ["T_69"])
        # -----
        self.T_70 = _Source(self._key_list + ["T_70"])
        self.T_71 = _Source(self._key_list + ["T_71"])
        self.T_72 = _Source(self._key_list + ["T_72"])
        self.T_73 = _Source(self._key_list + ["T_73"])
        self.T_74 = _Source(self._key_list + ["T_74"])
        self.T_75 = _Source(self._key_list + ["T_75"])
        self.T_76 = _Source(self._key_list + ["T_76"])
        self.T_77 = _Source(self._key_list + ["T_77"])
        self.T_78 = _Source(self._key_list + ["T_78"])
        self.T_79 = _Source(self._key_list + ["T_79"])
        # -----
        self.T_80 = _Source(self._key_list + ["T_80"])
        self.T_81 = _Source(self._key_list + ["T_81"])
        self.T_82 = _Source(self._key_list + ["T_82"])
        self.T_83 = _Source(self._key_list + ["T_83"])
        self.T_84 = _Source(self._key_list + ["T_84"])
        self.T_85 = _Source(self._key_list + ["T_85"])
        self.T_86 = _Source(self._key_list + ["T_86"])
        self.T_87 = _Source(self._key_list + ["T_87"])
        self.T_88 = _Source(self._key_list + ["T_88"])
        self.T_89 = _Source(self._key_list + ["T_89"])
        # -----
        self.T_90 = _Source(self._key_list + ["T_90"])
        self.T_91 = _Source(self._key_list + ["T_91"])
        self.T_92 = _Source(self._key_list + ["T_92"])
        self.T_93 = _Source(self._key_list + ["T_93"])
        self.T_94 = _Source(self._key_list + ["T_94"])
        self.T_95 = _Source(self._key_list + ["T_95"])
        self.T_96 = _Source(self._key_list + ["T_96"])
        self.T_97 = _Source(self._key_list + ["T_97"])
        self.T_98 = _Source(self._key_list + ["T_98"])
        self.T_99 = _Source(self._key_list + ["T_99"])
        # -----
        self.T_100 = _Source(self._key_list + ["T_100"])
        self.T_101 = _Source(self._key_list + ["T_101"])
        self.T_102 = _Source(self._key_list + ["T_102"])
        self.T_103 = _Source(self._key_list + ["T_103"])
        self.T_104 = _Source(self._key_list + ["T_104"])
        self.T_105 = _Source(self._key_list + ["T_105"])
        self.T_106 = _Source(self._key_list + ["T_106"])
        self.T_107 = _Source(self._key_list + ["T_107"])
        self.T_108 = _Source(self._key_list + ["T_108"])
        self.T_109 = _Source(self._key_list + ["T_109"])
        # -----
        self.T_110 = _Source(self._key_list + ["T_110"])

    def Get(self):
        return _CacheFile().Get(self._key_list)

# ==================================================================
class _Metallicity:
    def __init__(self,key_list:list[str]) -> None:
        self._key_list = key_list
        self.Z_00001  = _Age(self._key_list + ["Z_00001"])
        self.Z_0001   = _Age(self._key_list + ["Z_0001"])
        self.Z_001    = _Age(self._key_list + ["Z_001"])
        self.Z_002    = _Age(self._key_list + ["Z_002"])
        self.Z_003    = _Age(self._key_list + ["Z_003"])
        self.Z_004    = _Age(self._key_list + ["Z_004"])
        self.Z_006    = _Age(self._key_list + ["Z_006"])
        self.Z_008    = _Age(self._key_list + ["Z_008"])
        self.Z_010    = _Age(self._key_list + ["Z_010"])
        self.Z_014    = _Age(self._key_list + ["Z_014"])
        self.Z_020    = _Age(self._key_list + ["Z_020"])
        self.Z_030    = _Age(self._key_list + ["Z_030"])
        self.Z_040    = _Age(self._key_list + ["Z_040"])

    def Get(self):
        return _CacheFile().Get(self._key_list)

# ==================================================================
class _Multiplicity:
    def __init__(self,key_list:str) -> None:
        self.Pop_Single     = _Metallicity([key_list+"_SIN"])
        self.Pop_Binary     = _Metallicity([key_list+"_BIN"])


# ==================================================================
class _IMF_SALPETER:
    def __init__(self) -> None:
        self.UPTO_100M = _Multiplicity("SALPETER_100M")

class _IMF_KROUPA:
    def __init__(self) -> None:
        self.UPTO_100M          = _Multiplicity("KROUPA_100M")
        self.UPTO_100M_TOP      = _Multiplicity("KROUPA_100M_TH")
        self.UPTO_100M_BOTTOM   = _Multiplicity("KROUPA_100M_BH")
        
        self.UPTO_300M          = _Multiplicity("KROUPA_300M")
        self.UPTO_300M_TOP      = _Multiplicity("KROUPA_300M_TH")
        self.UPTO_300M_BOTTOM   = _Multiplicity("KROUPA_300M_BH")

class _IMF_CHABRIER:
    def __init__(self) -> None:
        self.UPTO_100M = _Multiplicity("CHABRIER_100M")
        self.UPTO_300M = _Multiplicity("CHABRIER_300M")

# ==================================================================
class CachedSpectra:
    def __init__(self) -> None:
        self.IMF_SALPETER   = _IMF_SALPETER() 
        self.IMF_KROUPA     = _IMF_KROUPA()
        self.IMF_CHABRIER   = _IMF_CHABRIER()


# USE
s = CachedSpectra("abc")
s.IMF_CHABRIER.UPTO_300M.Pop_Binary.Z_014.T_60.StellarFlux()
