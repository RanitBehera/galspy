import os
import numpy

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


