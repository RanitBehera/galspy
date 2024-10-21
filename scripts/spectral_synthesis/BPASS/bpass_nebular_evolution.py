import matplotlib.pyplot as plt
import galspy.utility.Figure.Beautification as bty
# import bpass_spectra_evolution
from galspec.bpass import BPASSCache

import galspec.Cloudy as gc

OUTDIR = "/mnt/home/student/cranit/RANIT/Repo/galspy/study/cloudy/bpass_sed"
for i in range(0,41):
    # if not i==11:continue
    if i==1:break
    out = gc.CloudyOutput(OUTDIR,"t"+str(i))
    con = out.Continuum

    x=con.Con.Frequency
    y_in = con.Con.Incident/con.Con.Frequency
    yout = con.Con.DiffuseOut/con.Con.Frequency
    total = con.Con.Total/con.Con.Frequency

    OFFSET = 1#/(10000**i)

    plt.plot(x,y_in * OFFSET,ls='-',lw=1,c='b',alpha=0.5)
    # plt.plot(x,yout * OFFSET,ls='-',c='r',alpha=1)
    # plt.plot(x,total * OFFSET,ls='-',c='m',alpha=1)

plt.axvline(1013.33,color='k',ls='--',lw=1)
plt.xscale('log')
plt.yscale('log')


bty.AttachSpectraLines(plt.gca())




# Check for Correct Input
if True:
    specs:dict = BPASSCache("cache/bpass_chab_300M.ch").Read()
    Z="0.00001"
    Zspecs  = specs[Z]
    Tkeys   = specs["T_KEYS"] 
    WL      = Zspecs["WL"]
    for i,Tkey in enumerate(Tkeys):
        if i==1:break
        # if not i%10==7: continue
        OFFSET = 1#/(10000**i)
        Tspec   = specs[Z][Tkey] *3.846e33

        plt.plot(WL,(Tspec * OFFSET),c='g')


plt.axvscale()

plt.show()