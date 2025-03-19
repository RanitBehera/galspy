import galspy as gs
import numpy as np
import matplotlib.pyplot as plt

from galspy.MPGadget import _Sim


def DoForSim(sim_path:str,redshift=7):
    SIM = gs.NavigationRoot(sim_path)
    SN=SIM.SnapNumFromRedshift(redshift)
    PIG = SIM.PIG(SN)

    h=PIG.Header.HubbleParam()
    z=PIG.Header.Redshift()
    box_size = PIG.Header.BoxSize()/1000

    # Get Mass Function to light
    fof_dm_mass = PIG.FOFGroups.MassByType().T[1]*1e10

    lower_limit = 32*PIG.Header.MassTable()[1]*1e10
    mask =fof_dm_mass>lower_limit
    MC = fof_dm_mass[mask]
    MC = MC.astype(np.float64)
    
    # To light
    xi=1e30 # erg s-1 A-1 Mo-1
    L=MC*xi/1.15# erg s-1 A-1
    pc = 3.086e18   # cm pc-1
    f_lam = L/(4*np.pi*((10*pc)**2)) # erg s-1 A-1 cm-2
    c= 3e8 * 1e10 # A Hz
    f_nu = f_lam * ((1500**2)/c)
    M_AB = -2.5 * np.log10(f_nu) - 48.6

    # Luminosity function
    log_L,dn_dlogL,error=gs.Utility.LumimosityFunction(M_AB,box_size/h,0.5)
    XMF = log_L
    YMF = np.log10(dn_dlogL+1e-300)
    if sim_path==gs.NINJA.L150N2040:
        plt.plot(XMF[:-5],YMF[:-5],'.-',label=f"{SIM.sim_name}; z={z:.02f}")
    if sim_path==gs.NINJA.L250N2040:
        plt.plot(XMF[1:-5],YMF[1:-5],'.-',label=f"{SIM.sim_name}; z={z:.02f}")




DoForSim(gs.NINJA.L150N2040)
DoForSim(gs.NINJA.L250N2040)

# ================ LUMINOSITY FUNCTION OBSERVED
x = [-22.965968509217227, -22.714659508937057, -22.431937018434454, -22.094240830167536, -21.67801001759394, -21.175392736034077, -20.594240470667298, -19.97382215139801, -19.345549470947468, -18.803664697484145, -18.308900339104593, -17.735602434919073, -17.264398284081402]
y = [-7.426086369245929, -6.730434553005776, -6.026086820375284, -5.399999946925958, -4.782608591811657, -4.2347825775434975, -3.765217422456503, -3.36521760821565, -3.008695783705235, -2.739130535738666, -2.5304349112555586, -2.2434784275912847, -2.0347828031081754]
plt.plot(x,y,label="Cosmos-Web")


plt.legend()
plt.show()

