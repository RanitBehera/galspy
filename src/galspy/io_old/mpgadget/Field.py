import os,numpy
from typing import Any
from galspec.navigation.base.Folder import _Folder
from galspec.IO.Header import _FieldHeader
from galspec.IO.BinaryFile import _BinaryFile

# --- Base Field Class
# class _FieldOld:
#     def __init__(self,parent_dir):
#         # Knowling field name is required to take different actions based on field under same name
#         self.field_name     = self.__class__.__name__.split("_")[-1]     # str
#         self.path           = parent_dir + os.sep + self.field_name
#         self.parent_path    = parent_dir

#     def __call__(self, *args: Any, **kwds: Any) -> Any:
#         return galspec._ReadFieldWithNumpy(self)
#         # return galspec._ReadFieldWithBigFile(self)

class _Field(_Folder):
    def __init__(self, path: str) -> None:
        super().__init__(path)
    
    def _ReadWithNumpy(self):
        header = _FieldHeader(os.path.join(self.path,"header"))
        data=numpy.zeros(header.total_data_length*header.NMEMB,dtype=header.DTYPE)
        for i in range(0,header.NFILE):
            filename = ("{:X}".format(i)).upper().rjust(6,'0')  
            file = _BinaryFile(os.path.join(self.path,filename),header.DTYPE)
            fill_start_index = sum(header.datalength_per_file[0:i])   * header.NMEMB
            fill_end_index   = sum(header.datalength_per_file[0:i+1]) * header.NMEMB
            data[fill_start_index:fill_end_index]=file.Read()
        if header.NMEMB>1: data = data.reshape(header.total_data_length,header.NMEMB)
        return data

    def _ReadWithBigFile(self):
        print(self.path,flush=True)
        raise NotImplementedError

    def Read(self):
        return self._ReadWithNumpy()
        # self._ReadWithBigFile()
    
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.Read()

