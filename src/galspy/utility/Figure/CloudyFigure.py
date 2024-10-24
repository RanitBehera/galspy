import numpy
import matplotlib.pyplot as plt
from galspec.Cloudy import CloudyOutputReader
from matplotlib.gridspec import GridSpec
import galspy.utility.Figure.Beautification as bty

def CloudyOverview(outs:list[CloudyOutputReader]):
    fig=plt.figure(figsize=(10,8))
    gs = GridSpec(2,2)

    ax_spec = fig.add_subplot(gs[0,0:2])
    ax_strc    = fig.add_subplot(gs[1,0])
    ax_line   = fig.add_subplot(gs[1,1])


    # SPECTRA
    alp=numpy.linspace(1,0.2,len(outs))
    for i,out in enumerate(outs):
        con = out.Spectrum.Continuum
        ax_spec.plot(con.Frequency,con.Incident,c='b',lw=1,alpha=alp[i])
        ax_spec.plot(con.Frequency,con.DiffuseOut,c='r',lw=1,alpha=alp[i])

    ax_spec.set_xscale('log')
    ax_spec.set_yscale('log')
    ax_spec.set_xlim(100,10000)
    ax_spec.set_ylim(1e25,1e35)
    bty.AddRydebergScale(ax_spec)

    ax_spec.set_xlabel("Angstrom")
    ax_spec.set_ylabel("Flux")

    ax


    # IONISATION STRUCURURE
    # ax_H

    plt.subplots_adjust(hspace=0.3,wspace=0.3)
    plt.show()


