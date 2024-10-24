import galspy.utility.Figure.CloudyFigure as cf
import galspec.Cloudy as cd

OUTDIR = "/mnt/home/student/cranit/RANIT/Repo/galspy/study/cloudy/toymodel/eh"
out=cd.CloudyOutputReader(OUTDIR,"eh1")
cf.CloudyOverview([out])