import matplotlib.pyplot as plt
import galspy.utility.Figure.Beautification as bty

from galspec.bpass import BPASSCache


import galspec.Cloudy as gc

OUTDIR = "/mnt/home/student/cranit/RANIT/Repo/galspy/study/cloudy/bpass_sed"
for i in range(0,41):
    # if not i==11:continue
    if i==1:break
    out = gc.CloudyOutput(OUTDIR,"t"+str(i))
    con = out.Continuum

    x=con.Con.Frequency # Cloudy call it freq table but we enables units angstrom
    y_in = con.Con.Incident/x
    yout = con.Con.DiffuseOut/x
    total = con.Con.Total/x

    OFFSET = 1#/(10000**i)

    plt.plot(x,y_in * OFFSET,ls='-',lw=1,c='b',alpha=0.5)
    # plt.plot(x,yout * OFFSET,ls='-',c='r',alpha=1)
    # plt.plot(x,total * OFFSET,ls='-',c='m',alpha=1)

plt.axvline(1000,color='k',ls='--',lw=1)
plt.xscale('log')
plt.yscale('log')


specs:dict = BPASSCache("cache/bpass_chab_300M.ch").Read()
Z = "0.00001"
Zspecs  = specs[Z]
Tkeys   = specs["T_KEYS"] 
WL      = Zspecs["WL"]

for i,Tkey in enumerate(Tkeys):
    if i==1:break
    # if not i%10==7: continue
    # if Tkey not in ["6.0","6.7","7.0","7.7","8.0","8.7","9.0"]: continue
    OFFSET = 1#/(100**i)
    Tspec   = specs[Z][Tkey]


    X,Y = WL, Tspec 
    plt.plot(X,Y*3.846e33,c='m')




# bty.AttachSpectraLines(plt.gca())

plt.show()