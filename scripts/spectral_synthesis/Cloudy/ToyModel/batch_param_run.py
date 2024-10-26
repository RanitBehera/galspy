from galspec.Cloudy import ConcurrentCloudyRunner
import numpy

# with open("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/spectral_synthesis/Cloudy/ToyModel/scriptsed.in","r") as fp:
with open("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/spectral_synthesis/BPASS/bpass_cloudy.in","r") as fp:
    SCRIPTSED=fp.read()

eh = ConcurrentCloudyRunner(SCRIPTSED,5)
prefix = [f"ri{i+1}" for i in range(5)]     #<---
eh.Map("$__RADIN__",[str(ri) for ri in [0.1,0.5,1,3,5]])
eh.Map("$__FN__",prefix)

# OUTPATH = "/mnt/home/student/cranit/RANIT/Repo/galspy/study/cloudy/toymodel/abund"  #<---
OUTPATH = "/mnt/home/student/cranit/RANIT/Repo/galspy/study/cloudy/bpass_1Myr/ri"  #<---
eh.RunCloudyAsync(OUTPATH,prefix)
