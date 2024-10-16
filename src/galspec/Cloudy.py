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

    def InputVariation(self,token:str,values:list[str]):
        if not len(values)==self.vcount:
            raise ValueError(f"Length of list of values {len(values)} doesnot match the expected variation count {self.vcount}.")
        if token in self._MAPTABLE.keys():
            raise ValueError(f"Token {token} for variation already present.")
        self._MAPTABLE[token]=values

    def ReplaceToken(self,token:str,value:str):
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
            print(f"[ {file} ]","Starting ...")

            result = subprocess.run(["cloudy","-r",file],
                    stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            
            print(f"[ {file} ]","Finished.")

            if result.stdout:print(f"[ {file} ]",result.stdout.decode())
            if result.stderr:print(f"[ {file} ]",result.stderr.decode())


        with ThreadPoolExecutor() as executor:
            executor.map(run_cloudy_instance, filenames)





class CloudyOutput:
    def __init__(self,output_dir:str,filename:str) -> None:
        self._output_dir    = output_dir
        self._filename      =  filename

        self._in        = self._output_dir + os.sep + self._filename + ".in"
        self._out       = self._output_dir + os.sep + self._filename + ".out"
        self._ovr       = self._output_dir + os.sep + self._filename + ".ovr"
        self._con       = self._output_dir + os.sep + self._filename + ".con"

        _cols  = [0,1,2,3,4,5,6,7,8]
        _data  = numpy.loadtxt(self._con,delimiter="\t",usecols=_cols).T

        self.Frequency      = _data[0]
        self.Incident       = _data[1]
        self.Transmitted    = _data[2]
        self.DiffuseOut     = _data[3]
        self.NetTrans       = _data[4]
        self.Reflection     = _data[5]
        self.Total          = _data[6]
        self.RefLine        = _data[7]
        self.OutLine        = _data[8]




    