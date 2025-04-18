# %%
import galspy as gs
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import KDTree
import pickle
from tqdm import tqdm
import os
from galspy.Utility.Visualization import Cube3D


SIM = gs.NavigationRoot(gs.NINJA.L150N2040)
PIG = SIM.PIG(z=7)
UNITS=PIG.Header.Units


print("Target Box ".ljust(32,"="))
PIG.print_box_info()


print("\nReading Fields ".ljust(32,"="))
print("- Gas".ljust(8),">","GroupIDs")
gas_gid = PIG.Gas.GroupID()
print("- Gas".ljust(8),">","Positions")
gas_pos = PIG.Gas.Position()
print("- Gas".ljust(8),">","Masses")
gas_mass = PIG.Gas.Mass()
print("- Gas".ljust(8),">","Metallicity")
gas_met = PIG.Gas.Metallicity()
print("- Gas".ljust(8),">","Smoothing Lengths")
gas_sml = PIG.Gas.SmoothingLength()
print("- FOF".ljust(8),">","GroupIDs")
fof_gids = PIG.FOFGroups.GroupID()
print("- FOF".ljust(8),">","Stellar Mass")
fof_st_mass = PIG.FOFGroups.MassByType().T[4]
print("- Star".ljust(8),">","Central Location")
star_cpos = PIG.GetCentralStarPosition()


# MASK FOFS =======================
MIN_STAR_NUM = 16
min_st_mass = MIN_STAR_NUM*PIG.Header.MassTable()[4]
fof_mask = fof_st_mass>min_st_mass
print("\nFiltering Target FoFs ".ljust(32,'='))
print(" - Minimum Star Number","=",MIN_STAR_NUM)
print(" - Corresponding Minimum Stellar Mass","=",f"{min_st_mass*1e10:.02e}","Mo/h")
TFOF_GIDS = fof_gids[fof_mask]
print(" - Number of target FoF found","=",len(TFOF_GIDS))


# KERNELS =======================
def CubicSpline(r,h):
    C = (8/(np.pi*h**3))
    q = r/h
    I1=C*(1 - 6*(q**2) + 6*(q**3))
    I2=C*(2*((1-q)**3))
    I3=np.zeros_like(q)
    conditions = [q <= 0.5, np.logical_and(0.5 < q, q <= 1), q > 1]
    output = np.select(conditions,[I1,I2,I3])
    return output


Kernel = CubicSpline
print("\nUsing Kernel :",Kernel.__name__)



