import numpy as np
import matplotlib.pyplot as plt
import galspec.Cloudy as cd

import galspec.Utility as gu

PATH = "/mnt/home/student/cranit/RANIT/Repo/galspy/study/cloudy/bpass_sed2"
fig,ax = plt.subplots(1,2,figsize=(10,5))


lb_flx_in = []
lb_flx_out = []
lb_flx_tot = []

hb_flx_in = []
hb_flx_out = []
hb_flx_tot = []

beta_in=[]
beta_out=[]
beta_tot=[]


LB_LAM = 1450
HB_LAM = 2550
RANGE = 50

for i in range(51):
    print(i)
    cloud = cd.CloudyOutputReader(PATH,f"t{i}")

    con = cloud.Spectrum.Continuum
    # ================
    _beta_in = gu.TwoBandSlopeFinder(con.Frequency,con.Incident,LB_LAM,HB_LAM,RANGE,RANGE)
    _beta_out = gu.TwoBandSlopeFinder(con.Frequency,con.DiffuseOut,LB_LAM,HB_LAM,RANGE,RANGE)
    _beta_tot = gu.TwoBandSlopeFinder(con.Frequency,con.Total,LB_LAM,HB_LAM,RANGE,RANGE)
    beta_in.append(_beta_in)
    beta_out.append(_beta_out)
    beta_tot.append(_beta_tot)
    # ================
    _lb_flx_in = gu.BandFluxFinder(con.Frequency,con.Incident,LB_LAM,RANGE)
    _lb_flx_out = gu.BandFluxFinder(con.Frequency,con.DiffuseOut,LB_LAM,RANGE)
    _lb_flx_tot = gu.BandFluxFinder(con.Frequency,con.Total,LB_LAM,RANGE)
    lb_flx_in.append(_lb_flx_in)
    lb_flx_out.append(_lb_flx_out)
    lb_flx_tot.append(_lb_flx_tot)
    _hb_flx_in = gu.BandFluxFinder(con.Frequency,con.Incident,HB_LAM,RANGE)
    _hb_flx_out = gu.BandFluxFinder(con.Frequency,con.DiffuseOut,HB_LAM,RANGE)
    _hb_flx_tot = gu.BandFluxFinder(con.Frequency,con.Total,HB_LAM,RANGE)
    hb_flx_in.append(_hb_flx_in)
    hb_flx_out.append(_hb_flx_out)
    hb_flx_tot.append(_hb_flx_tot)


lb_flx_in = np.array(lb_flx_in)
lb_flx_out = np.array(lb_flx_out)
lb_flx_tot = np.array(lb_flx_tot)

hb_flx_in = np.array(hb_flx_in)
hb_flx_out = np.array(hb_flx_out)
hb_flx_tot = np.array(hb_flx_tot)

beta_in = np.array(beta_in)
beta_out = np.array(beta_out)
beta_tot = np.array(beta_tot)

# ============================
x=6+(np.array(range(51))/10)
# Beta
ax[1].plot(x,beta_in,label="Incident",c='b')
ax[1].plot(x,beta_out,label="DiffuseOut",c='r')
ax[1].plot(x,beta_tot,label="Total",c='g')
ax[1].legend()

# Normalisation
ax[0].plot(x,lb_flx_in,c='b',label=f"Incident ({LB_LAM})$\\AA$")
ax[0].plot(x,lb_flx_out,c='r',label=f"DiffuseOut ({LB_LAM})$\\AA$")
ax[0].plot(x,lb_flx_tot,c='g',label=f"Total ({LB_LAM})$\\AA$")

ax[0].plot(x,hb_flx_in,c='b',ls='--',label=f"Incident ({HB_LAM})$\\AA$")
ax[0].plot(x,hb_flx_out,c='r',ls='--',label=f"DiffuseOut ({HB_LAM})$\\AA$")
ax[0].plot(x,hb_flx_tot,c='g',ls='--',label=f"Total ({HB_LAM})$\\AA$")


ax[0].set_yscale('log')
ax[0].legend(ncols=2)

# Beautify
for a in ax:
    a.set_xlim(6,9.5)
    a.set_xlabel("Log Age (Year)")

ax[0].set_ylabel("Band Flux (erg/s/A)")
ax[1].set_ylabel("UV Slope $\\beta_{UV}$")





plt.suptitle("IMF : Chab_300M \nZ=0.00001")


plt.show()
