import numpy,os
from typing import Literal
import galspy.FileTypes.BigFile as bf

class _PIGQuery:
    def __init__(self,path) -> None:
        self.path = path

    def GetGroupBlockStartEnd(self,group_id:int,particle_type:Literal["Gas","DarkMatter","Star","Blackhole"]):
        assert group_id>0
        lbt = bf.Column(self.path + os.sep + "FOFGroups/LengthByType").Read()
        lgas,ldm,_,_,lstar,lbh=lbt.T

        if particle_type=="Gas":
            csm = numpy.cumsum(lgas)
            start = csm - lgas
        elif particle_type=="DarkMatter":
            csm = numpy.cumsum(ldm)
            start = csm - ldm
        elif particle_type=="Star":
            cms = numpy.cumsum(lstar)
            start = csm - lstar
        elif particle_type=="Blackhole":
            csm = numpy.cumsum(lbh)
            start = csm - lbh
        else:
            raise ValueError("Unknown Particle Type.")
        

        # group_id is 1 based while index needs to be zero based
        gid = group_id - 1
        return int(start[gid]),int(csm[gid])


