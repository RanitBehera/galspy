from galspec.Cloudy import ParameterStudy

SCRIPT=\
"""\
table SED "$__SEDFN__"
luminosity solar 4
radius linear parsec 3
sphere
hden 4
abundances "HII.abn"
iterate
stop temprature 100
stop pfrac 0.01
set save prefix "$__PREFN__"
save overview ".ovr" last
save continuum ".con" last units Angstrom
"""


eh = ParameterStudy(SCRIPT,5)
prefix = [f"es{i+1}" for i in range(5)]
eh.InputVariation("$__SEDFN__",[pre+".sed" for pre in prefix])
eh.InputVariation("$__PREFN__",prefix)

OUTPATH = "/mnt/home/student/cranit/RANIT/Repo/galspy/study/cloudy/uveffect/ES"
eh.RunCloudyAsync(OUTPATH,prefix)
