import numpy, struct
from typing import Literal

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

        attr_v2_dict={}
        struct_dtype_map={
            'i4':'i','i8':'q',
            'u4':'I','u8':'Q',
            'f4':'f','f8':'d',
            'S1':'c',}
        for line in attr_v2.split("\n"):
            if line=="":continue
            chunks = line.split(" ")
            fmt=chunks[1][0] + struct_dtype_map[chunks[1][1:]]*int(chunks[2])
            attr_v2_dict[chunks[0]]=struct.unpack(fmt,bytes.fromhex(chunks[3]))[0]
        
        return attr_v2_dict
