import numpy as np
import pickle
import matplotlib.pyplot as plt



gids,cxs,cys,czs = np.loadtxt("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/dust/data/man_gid_cen.txt").T
gids = np.int64(gids)

# Generate dens profile

def GetPickle(filepath):
    with open(filepath,"rb") as fp:
        data = pickle.load(fp)
    return data

for i in range(len(gids)):
    gid,cx,cy,cz=gids[i],cxs[i],cys[i],czs[i]
    
    # ------ READ
    PATH="/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/dust/data_gas"
    pos = GetPickle(f"{PATH}/pos_gas_{gid}.dat")
    vel = GetPickle(f"{PATH}/vel_gas_{gid}.dat")
    mass = GetPickle(f"{PATH}/mass_gas_{gid}.dat")*1e10
    metallicity = GetPickle(f"{PATH}/metallicity_gas_{gid}.dat")
    metallicity = metallicity*mass
    
    # ------ LOCAL FRAME
    Center = np.column_stack((cx,cy,cz))
    pos = pos-Center

    # Get Radius and bin
    rad = np.linalg.norm(pos,axis=1)
    delta_rad = 1.
    bin_indices=np.int32(rad/delta_rad)
    num_bins = np.max(bin_indices) + 1


    # fill bins
    bin_mass = np.zeros(num_bins)
    np.add.at(bin_mass,bin_indices,mass)


    # Convert
    bin_rad = delta_rad*np.arange(num_bins)
    bin_volume = 4*np.pi*(bin_rad**2)*delta_rad
    bin_dens = bin_mass/bin_volume
    bin_dens *= 0.75*2e33/((3e21)**3) 
    bin_dens /=1.67e-24

    # physical
    # https://ned.ipac.caltech.edu/level5/Madau6/Madau1_1.html
    z=7
    bin_dens *= (1+z)**3
    fb=0.0493/0.3153
    n_igm = (1.6e-7)*(fb/0.019)*((1+z)**3) 

    #smooth 
    window_size = 32
    kernel = np.ones(window_size) / window_size
    sm_bin_dens = np.convolve(bin_dens, kernel, mode="same")

    # Check igm
    plt.plot(bin_rad,sm_bin_dens,label=f"{gid}")

plt.yscale('log')
plt.xscale('log')
plt.xlabel("ckpc/h")
plt.axvline(2500,color='k',lw=1)
plt.axvline(10000,color='r',lw=1)
plt.axhline(n_igm,color='k',lw=1,ls='--')
plt.legend()
plt.show()