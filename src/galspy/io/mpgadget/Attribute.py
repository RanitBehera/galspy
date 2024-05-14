from typing import Any
import numpy
from galspec.IO.DType import _DTYPE

class _Attr:
    def __init__(self, attrline: str) -> None:
        chunks      = attrline.split(" ")
        self.name   = chunks[0]
        self.DType  = _DTYPE(chunks[1])
        self.dtype  = self.DType()
        self.nmemb  = chunks[2]

        np_chunks   = numpy.array(chunks)
        sqbr_start  = int(numpy.where(np_chunks=='[')[0])
        sqbr_end    = int(numpy.where(np_chunks=="]")[0])
        self.value  = np_chunks[sqbr_start+1:sqbr_end].astype(self.dtype)
        
        if (self.value.size==1): self.value=self.value[0]

    def __str__(self) -> str:
        return str(self.value)
        
    def __repr__(self) -> str:
        return repr(self.value)
    
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.value