# ================================
# %%
# plt.figure(figsize=(10,10))
def TargetFoF(tgid,probe_spacing_factor=0.01,probe_radius_factor=1,with_metal=False,metal_factor=1,label=""):
    tmask_gas = gas_gid==tgid
    tgas_pos = gas_pos[tmask_gas]
    tgas_mass = gas_mass[tmask_gas]
    tgas_sml = gas_sml[tmask_gas]
    tgas_met = gas_met[tmask_gas]
    spos = star_cpos[tgid]

    # Start point and end point
    spt=np.array(spos)
    ept_z = np.max(tgas_pos.T[2])        # <------ Towards Positive Z axis
    ept = np.array(spt)
    ept[2] = ept_z

    # Probe points
    PROBE_SPACING = probe_spacing_factor*PIG.Header.BoxSize()/2040
    PROBE_RADIUS = probe_radius_factor*np.max(gas_sml)

    num_points = np.int32((ept[2]-spt[2])/PROBE_SPACING)
    probe_z = np.linspace(spt[2],ept[2],num_points)
    probe_points = np.array([[spt[0],spt[1],zp] for zp in probe_z])

    # Tree and Probe
    tree = KDTree(tgas_pos)
    if len(probe_points)==0:
        return (tgid,0,0)

    ngb_ids=tree.query_ball_point(probe_points,PROBE_RADIUS)
    probe_dens=np.zeros(len(probe_points))
    probe_mets=np.zeros(len(probe_points))
    for i in range(len(ngb_ids)):
        pp=probe_points[i]
        pp_ngb_ids=ngb_ids[i]
        pp_ngb_sml = tgas_sml[pp_ngb_ids]
        pp_ngb_dist = np.linalg.norm(tgas_pos[pp_ngb_ids]-pp,axis=1)
        # -------
        pp_ngb_mass = tgas_mass[pp_ngb_ids]
        pp_ngb_met_mass = tgas_mass[pp_ngb_ids]*tgas_met[pp_ngb_ids]
        # pp_ngb_mass = tgas_mass[pp_ngb_ids]*((tgas_met[pp_ngb_ids]/0.02)**0.7)
        # -------
        probe_dens[i]=np.sum(pp_ngb_mass*CubicSpline(pp_ngb_dist,pp_ngb_sml))
        probe_mets[i]=np.sum(pp_ngb_met_mass*CubicSpline(pp_ngb_dist,pp_ngb_sml))

    # ----- Salting

    # ----- Units
    h=PIG.Header.HubbleParam()
    probe_dens *= PIG.Header.Units.Density * (h**2)   # Mass / Volume
    zstops *= PIG.Header.Units.Length/h
    # ----- Salting
    probe_dens +=1e-30 #To avoid divide by zero errors
    probe_Z = probe_mets/probe_dens
    # ----- Metallicity Scaling
    metal_factor=1
    probe_dens_Z=probe_dens*((probe_Z/0.02)**metal_factor)
    # ----- Density to Number
    X=0.75
    MH=1.67e-24
    probe_ndens = probe_dens * (X/MH)
    probe_ndens_Z = probe_dens_Z * (X/MH)
    # ----- Comoving to Physical
    probe_ndens *=(1+PIG.Header.Redshift())**3
    probe_ndens_Z *=(1+PIG.Header.Redshift())**3
    zstops /=(1+PIG.Header.Redshift())

    # ----- Integrate
    ds=np.diff(zstops)
    N=np.sum(probe_ndens[:-1]*ds)
    NZ=np.sum(probe_ndens_Z[:-1]*ds)

    kappa = 2e21
    epsilon=15
    AV = N/(epsilon*kappa)
    AVZ = NZ/(epsilon*kappa)





    # ----- Visualisation
    if False:
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        c3d=Cube3D(ax)
        c3d.add_points(tgas_pos,1,(0.7,0.7,0.7),0.2,'.')
        c3d.get_axis().plot(*np.row_stack((spt,ept)).T,'-k',lw=1)
        c3d.add_points(probe_points,100,'r',1,'+')
        for pp in probe_points:
            pass
            c3d.add_sphere_wire(pp,0.5*PROBE_RADIUS,'k')
        c3d.show()


    if True:
        # plt.plot((probe_z-probe_z[0])/3.086e21,probe_ndens,'-',label=f"R={probe_radius_factor} ({len(probe_z)}) ; N={np.log10(N):.02f}")
        # plt.plot((probe_z-probe_z[0])/3.086e21,probe_ndens,'-',label=f"S={probe_spacing_factor} ({len(probe_z)}) ; N={np.log10(N):.02f}")
        plt.plot((probe_z-probe_z[0])/3.086e21,probe_ndens,'-',label=label+ f" N={np.log10(N):.02f} ; $A_V$={AV:.02f}")

    return (tgid,N,NZ,AV,AVZ)

TGID=20
TargetFoF(TGID,0.01,1,False,1,"No Scaling ;")
TargetFoF(TGID,0.01,1,True,1,"Scaling a=1 ;")
TargetFoF(TGID,0.01,1,True,0.7, "Saling a=0.7 ;")

# plt.xscale("log")
plt.yscale("log")
plt.ylim(1e-5,1e3)
plt.legend(title=f"$\kappa$={2e21} ; $\epsilon$={15}")
# plt.title("No Cloud Metallicity Scaling")
plt.xlabel("Physical Sightline Distance (kpc)")
plt.ylabel("Physical Number Density ($cm^{-3}$)")
plt.grid(alpha=0.3)
plt.annotate(f"{PIG.sim_name} : TGID = {TGID}",(0,0),(4,4),"axes fraction","offset pixels",ha="left",va="bottom")
plt.show()



# %%
