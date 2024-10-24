from galspec.Cloudy import ConcurrentCloudyRunner
import numpy

with open("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/spectral_synthesis/Cloudy/ToyModel/scriptsed.in","r") as fp:
    SCRIPTSED=fp.read()

eh = ConcurrentCloudyRunner(SCRIPTSED,5)
prefix = [f"eh{i+1}" for i in range(5)]     #<---
eh.Map("$__SEDFN__",[pre for pre in prefix])

OUTPATH = "/mnt/home/student/cranit/RANIT/Repo/galspy/study/cloudy/toymodel/eh"  #<---
eh.RunCloudyAsync(OUTPATH,prefix)
