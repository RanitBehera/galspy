import galspy as gs
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.lines as mlines
import matplotlib.patches as mpatches



gs.SetPlotStyle(16)
plt.figure(figsize=(10,6))

box=[]
def ForSim(filepath,redshift,**kwargs):
    PIG = gs.NavigationRoot(filepath).PIG(z=redshift)
    
    MBT = PIG.FOFGroups.MassByType().T*1e10
    gas,dm,star = MBT[0],MBT[1],MBT[4]

    gas_metmass = PIG.FOFGroups.GasMetalMass()*1e10

    mtable = np.array(PIG.Header.MassTable())*1e10 
    box_size = PIG.Header.BoxSize()/1000


    M,dn_dlogM,error=gs.Utility.MassFunction(dm[dm>16*mtable[1]],box_size,14) 
    plt.plot(M,dn_dlogM,**kwargs)

    M,dn_dlogM,error=gs.Utility.MassFunction(gas[gas>16*mtable[0]],box_size,14)  
    plt.plot(M,dn_dlogM,marker='o',ms=4,**kwargs)
    
    M,dn_dlogM,error=gs.Utility.MassFunction(star[star>16*mtable[4]],box_size,14)  
    mask = dn_dlogM>1e-8
    plt.plot(M[mask],dn_dlogM[mask],marker='*',ms=8,**kwargs)
    
    M,dn_dlogM,error=gs.Utility.MassFunction(gas_metmass[gas_metmass>1e5],box_size,14)  
    plt.plot(M,dn_dlogM,marker='D',ms=4,**kwargs)

    box.append(mpatches.Patch(color=kwargs["color"],label=PIG.sim_name))


REDSHIFT=5
# ----------------
cosmo = {'flat': True,'H0': 67.36,'Om0': 0.3153,'Ob0': 0.0493,'sigma8': 0.811,'ns': 0.9649}
mass_range = np.logspace(6,13,1000)
mr,mf=gs.Utility.MassFunctionLiterature("Press-Schechter",cosmo,REDSHIFT,mass_range,"dn/dlnM")
plt.plot(mr,mf,'k--',lw=1)
box.append(mlines.Line2D([],[],color='k',ls='--',label="Press-Schechter",lw=1))
mr,mf=gs.Utility.MassFunctionLiterature("Seith-Tormen",cosmo,REDSHIFT,mass_range,"dn/dlnM")
plt.plot(mr,mf,'k:',lw=1)
box.append(mlines.Line2D([],[],color='k',ls=':',label="Seith-Tormen",lw=1))

# ----------------
ForSim(gs.NINJA.L150N2040,REDSHIFT,color='m')
ForSim(gs.NINJA.L250N2040,REDSHIFT,color='c')
# ForSim(gs.NINJA.L150N2040_WIND_WEAK,REDSHIFT,color='y')

plt.xscale("log")
plt.yscale("log")
plt.xlabel("Mass ($M_\odot/h$)",fontsize=12)
plt.ylabel("$\phi$",fontsize=20)
plt.ylim(1e-8,1e1)
plt.xlim(1e4,1e13)
# plt.legend(frameon=False,loc="lower left")
plt.grid(alpha=0.2)
plt.annotate(f"z={REDSHIFT}",(0,1),(8,-8),"axes fraction","offset pixels",
             ha="left",va="top",fontsize=16)


# Costume Legend
leg_box = plt.gca().legend(handles=box,fontsize=10, loc='upper right',ncol=1,frameon=False,markerfirst=False)
plt.gca().add_artist(leg_box)

hands = []
hands.append(mlines.Line2D([], [], color='k', marker='',markersize=8, label='Dark Matter'))
hands.append(mlines.Line2D([], [], color='k', marker='o',markersize=4, label='Gas'))
hands.append(mlines.Line2D([], [], color='k', marker='*',markersize=8, label='Stellar'))
hands.append(mlines.Line2D([], [], color='k', marker='D',markersize=4, label='Gas Metal Mass'))
leg_part=plt.gca().legend(handles=hands,fontsize=10, loc='lower left',ncol=1,frameon=False)
plt.gca().add_artist(leg_part)



plt.show()
















