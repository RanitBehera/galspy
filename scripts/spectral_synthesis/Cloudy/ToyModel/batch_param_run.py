from galspec.Cloudy import ConcurrentCloudyRunner
import numpy

SCRIPTSED=\
"""\
table SED "$__SEDFN__"
L(nu) = 21.0 at 1.1 Ryd 
radius linear parsec 3
sphere
hden 2
abundances "HII.abn"
iterate
stop temprature 100
stop pfrac 0.01
set save prefix "$__PREFN__"
save overview ".ovr" last
save continuum ".con" last units Angstrom
save diffuse continuum ".diffcon" last units Angstrom
save grain continuum ".graincon" last units Angstrom
save two photon continuum ".twophcon" last units Angstrom
"""


SCRIPTNH=\
"""\
table SED "es5.sed"
luminosity solar 4
radius linear parsec 3
sphere
hden $__HDEN__
abundances "solar_GASS10.abn"
iterate
stop temprature 100
stop pfrac 0.01
set save prefix "$__PREFN__"
save overview ".ovr" last
save continuum ".con" last units Angstrom
save diffuse continuum ".diffcon" last units Angstrom
save grain continuum ".graincon" last units Angstrom
save two photon continuum ".twophcon" last units Angstrom
"""




# ======================================

# eh = ParameterStudy(SCRIPTSED,5)
# prefix = [f"fs{i+1}" for i in range(5)]     #<---
# eh.Map("$__SEDFN__",[pre+".sed" for pre in prefix])

eh = ConcurrentCloudyRunner(SCRIPTNH,5)
prefix = [f"nh{i+1}" for i in range(5)]     #<---
eh.Map("$__HDEN__",[str(i) for i in range(1,6)])

eh.Map("$__PREFN__",prefix)
OUTPATH = "/mnt/home/student/cranit/RANIT/Repo/galspy/study/cloudy/uveffect/NH"  #<---
eh.RunCloudyAsync(OUTPATH,prefix)
