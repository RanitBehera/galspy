import galspy.utility.Figure.CloudyFigure as cf
import galspec.Cloudy as cd
import matplotlib.pyplot as plt

OUTDIR = "/mnt/home/student/cranit/RANIT/Repo/galspy/study/cloudy/toymodel/eh"
out=cd.CloudyOutputReader(OUTDIR,"eh5")
cf.CloudySpecAndZone(out)

plt.show()