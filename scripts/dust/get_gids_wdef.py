import galspy
import numpy as np

SNAPSPATH = "/mnt/home/student/cranit/NINJA/simulations/L150N2040/SNAPS/"
SNAPNUM=43
MASSUNIT=1e10

# Cluster Defibition.
# Number of stars a halo should have to further post process.
# Linked to minimum stellar mass in the cluster.
CLDEF = 32     


# =========
root = galspy.NavigationRoot(SNAPSPATH)
print("[ TARGET BOX ]")
print(f"- Path:{SNAPSPATH}")
print(f"- Snapshot Number:{SNAPNUM}")
a=root.PART(SNAPNUM).Header.Time()
z=(1/a)-1
print(f"- Redshift:{z:.02}")

# print()
# print("[ READING PART ]")
# print("- Star Positions : ",end="")
# part_star_pos = root.PART(SNAPNUM).Star.Position()
# print("Done")

PIG=root.PIG(SNAPNUM)

print()
print("[ READING PIG ]")
print("- FOF GroupIDs : ",end="",flush=True)
gids = PIG.FOFGroups.GroupID()
print("Done")
print(f"  * Found {len(gids)} Groups.")

print("- FOF Group Stellar Mass : ",end="",flush=True)
gsm = PIG.FOFGroups.MassByType().T[4]*MASSUNIT
argmax_gsm= np.argmax(gsm)
max_gsm_gid,max_gsm = gids[argmax_gsm],gsm[argmax_gsm] 
single_star_mass = PIG.Header.MassTable()[4]*MASSUNIT
min_clmass = CLDEF*single_star_mass
cl_mask = gsm>min_clmass
cids    = gids[cl_mask]  # Cluster ids
csm     = gsm[cl_mask]
print("Done")
print(f"  * Mass of single star particle {single_star_mass:.02} M_solar/h.")
print(f"  * Maximum group stellar mass in GroupID {max_gsm_gid} with {max_gsm:.02} M_solar/h corresponding to {round(max_gsm/single_star_mass)} star count in group.")
print(f"  * Found {len(cids)} groups with cluster definition of {CLDEF} star particles corresponding to minimum cluster stellar mass of {min_clmass:.02} M_solar/h.")


np.savetxt("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/dust/data/gid_wdef32.txt",np.column_stack([cids,np.int64(csm/single_star_mass)]),fmt="%d %d")
