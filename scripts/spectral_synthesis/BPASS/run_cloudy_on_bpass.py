import numpy
import os
from galspec.Cloudy import ConcurrentCloudyRunner

# ================================================================
#                    CLOUDY BATCH SCRIPT
# ================================================================
SCRIPT=\
"""\
table SED "$__SEDFN__.sed"
L(nu) = $__LNORM__ at 0.9120 Ryd 
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

LNORM = [27.232,27.26,27.267,27.283,27.275,27.165,27.085,27.003,26.896,26.788,26.662,26.532,26.399,26.277,26.15,26.024,25.897,25.795,25.675,25.572,25.42,25.296,25.133,24.958,24.787,24.587,24.352,24.094,23.844,23.593,23.404,23.112,22.8,22.328,21.985,21.465,21.563,21.534,21.904,22.076,22.151,22.305,22.19,22.2,22.429,22.299,22.01,22.252,22.084,20.673,19.446]
LNORM = [str(L) for L in LNORM]

script = ConcurrentCloudyRunner(SCRIPT,len(SED_FN))
script.Map("$__SEDFN__",SED_FN)
script.Map("$__LNORM__",LNORM)

script.RunCloudyAsync(OUTDIR,SED_FN)