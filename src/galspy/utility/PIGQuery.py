import numpy,os
from typing import Literal
from galspy.MPGadget import _FOFGroups

class _PIGQuery:
    def __init__(self,path) -> None:
        self.path = path

    def GetGroupBlock(self,group_id:int,particle_type:Literal["Gas","DarkMatter","Star","Blackhole"]):
        assert group_id>0
        fof = _FOFGroups(self.path + os.sep + "FOFGroups")
        lbt = fof.LengthByType()
        lgas,ldm,_,_,lstar,lgas=lbt.T

        if particle_type=="Gas":
            csm = 0