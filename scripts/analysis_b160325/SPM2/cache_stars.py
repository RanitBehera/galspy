import galspy
import numpy as np
from astropy.cosmology import FlatLambdaCDM
import pickle

SNAPSPATH = "/mnt/home/student/cranit/NINJA/simulations/L250N2040/SNAPS/"
SNAPNUM=42
PIG = galspy.NavigationRoot(SNAPSPATH).PIG(SNAPNUM)
print("Reading ...")
all_star_id  = PIG.Star.ID()
all_star_sft  = PIG.Star.StarFormationTime()
all_star_met  = PIG.Star.Metallicity()
print("Done")


H0=PIG.Header.HubbleParam()*100
Ol0=PIG.Header.OmegaLambda()
Om0=PIG.Header.Omega0()
cosmo = FlatLambdaCDM(H0=H0, Om0=Om0)

z=PIG.Header.Redshift()
age_uni_snap = cosmo.age(z).value*1000 #in Myr

z_sft = (1/all_star_sft)-1
age_uni_sft = cosmo.age(z_sft).value*1000 #in Myr 
age_star = age_uni_snap-age_uni_sft
age_star = np.clip(age_star,1,None)
age_star = np.round(np.log10(age_star)+6,1)

# ----

Z_foots=np.array([1e-5,1e-4,1e-3,2e-3,3e-3,4e-3,6e-3,8e-3,1e-2,1.4e-2,2e-2,3e-2,4e-2])

def map_to_closest(array1, array2):
    # Find the closest value in array1 for each value in array2
    indices = np.abs(array2[:, None] - array1).argmin(axis=1)
    return array1[indices]

met_star = map_to_closest(Z_foots,all_star_met)


# ----
Z_foots=[1e-5,1e-4,1e-3,2e-3,3e-3,4e-3,6e-3,8e-3,1e-2,1.4e-2,2e-2,3e-2,4e-2]
T_foots = np.arange(6,11.1,0.1)

Z_ind_map=dict(zip(Z_foots,range(len(Z_foots))))
T_ind_map=dict(zip(np.round(T_foots,1),range(len(T_foots))))

Z_keys = met_star
T_keys = age_star

Z_index = np.array([Z_ind_map.get(key, None) for key in Z_keys])
T_index = np.array([T_ind_map.get(float(f"{key:.1f}"), None) for key in T_keys])

spec_index = 1+(Z_index*len(T_foots)+T_index)


id_index_map = dict(zip(all_star_id,spec_index))


filepath="/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/SPM2/cache/specindex250.dict"
with open(filepath,"wb") as fp:
    pickle.dump(id_index_map,fp)
print(f"Saved as \"{filepath}\"") 