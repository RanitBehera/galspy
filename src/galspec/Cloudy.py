import os
import numpy
import pathlib

import subprocess
from concurrent.futures import ProcessPoolExecutor,ThreadPoolExecutor


class ConcurrentCloudyRunner:
    def __init__(self,input_script:str,variation_count:int):
        self.script=input_script
        self.vcount=variation_count

        self._MAPTABLE = {}
        self._REPTABLE = {} #Replace Table for Macros

    def Map(self,token:str,values:list[str]):
        if not len(values)==self.vcount:
            raise ValueError(f"Length of list of values {len(values)} doesnot match the expected variation count {self.vcount}.")
        if token in self._MAPTABLE.keys():
            raise ValueError(f"Token {token} for variation already present.")
        self._MAPTABLE[token]=values

    def Replace(self,token:str,value:str):
        if token in self._REPTABLE.keys():
            raise ValueError(f"Token '{token}' for replacement to '{self._REPTABLE[token]}' already present.")
        self._REPTABLE[token]=value

    def GenerateInputFiles(self,outdir:str,filenames:list[str]):
        if not len(filenames)==self.vcount:
            raise ValueError(f"Length of list of filenames {len(filenames)} doesnot match the expected variation count {self.vcount}.")

        pathlib.Path(outdir).mkdir(parents=True,exist_ok=True)

        for i in range(self.vcount):
            filepath = outdir + os.sep + filenames[i] + ".in"
            MSCRIPT = self.script

            for token,value in self._REPTABLE.items():
                MSCRIPT = MSCRIPT.replace(token,value)

            for token,value in self._MAPTABLE.items():
                MSCRIPT = MSCRIPT.replace(token,value[i])

            with open(filepath,"w") as fp:
                fp.write(MSCRIPT)


    def RunCloudyAsync(self,outdir:str,filenames:list[str]):
        self.GenerateInputFiles(outdir,filenames)


        def run_cloudy_instance(script_name:str):
            file = script_name
            if file.endswith(".in"):file.removesuffix(".in")

            os.chdir(outdir)
            print(f"[ {file} ]","Running ...")

            result = subprocess.run(["cloudy","-r",file],
                    stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            
            print(f"[ {file} ]","Finished.")

            if result.stdout:print(f"[ {file} ]",result.stdout.decode())
            if result.stderr:print(f"[ {file} ]",result.stderr.decode())


        with ThreadPoolExecutor() as executor:
            executor.map(run_cloudy_instance, filenames)

# =============================================================================

class _FileReader:
    def __init__(self,filepath,usecols=None):
        self.filepath   = filepath
        self._usecols    = usecols
        self._data      = None

    def _GetColumn(self,index):
        if self._data is None:
            if not os.path.exists(self.filepath):
                raise FileNotFoundError(f"File {self.filepath} doesn't exist.")
            else:
                self._data  = numpy.loadtxt(self.filepath,delimiter="\t",usecols=self._usecols).T
        
        return self._data[index]


class _DiffuseContinuum(_FileReader):
    def __init__(self,filepath):
        super().__init__(filepath)

    @property
    def Energy(self):       return self._GetColumn(0)
    @property
    def ConEmitLocal(self): return self._GetColumn(1)
    @property
    def DiffuseLineEmission(self): return self._GetColumn(2)
    @property
    def Total(self):        return self._GetColumn(3)

class _GrainContinuum(_FileReader):
    def __init__(self,filepath):
        super().__init__(filepath)

    @property
    def Energy(self):     return self._GetColumn(0) 
    @property
    def Grapahite(self):  return self._GetColumn(1) 
    @property
    def Rest(self):       return self._GetColumn(2) 
    @property
    def Total(self):      return self._GetColumn(3) 

class _TwoPhotonContinuum(_FileReader):
    def __init__(self,filepath):
        super().__init__(filepath)

    @property
    def Energy(self):     return self._GetColumn(0)
    @property
    def Nu(self):         return self._GetColumn(1)
    @property
    def NuFnu(self):      return self._GetColumn(2)


class _Continuum(_FileReader):
    def __init__(self,filepath):
        super().__init__(filepath,[0,1,2,3,4,5,6,7,8])

    @property
    def Frequency(self): return self._GetColumn(0)    
    @property
    def Incident(self): return self._GetColumn(1)/self._GetColumn(0)
    @property
    def Transmitted(self): return self._GetColumn(2)/self._GetColumn(0)
    @property
    def DiffuseOut(self): return self._GetColumn(3)/self._GetColumn(0)
    @property
    def NetTrans(self): return self._GetColumn(4)/self._GetColumn(0)
    @property
    def Reflection(self): return self._GetColumn(5)/self._GetColumn(0)
    @property
    def Total(self): return self._GetColumn(6)/self._GetColumn(0)
    @property
    def RefLine(self): return self._GetColumn(7)/self._GetColumn(0)
    @property
    def OutLine(self): return self._GetColumn(8)/self._GetColumn(0)


class _ElementHydrogen(_FileReader):
    def __init__(self,filepath):
        super().__init__(filepath)
    
    @property
    def Depth(self): return self._GetColumn(0)
    @property
    def HI(self): return self._GetColumn(1)
    @property
    def HII(self): return self._GetColumn(2)
    @property
    def H2(self): return self._GetColumn(3)

class _ElementHelium(_FileReader):
    def __init__(self,filepath):
        super().__init__(filepath)
    
    @property
    def Depth(self): return self._GetColumn(0)
    @property
    def HeI(self): return self._GetColumn(1)
    @property
    def HeII(self): return self._GetColumn(2)
    @property
    def HeIII(self): return self._GetColumn(3)

class _ElementCarbon(_FileReader):
    def __init__(self,filepath):
        super().__init__(filepath)

    @property
    def Depth(self): return self._GetColumn(0)
    @property
    def CI(self): return self._GetColumn(1)
    @property
    def CII(self): return self._GetColumn(2)
    @property
    def CIII(self): return self._GetColumn(3)
    @property
    def CIV(self): return self._GetColumn(4)
    @property
    def CV(self): return self._GetColumn(5)
    @property
    def CVI(self): return self._GetColumn(6)
    @property
    def CVII(self): return self._GetColumn(7)

class _ElementNitrogen(_FileReader):
    def __init__(self,filepath):
        super().__init__(filepath)

    @property
    def Depth(self): return self._GetColumn(0)
    @property
    def NI(self): return self._GetColumn(1)
    @property
    def NII(self): return self._GetColumn(2)
    @property
    def NIII(self): return self._GetColumn(3)
    @property
    def NIV(self): return self._GetColumn(4)
    @property
    def NV(self): return self._GetColumn(5)
    @property
    def NVI(self): return self._GetColumn(6)
    @property
    def NVII(self): return self._GetColumn(7)
    @property
    def NVIII(self): return self._GetColumn(8)

class _ElementOxygen(_FileReader):
    def __init__(self,filepath):
        super().__init__(filepath)

    @property
    def Depth(self): return self._GetColumn(0)
    @property
    def OI(self): return self._GetColumn(1)
    @property
    def OII(self): return self._GetColumn(2)
    @property
    def OIII(self): return self._GetColumn(3)
    @property
    def OIV(self): return self._GetColumn(4)
    @property
    def OV(self): return self._GetColumn(5)
    @property
    def OVI(self): return self._GetColumn(6)
    @property
    def OVII(self): return self._GetColumn(7)
    @property
    def OVIII(self): return self._GetColumn(8)
    @property
    def OIX(self): return self._GetColumn(9)

class _Overview(_FileReader):
    def __init__(self, filepath):
        super().__init__(filepath)
    
    @property
    def Depth(self): return self._GetColumn(0)
    @property
    def TemperatureElectron(self): return self._GetColumn(1)
    @property
    def HeatingTotal(self): return self._GetColumn(2)
    @property
    def HydrogenDensity(self): return self._GetColumn(3)
    @property
    def ElectronDensity(self): return self._GetColumn(4)
    @property
    def H2MoleculeFraction(self): return self._GetColumn(5)
    @property
    def HI_Fraction(self): return self._GetColumn(6)
    @property
    def HII_Fraction(self): return self._GetColumn(7)
    @property
    def HeI(self): return self._GetColumn(8)
    @property
    def HeII(self): return self._GetColumn(9)
    @property
    def HeIII(self): return self._GetColumn(10)
    @property
    def CO_O(self): return self._GetColumn(11)
    @property
    def CI(self): return self._GetColumn(12)
    @property
    def CII(self): return self._GetColumn(13)
    @property
    def CIII(self): return self._GetColumn(14)
    @property
    def CIV(self): return self._GetColumn(15)
    @property
    def OI(self): return self._GetColumn(16)
    @property
    def OII(self): return self._GetColumn(17)
    @property
    def OIII(self): return self._GetColumn(18)
    @property
    def OIV(self): return self._GetColumn(19)
    @property
    def OV(self): return self._GetColumn(20)
    @property
    def OVI(self): return self._GetColumn(21)
    @property
    def H20_O(self): return self._GetColumn(22)
    @property
    def AV_Point(self): return self._GetColumn(23)
    @property
    def AV_Extended(self): return self._GetColumn(24)
    @property
    def Tau_912(self): return self._GetColumn(25)

# =================================================================

class _Spectrum:
    def __init__(self,filepath:str):
        self._filepath      =  filepath

        self.Continuum          = _Continuum(self._filepath + ".con")
        
        # self.DiffuseContinuum   = _DiffuseContinuum(self._filepath + ".diffcon")
        # self.GrainContinuum     = _GrainContinuum(self._filepath + ".graincon")
        # self.TwoPhotonContinuum = _TwoPhotonContinuum(self._filepath + ".twophcon")


class _Element:
    def __init__(self,filepath):
        pass
        self.Hydrogen   = _ElementHydrogen(filepath + ".is_H")
        self.Helium     = _ElementHelium(filepath + ".is_He")
        self.Carbon     = _ElementCarbon(filepath + ".is_C")
        self.Nitrogen   = _ElementNitrogen(filepath + ".is_N")
        self.Oxygen     = _ElementOxygen(filepath + ".is_O")

class _Overview:
    pass

class CloudyOutputReader:
    def __init__(self,output_dir:str,filename:str) -> None:
        self._output_dir    = output_dir
        self._filename      =  filename

        self.Overview   = _Overview()
        self.Spectrum   = _Spectrum(output_dir+os.sep+filename)
        self.Elements   = _Element(output_dir+os.sep+filename)





    