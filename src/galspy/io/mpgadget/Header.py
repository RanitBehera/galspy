import numpy
from galspec.IO.DType import _DTYPE


class _FieldHeader:
    def __init__(self, path: str) -> None:
        self.path   = path

        with open(self.path) as f:
            self.contents       = f.read()
        
        lines = self.contents.split("\n")[:-1]
        
        self.DType              = _DTYPE(lines[0].split(" ")[1])
        self.DTYPE              = self.DType()

        self.NMEMB              = int(lines[1].split(":")[1])
        self.NFILE              = int(lines[2].split(":")[1])

        self.filenames              = ()
        self.datalength_per_file    = numpy.zeros(len(lines)-3,dtype=int)
        # self.checksum_of_files      = numpy.zeros(len(lines)-3,dtype=int)
        for i in range(3,len(lines)):
            self.filenames+=(lines[i].split(":")[0],)
            self.datalength_per_file[i-3]   = int(lines[i].split(":")[1])
            # self.checksum_of_files[i-3]     = int(lines[i].split(":")[3])

        self.total_data_length         = sum(self.datalength_per_file)

    def __str__(self) -> str:
        return self.contents

    def __repr__(self) -> str:
        return self.contents