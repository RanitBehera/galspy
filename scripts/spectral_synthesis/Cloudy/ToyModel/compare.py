import galspy.utility.Figure.CloudyFigure as cf
import galspec.Cloudy as cd
import matplotlib.pyplot as plt

OUTDIR = "/mnt/home/student/cranit/RANIT/Repo/galspy/study/cloudy/bpass_1Myr/hden"
out=cd.CloudyOutputReader(OUTDIR,"hd5")
cf.CloudySpecAndZone(out)

plt.show()