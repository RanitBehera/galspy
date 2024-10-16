import galspec.Cloudy as gc
import numpy
import matplotlib.pyplot as plt

CLOUDY_DIR = "/mnt/home/student/cranit/RANIT/Repo/galspy/study/cloudy/sed"
con = gc.CloudyOutput(CLOUDY_DIR,"test")

def ConvertToWavelength(freq,flux_nu):
    pass

plt.plot(con.Frequency,con.Incident,label="Incident")
plt.plot(con.Frequency,con.Transmitted,label="Transmitted")
plt.plot(con.Frequency,con.DiffuseOut,label="DiffuseOut")
plt.plot(con.Frequency,con.NetTrans,label="NetTrans")
plt.plot(con.Frequency,con.Reflection,label="Reflection")
plt.plot(con.Frequency,con.Total,label="Total")
plt.xscale('log')
plt.yscale('log')
plt.legend()
plt.show()