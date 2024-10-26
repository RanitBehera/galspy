import numpy
import os
from galspec.Cloudy import ConcurrentCloudyRunner

INFILE = "/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/spectral_synthesis/BPASS/bpass_cloudy.in"
OUTDIR = "/mnt/home/student/cranit/RANIT/Repo/galspy/study/cloudy/bpass_1Myr/hden"

with open(INFILE,"r") as fp:SCRIPT=fp.read()


# Auto-detect ".sed" files
# SED_FN  = [cld.removesuffix(".sed") for cld in os.listdir(OUTDIR) 
#            if os.path.isfile(OUTDIR+os.sep+cld) and cld.endswith(".sed")]

# SED_FN = sorted(SED_FN,key=lambda x: int(x[1:]))

# LNORM = [-23.405,-23.404,-23.404,-22.423,-21.728,-21.585,-21.453,-21.68,-22.031,-22.419,-22.616,-22.685,-22.86,-22.759,-22.852,-22.854,-22.836,-22.734,-22.31,-21.952,-21.717,-21.978,-21.812,-21.986,-21.946,-22.104,-22.104,-22.328,-22.296,-22.264,-22.28,-22.547,-22.709,-22.71,-22.759,-22.822,-22.86,-23.115,-23.014,-23.042,-23.353,-23.017,-23.493,-23.531,-23.5,-23.458,-23.461,-23.755,-23.494,-23.905,-24.655]
# LNORM = [str(L) for L in LNORM]

script = ConcurrentCloudyRunner(SCRIPT,5)
# script.Map("$__SEDFN__",SED_FN)
# script.Map("$__LNORM__",LNORM)

RADIN = [str(ri) for ri in [0.1,0.5,1,3,5]]
HDEN = [str(hd) for hd in [1,2,3,4,5]]
FN = ["hd1","hd2","hd3","hd4","hd5"]
# script.Map("$__RADIN__",RADIN)
script.Map("$__HDEN__",HDEN)
script.Map("$__FN__",FN)
script.RunCloudyAsync(OUTDIR,FN)