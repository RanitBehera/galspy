import matplotlib.pyplot as plt
# import bpass_spectra_evolution

import galspec.Cloudy as gc

OUTDIR = "/mnt/home/student/cranit/RANIT/Repo/galspy/study/cloudy/bpass_sed"
for i in range(11):
    if i==2:break
    out = gc.CloudyOutput(OUTDIR,"t"+str(i))
    con = out.Continuum

    plt.plot(con.Con.Frequency,con.Con.Incident/con.Con.Frequency,ls='-',lw=1,c='b',alpha=1)
    plt.plot(con.Con.Frequency,con.Con.DiffuseOut/con.Con.Frequency,ls='-',c='r',alpha=1)
    # plt.plot(con.Con.Frequency,con.Con.Reflection/con.Con.Frequency,ls='--',c='k',alpha=1)
plt.xscale('log')
plt.yscale('log')
plt.show()