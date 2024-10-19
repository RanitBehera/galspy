import os
import numpy
import pathlib

import subprocess
from concurrent.futures import ThreadPoolExecutor


class ParameterStudy:
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




class _DiffuseContinuum:
    def __init__(self,filename):
        self.filename = filename
        _data  = numpy.loadtxt(self.filename).T
        self.Energy                 = _data[0] 
        self.ConEmitLocal           = _data[1] 
        self.DiffuseLineEmission    = _data[2] 
        self.Total                  = _data[3] 

class _GrainContinuum:
    def __init__(self,filename):
        self.filename = filename
        _data  = numpy.loadtxt(self.filename).T
        self.Energy     = _data[0] 
        self.Grapahite  = _data[1] 
        self.Rest       = _data[2] 
        self.Total      = _data[3] 

class _TwoPhotonContinuum:
    def __init__(self,filename):
        self.filename = filename
        _data  = numpy.loadtxt(self.filename).T
        self.Energy     = _data[0] 
        self.Nu         = _data[1] 
        self.NuFnu      = _data[2] 


class _Con:
    def __init__(self,filename):
        self.filename = filename

        _cols  = [0,1,2,3,4,5,6,7,8]
        _data  = numpy.loadtxt(filename,delimiter="\t",usecols=_cols).T
        self.Frequency      = _data[0]
        self.Incident       = _data[1]
        self.Transmitted    = _data[2]
        self.DiffuseOut     = _data[3]
        self.NetTrans       = _data[4]
        self.Reflection     = _data[5]
        self.Total          = _data[6]
        self.RefLine        = _data[7]
        self.OutLine        = _data[8]

class _Continuum:
    def __init__(self,output_dir:str,filename:str):
        self._output_dir    = output_dir
        self._filename      =  filename
        _con       = self._output_dir + os.sep + self._filename + ".con"
        _diffcon   = self._output_dir + os.sep + self._filename + ".diffcon"
        _graincon   = self._output_dir + os.sep + self._filename + ".graincon"
        _twophcon   = self._output_dir + os.sep + self._filename + ".twophcon"

        self.Con        = _Con(_con)
        self.Diffuse    = _DiffuseContinuum(_diffcon)
        self.Grain      = _GrainContinuum(_graincon)
        self.TwoPhoton  = _TwoPhotonContinuum(_twophcon)






class CloudyOutput:
    def __init__(self,output_dir:str,filename:str) -> None:
        self._output_dir    = output_dir
        self._filename      =  filename


        self.Continuum  = _Continuum(output_dir,filename)


        # Temporary
        _in        = self._output_dir + os.sep + self._filename + ".in"
        _out       = self._output_dir + os.sep + self._filename + ".out"
        _ovr       = self._output_dir + os.sep + self._filename + ".ovr"


        




    