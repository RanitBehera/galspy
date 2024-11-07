import matplotlib.pyplot as plt
import galspy.utility.Figure.Beautification as bty

from galspec.bpass import BPASSCache


import galspec.Cloudy as gc

OUTDIR = "/mnt/home/student/cranit/RANIT/Repo/galspy/study/cloudy/bpass_sed"
for i in range(0,41):
    # if not i==11:continue
    if i==1:break
    out = gc.CloudyOutputReader(OUTDIR,"t"+str(i))
    con = out.Spectrum.Continuum

    x=con.Frequency # Cloudy call it freq table but we enables units angstrom
    y_in = con.Incident
    yout = con.DiffuseOut
    total = con.Total

    OFFSET = 1#/(10000**i)

    plt.plot(x,y_in * OFFSET,ls='-',lw=1,c='b',alpha=1,label="BPASS SSP")
    plt.plot(x,yout * OFFSET,ls='-',lw=1,c='c',alpha=1,label="Cloudy Nebular")
    plt.plot(x,(y_in+yout) * OFFSET,ls='-',lw=1,c='r',alpha=1,label="Total")

# plt.axvline(1000,color='k',ls='--',lw=1)
plt.xscale('log')
plt.yscale('log')
plt.xlim(100,1e4)
plt.ylim(1e37,1e43)
plt.legend(loc="upper left",frameon=False)
plt.xlabel("Wavelength $(\\AA)$")
plt.ylabel("Flux (ergs s$^{-1}$ $\\AA^{-1}$)")
plt.subplots_adjust(bottom=0.2,left=0.2)

# VERIFY CORRECT INPUT
if False:
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