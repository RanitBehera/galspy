import pickle,os
import numpy as np
from scipy.spatial import KDTree
from tqdm import tqdm
import galspy as gs
from multiprocessing import Pool


PIG = gs.NavigationRoot(gs.NINJA.L150N2040).PIG(z=7)

DDIR = "/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/spectra_compare_single/data"
def Read(tgid,name):
    ddir = DDIR + os.sep + f"GID_{tgid}" + os.sep + name + ".dat"
    with open(ddir,"rb") as fp:
        return pickle.load(fp)

TGID = 4

m_gas_gid = Read(TGID,"gas_gid")
m_gas_pos = Read(TGID,"gas_pos")
m_gas_mass = Read(TGID,"gas_mass")
m_gas_met = Read(TGID,"gas_met")
m_gas_sml = Read(TGID,"gas_sml")
m_star_gid = Read(TGID,"star_gid")
m_star_pos = Read(TGID,"star_pos")
m_star_mass = Read(TGID,"star_mass")
m_star_pot = Read(TGID,"star_pot")
m_star_id = Read(TGID,"star_id")

id_to_spos = dict(zip(m_star_id, m_star_pos))

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



ept_z = np.max(m_gas_pos.T[2])        # <------ Towards Positive Z axis
PROBE_SPACING = 0.01*PIG.Header.BoxSize()/2040
PROBE_RADIUS = np.max(m_gas_sml)
tree = KDTree(m_gas_pos)


def SightlineFrom(sid):
    spos = id_to_spos[sid] 

    # Start point and end point
    spt=np.array(spos)
    ept = np.array(spt)
    ept[2] = ept_z

    # Probe points

    num_points = np.int32((ept[2]-spt[2])/PROBE_SPACING)
    probe_z = np.linspace(spt[2],ept[2],num_points)
    probe_points = np.array([[spt[0],spt[1],zp] for zp in probe_z])

    # Tree and Probe
    if len(probe_points)==0:
        return sid,0,0,0,0
    
    ngb_ids=tree.query_ball_point(probe_points,PROBE_RADIUS)
    probe_dens=np.zeros(len(probe_points))
    probe_mets=np.zeros(len(probe_points))
    for i in range(len(ngb_ids)):
        pp=probe_points[i]
        pp_ngb_ids=ngb_ids[i]
        pp_ngb_sml = m_gas_sml[pp_ngb_ids]
        pp_ngb_dist = np.linalg.norm(m_gas_pos[pp_ngb_ids]-pp,axis=1)
        # -------
        pp_ngb_mass = m_gas_mass[pp_ngb_ids]
        pp_ngb_met_mass = m_gas_mass[pp_ngb_ids]*m_gas_met[pp_ngb_ids]
        # pp_ngb_mass = tgas_mass[pp_ngb_ids]*((tgas_met[pp_ngb_ids]/0.02)**0.7)
        # -------
        probe_dens[i]=np.sum(pp_ngb_mass*CubicSpline(pp_ngb_dist,pp_ngb_sml))
        probe_mets[i]=np.sum(pp_ngb_met_mass*CubicSpline(pp_ngb_dist,pp_ngb_sml))


    # ----- Salting
    probe_dens +=1e-30 #To avoid divide by zero errors
    # ----- Metallicity Scaling
    _Z = probe_mets/probe_dens
    metal_factor=1
    probe_dens_Z=probe_dens*((_Z/0.02)**metal_factor)
    # ----- Units
    h=0.6736
    probe_dens *= PIG.Header.Units.Density * (h**2)   # Mass / Volume
    probe_dens_Z *= PIG.Header.Units.Density * (h**2)   # Mass / Volume
    probe_z *= PIG.Header.Units.Length/h
    # ----- Density to Number
    probe_ndens = probe_dens * 0.75 / 1.67e-24
    probe_ndens_Z = probe_dens_Z * 0.75 / 1.67e-24
    # ----- Comoving to Physical
    probe_ndens *=(1+PIG.Header.Redshift())**3
    probe_ndens_Z *=(1+PIG.Header.Redshift())**3
    probe_z /=(1+PIG.Header.Redshift())

    # ----- Integrate
    ds=np.diff(probe_z)
    N=np.sum(probe_ndens[:-1]*ds)
    NZ=np.sum(probe_ndens_Z[:-1]*ds)

    # ----- Convert to Physical
    kappa = 2e21
    epsilon=15
    AV = N/(epsilon*kappa)
    AVZ = NZ/(epsilon*kappa)


    return sid,N,NZ,AV,AVZ





data = {}
with Pool(24) as pool:
    for sid,N,NZ,AV,AVZ in tqdm(pool.imap_unordered(SightlineFrom,m_star_id),total=len(m_star_pos)):
        data[sid]=(N,NZ,AV,AVZ)

data=dict(sorted(data.items()))

filepath = f"/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/spectra_compare_single/data/{PIG.sim_name}_{PIG.redshift_name}_{TGID}.dict"

os.makedirs(os.path.dirname(filepath), exist_ok=True)
with open(filepath,"wb") as fp:
    pickle.dump(data,fp)