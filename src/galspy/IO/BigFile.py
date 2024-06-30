import numpy, struct, os
from typing import Literal
from multiprocessing import Pool

class Attribute:
    """
    This class helps reading and writing the Attribute (attr-v2) for bigfile.

    Attributes:
        path (str): The path of the attributr (attr-v2) file.
    """

    def __init__(self,path:str) -> None:
        self.path = path
        """The path of the attributr (attr-v2) file."""

    def Read(self,plain_text:bool=False):

        with open(self.path) as f:
            attr_v2=f.read()
        
        if plain_text:return attr_v2

        struct_dtype_map={'i4':'i','i8':'q','u4':'I','u8':'Q','f4':'f','f8':'d','S1':'c',}
        attr_v2_dict={}
        for line in attr_v2.split("\n"):
            if line=="":continue
            chunks      = line.split(" ")

            key         = chunks[0]
            endianess   = chunks[1][0]
            dtype       = chunks[1][1:]
            length      = int(chunks[2])

            fmt = endianess + struct_dtype_map[dtype]*length
            val = list(struct.unpack(fmt,bytes.fromhex(chunks[3])))
            
            if dtype=='S1':val=b''.join(val)#.decode("utf-8")
            if length==1:val=val[0]
            
            attr_v2_dict[key]= val

        return attr_v2_dict


class Header:
    def __init__(self,path:str) -> None:
        self.path = path
        """The path of the header file."""

    def Read(self,plain_text:bool=False):
        with open(self.path) as f:
            header=f.read()
        
        if plain_text:return header

        lines = header.split("\n")

        header_dict={}
        header_dict["DTYPE"] = lines[0].split(" ")[1]
        header_dict["NMEMB"] = int(lines[1].split(":")[1])
        header_dict["NFILE"] = int(lines[2].split(":")[1])

        for i in range(3,len(lines)):
            if lines[i]=="":continue
            filename,rowlen,_,_=lines[i].split(":")
            header_dict[filename] = int(rowlen.strip())
           
        return header_dict


# -----------------------------------------------------
class Blob:
    def __init__(self,path:str,dtype:str) -> None:
        self.path = path
        self.dtype = dtype

    def Read(self):
        with open(self.path,mode="rb") as file:
            return numpy.fromfile(file,dtype=self.dtype)
        
def ReadBlobWrapper(path_n_type):
    return Blob(path_n_type[0],path_n_type[1]).Read()



# -----------------------------------------------------
class Column:
    def __init__(self,path:str) -> None:
        self.path = path
    
    def Read(self,parallel=False):
        header = Header(os.path.join(self.path,"header")).Read()
        dtype = header["DTYPE"]
        nmemb = header["NMEMB"]
        nfile = header["NFILE"]

        filenames = [("{:X}".format(i)).upper().rjust(6,'0') for i in range(nfile)]
        rowlen_per_blob = [header[fn] for fn in filenames]
        rowlen = sum(rowlen_per_blob)
        
        if not parallel:
            data = numpy.empty(rowlen*nmemb,dtype=dtype)
            for i in range(nfile):
                blob_start  = nmemb * sum(rowlen_per_blob[0:i])
                blob_end    = nmemb * sum(rowlen_per_blob[0:i+1])
                blob_path   = os.path.join(self.path,filenames[i])
                data[blob_start:blob_end] = Blob(blob_path,dtype).Read()    
            if nmemb>1: data = data.reshape(rowlen,nmemb)
            return data
        else:
            blob_paths = [(os.path.join(self.path,fn),dtype) for fn in filenames]
            with Pool(nfile) as p:
                blobs = p.map(ReadBlobWrapper,blob_paths)
            data=numpy.array(blobs).flatten()
            # data=numpy.array(blobs).ravel()
            if nmemb>1: data = data.reshape(rowlen,nmemb)
            return data
            
        



    
