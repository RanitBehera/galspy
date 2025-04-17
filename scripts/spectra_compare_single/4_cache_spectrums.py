import galspy as gs
import numpy as np
from galspy.Spectra import SpectralTemplates
from galspy.Spectra.Templates import BPASS
from galspy.Spectra.Dust import DustExtinction
from typing import Literal
import pickle,os
from tqdm import tqdm


PIG = gs.NavigationRoot(gs.NINJA.L150N2040).PIG(z=7)



# -----------------------------------------------------------------------
DDIR = "/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/spectra_compare_single/data"
def Read(tgid,name):
    ddir = DDIR + os.sep + f"GID_{tgid}" + os.sep + name + ".dat"
    with open(ddir,"rb") as fp:
        return pickle.load(fp)
    
TGID = 4
m_star_id = Read(TGID,"star_id")
m_star_mass = Read(TGID,"star_mass")
m_star_pot = Read(TGID,"star_pot")

cind = np.argmin(m_star_pot)
csid = m_star_id[cind]

filepath = DDIR + f"/L150N2040_z7p00_{TGID}.dict"
with open(filepath,"rb") as fp:
    data=pickle.load(fp)

cdata = data[csid]
CN,CNZ,CAV,CAVZ = cdata 

# odata = np.array([data[sid] for sid in m_star_id])
# N,NZ,AV,AVZ=odata.T

sid_to_AVZ = {}
for sid in m_star_id:
    sid_to_AVZ[sid] = data[sid][3]

CAVZ = sid_to_AVZ[csid]


print(CAVZ)


# -----------------------------------------------------------------------
specs_template_index = PIG.GetStarsSpecIndex()
def LoadSpectrums(imf:BPASS.AVAIL_MODEL_HINT,system:Literal["Single","Binary"]):
    fnsuffix = SpectralTemplates._get_filename(imf,system).removesuffix(".specs").removeprefix("_")

    global _template_specs_stellar
    _template_specs_stellar = SpectralTemplates.GetStellarTemplates(imf,system)
LoadSpectrums("CHABRIER_UPTO_300M","Binary")






# -----------------------------------------------------------------------
de = DustExtinction()
def gather_spectrum(target_star_ids,target_star_mass):
    tspecindex = [specs_template_index[tsid] for tsid in target_star_ids]
    mass_factor = (target_star_mass/PIG.Header.HubbleParam())/1e-4
    mass_scale = 1*mass_factor  # Right now twice the mass means twice the light

    Avs = [sid_to_AVZ[sid] for sid in target_star_ids]

    # Initialse to gather
    wl_stellar = _template_specs_stellar[0]
    blobspecs_stellar = np.zeros_like(wl_stellar)

    mask = (wl_stellar>10)&(wl_stellar<30000)
    wl_dust=wl_stellar[mask]
    blobspecs_with_dust = np.zeros_like(wl_dust)

    for ti, ms, Av in tqdm(zip(tspecindex, mass_scale, Avs), total=len(tspecindex)):
        current_star_spec=ms*_template_specs_stellar[ti]
        blobspecs_stellar+=current_star_spec

        _,reddened_spec = de.get_reddened_spectrum(wl_dust,current_star_spec[mask],"Calzetti",Av)
        blobspecs_with_dust+=reddened_spec

    return wl_stellar,blobspecs_stellar,wl_dust,blobspecs_with_dust

wl_st,spec_st,wl_dust,spec_stde = gather_spectrum(m_star_id,m_star_mass)

mask = (wl_st>10)&(wl_st<30000)
wl_de_central,spec_de_central = de.get_reddened_spectrum(wl_st[mask],spec_st[mask],"Calzetti",0.5)

filepath_st = DDIR + os.sep + f"spec_st_{PIG.sim_name}_{PIG.redshift_name}_{TGID}.txt"
filepath_dei = DDIR + os.sep + f"spec_dei_{PIG.sim_name}_{PIG.redshift_name}_{TGID}.txt"
filepath_dec = DDIR + os.sep + f"spec_dec_{PIG.sim_name}_{PIG.redshift_name}_{TGID}.txt"
np.savetxt(filepath_st,np.column_stack((wl_st,spec_st)),header="wl spec_st",fmt="%.02e %.02e")
np.savetxt(filepath_dei,np.column_stack((wl_dust,spec_stde)),header="wl_dust spec_stde",fmt="%.02e %.02e")
np.savetxt(filepath_dec,np.column_stack((wl_de_central,spec_de_central)),header="wl_dust spec_stde_central",fmt="%.02e %.02e")