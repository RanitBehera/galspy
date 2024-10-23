import numpy
import os
from galspec.Cloudy import ConcurrentCloudyRunner

# ================================================================
#                    CLOUDY BATCH SCRIPT
# ================================================================
SCRIPT=\
"""\
table SED "$__SEDFN__.sed"
L(nu) = $__LNORM__ at 456.0 Ryd 
radius linear parsec 3
sphere
hden 2
abundances "solar_GASS10.abn"
iterate
stop temprature 100
stop pfrac 0.01
set save prefix "$__SEDFN__"
save overview ".ovr" last
save continuum ".con" last units Angstrom
save diffuse continuum ".diffcon" last units Angstrom
save grain continuum ".graincon" last units Angstrom
save two photon continuum ".twophcon" last units Angstrom
"""
# ==================================================================

# ==================================================================
OUTDIR = "/mnt/home/student/cranit/RANIT/Repo/galspy/study/cloudy/bpass_sed"

# Auto-detect ".sed" files
SED_FN  = [cld.removesuffix(".sed") for cld in os.listdir(OUTDIR) 
           if os.path.isfile(OUTDIR+os.sep+cld) and cld.endswith(".sed")]

LNORM = [-23.405,-23.404,-23.404,-22.423,-21.728,-21.585,-21.453,-21.68,-22.031,-22.419,-22.616,-22.685,-22.86,-22.759,-22.852,-22.854,-22.836,-22.734,-22.31,-21.952,-21.717,-21.978,-21.812,-21.986,-21.946,-22.104,-22.104,-22.328,-22.296,-22.264,-22.28,-22.547,-22.709,-22.71,-22.759,-22.822,-22.86,-23.115,-23.014,-23.042,-23.353,-23.017,-23.493,-23.531,-23.5,-23.458,-23.461,-23.755,-23.494,-23.905,-24.655]
LNORM = [str(L) for L in LNORM]

script = ConcurrentCloudyRunner(SCRIPT,len(SED_FN))
script.Map("$__SEDFN__",SED_FN)
script.Map("$__LNORM__",LNORM)

script.RunCloudyAsync(OUTDIR,SED_FN)