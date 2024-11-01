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
        self._usecols   = usecols
        self._filedata  = None
        self._filetext  = None

    def _GetColumn(self,index):
        if self._filedata is None:
            if not os.path.exists(self.filepath):
                raise FileNotFoundError(f"File {self.filepath} doesn't exist.")
            else:
                self._filedata  = numpy.loadtxt(self.filepath,delimiter="\t",usecols=self._usecols).T
        
        return self._filedata[index]

    def _GetText(self):
        if self._filetext is None:
            if not os.path.exists(self.filepath):
                raise FileNotFoundError(f"File {self.filepath} doesn't exist.")
            else:
                with open(self.filepath,'r') as fp:
                    self._filetext = fp.read()
        
        return self._filetext
    
     


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
    def n_Nu(self):         return self._GetColumn(1)
    @property
    def nuFnu(self):      return self._GetColumn(2)


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
        
        self.DiffuseContinuum   = _DiffuseContinuum(self._filepath + ".diffcon")
        # self.GrainContinuum     = _GrainContinuum(self._filepath + ".graincon")
        self.TwoPhotonContinuum = _TwoPhotonContinuum(self._filepath + ".twophcon")


class _Element:
    def __init__(self,filepath):
        self.Hydrogen   = _ElementHydrogen(filepath + ".is_H")
        self.Helium     = _ElementHelium(filepath + ".is_He")
        self.Carbon     = _ElementCarbon(filepath + ".is_C")
        self.Nitrogen   = _ElementNitrogen(filepath + ".is_N")
        self.Oxygen     = _ElementOxygen(filepath + ".is_O")


class _Output(_FileReader):
    def __init__(self, filepath):
        super().__init__(filepath)
        self._text = None
        self._parsed=False


    def _read_if_not_already(self):
        if self._text is None:
            with open(self.filepath,"r") as fp:
                self._text = fp.readlines() 

    def _Parse(self):
        if self._parsed: return
        self._parsed = True

        self._read_if_not_already()

        _zone_block_start=[]
        for i,line in enumerate(self._text):
            line=line.strip()
            if line.startswith("#"):
                _zone_block_start.append(i)
            elif line.startswith("Intrinsic line intensities"):
                self._int_line_start=i
            elif line.startswith("Emergent line intensities"):
                self._int_line_end=i-1
                self._emg_line_start=i

        
        self._zone_block_start=_zone_block_start



    # # TODO : Improve
    @property
    def InnerRadius(self):
        self._inn_rad=None
        if self._text is None and self._inn_rad is None:
            with open(self.filepath,"r") as fp:
                self._text = fp.read() 

        self._text=self._text.split('\n')
        self._text=self._text[:100]
        target_line = ""
        for line in self._text:
            line:str

            if "radius" in line:
                target_line=line
                break
        
        target_line = target_line.strip()[1:-1].strip()
        target_chunks = target_line.split(" ")

        rad_inn = float(target_chunks[-1])
        return rad_inn


class _LineListIntensity(_FileReader):
    def __init__(self, filepath):
        super().__init__(filepath)
        self._parsed=False
        self._lines = {}

    def _Parse(self):
        if self._parsed: return
        
        text = self._GetText()
        text = text.split('\n')[2:]
        for line in text:
            if line.strip()=="":continue
            lam,rel_int=line.split()[2:4]
            self._lines[lam]=float(rel_int)
        
        self._parsed = True

    @property
    def H_alpha(self):self._Parse();return self._lines["6562.80A"]
    @property
    def H_beta(self):self._Parse();return self._lines["4861.32A"]






class CloudyOutputReader:
    def __init__(self,output_dir:str,filename:str) -> None:
        self._output_dir    = output_dir
        self._filename      =  filename

        self.Overview   = _Overview(output_dir+os.sep+filename+".ovr")
        self.Spectrum   = _Spectrum(output_dir+os.sep+filename)
        self.Elements   = _Element(output_dir+os.sep+filename)

        self.Output     = _Output(output_dir+os.sep+filename + ".out")
        self.Lines      = _LineListIntensity(output_dir+os.sep+filename + ".lines")


    

# if __name__ == "__main__":
#     out = _Output("/mnt/home/student/cranit/RANIT/Repo/galspy/study/cloudy/bpass_ri/r1.out")
#     print(out.InnerRadius)