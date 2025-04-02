import galspy as gs
import numpy as np
import matplotlib.pyplot as plt
from astropy.cosmology import FlatLambdaCDM


SIM=gs.NavigationRoot(gs.NINJA.L150N2040)
PIG=SIM.PIG(z=7.0)


# Gas Fields
gid = PIG.Gas.GroupID()
pos = PIG.Gas.Position()
mass = PIG.Gas.Mass()
metallicity = PIG.Gas.Metallicity()



def _get_pixel_resolution():
    h=PIG.Header.HubbleParam()
    Om0=PIG.Header.Omega0()
    z=PIG.Header.Redshift()  

    RB = 0.031          #arcsecond per pixel : JWST 
    RB *= 1/3600        #degree per pixel
    RB *= np.pi/180     #radian per pixel

    cosmo = FlatLambdaCDM(H0=h*100,Om0=Om0)
    DA=cosmo.angular_diameter_distance(z).value #in Mpc
    DA*=1000 #To Kpc
    res = DA * RB   #pKpc per pixel
    res *=(1+z)*h   #cKpc per pixel
    return res



def ForTGID(TGID):
    print(TGID,flush=True)
    mask = gid==TGID
    tpos = pos[mask]
    tmass = mass[mask]
    tmetal = metallicity[mask]

    print("Before :",np.sum(tmass))
    mask = np.int32(tmetal/0.02>0.001)
    tmass=tmass*mask
    print("Before :",np.sum(tmass))

    exit()
    # Hitogram
    x,y,z=tpos.T
    u,v=x,y


    plt.figure()



    # ------------
    begin_u,begin_v = np.min(u),np.min(v)
    end_u,end_v = np.max(u),np.max(v)
    pr = _get_pixel_resolution()
    bin_edges_u = np.arange(begin_u-0.5*pr,end_u+0.5*pr,pr)
    if bin_edges_u[-1]<end_u+0.5*pr:
        np.append(bin_edges_u,bin_edges_u[-1]+pr)
    bin_edges_v = np.arange(begin_v-0.5*pr,end_v+0.5*pr,pr)
    if bin_edges_v[-1]<end_v+0.5*pr:
        np.append(bin_edges_v,bin_edges_v[-1]+pr)
    # ------------

    bin_hgt,ue,ve=np.histogram2d(u,v,bins=(bin_edges_u,bin_edges_v),weights=tmass)

    Area = pr**2/(0.6736**2)
    Area *= 1/(1+PIG.Header.Redshift())**2
    Area *=3.086e21**2


    NHI=((1e10/0.6736)*bin_hgt*0.75*2e30/1.67e-27)/Area
    NHI = NHI/2

    # plt.





    AV = NHI*1e-22

    # Plot
    plt.imshow(np.log10(1+NHI.T),origin="lower",extent=(np.min(u),np.max(u),np.min(v),np.max(v)))
    # plt.imshow(AV.T,origin="lower",extent=(np.min(u),np.max(u),np.min(v),np.max(v)))
    plt.show()


# for i in range(10):
ForTGID(2)