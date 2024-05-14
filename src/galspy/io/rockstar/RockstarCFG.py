import numpy

class _RockstarCFG:
    def __init__(self, path: str) -> None:
        self.path   = path

        with open(self.path) as f:
            self.contents       = f.read()
        
        lines = self.contents.split("\n")[:-1]
        temp_dict = {} 
        for line in lines:
            key,value = line.split("=")
            key,value = key.strip(),value.strip()
            temp_dict[key]=value

        self.MIN_HALO_PARTICLES     = numpy.int64(temp_dict["MIN_HALO_PARTICLES"])
        self.MIN_HALO_OUTPUT_SIZE   = numpy.int64(temp_dict["MIN_HALO_OUTPUT_SIZE"])
        self.INBASE                 = temp_dict["INBASE"][1:-1]
        self.OUTBASE                = temp_dict["OUTBASE"][1:-1]


    def __str__(self) -> str:
        return self.contents

    def __repr__(self) -> str:
        return self.contents