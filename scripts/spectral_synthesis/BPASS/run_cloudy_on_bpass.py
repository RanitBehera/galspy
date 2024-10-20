import numpy
import os
from galspec.Cloudy import ConcurrentCloudyRunner

# ================================================================
#                    CLOUDY BATCH SCRIPT
# ================================================================
SCRIPT=\
"""\
table SED "$__SEDFN__.sed"
L(nu) = 21.0 at 1.1 Ryd 
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

script = ConcurrentCloudyRunner(SCRIPT,len(SED_FN))
script.Map("$__SEDFN__",SED_FN)
script.RunCloudyAsync(OUTDIR,SED_FN)