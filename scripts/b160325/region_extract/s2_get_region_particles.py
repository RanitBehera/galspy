
import galspy,numpy
from galspy.utility.visualization import CubeVisualizer
import pickle,os

# PATH = "/mnt/home/student/cranit/NINJA/simulations/L150N2040/SNAPS"
PATH = "/mnt/home/student/cranit/Data/MP_Gadget/Nishi/L50N1008z05"
ROOT = galspy.NavigationRoot(PATH)
# SAVEDIR = "/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/region_extract/data"
SAVEDIR = "/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/region_extract/data_kanish"
SPAN = 505 #kpc - center to side
gid=827
# SUFFIX=f"gas_{gid}"
SNAPNUM = 174

PTYPE = ROOT.PART(SNAPNUM).Gas
PTEXT = "gas"   #"gas" or "star"
SUFFIX = f"{PTEXT}_{gid}"



SAVEDIR=SAVEDIR+os.sep+f"GID_{gid}"
if not os.path.exists(SAVEDIR):
    os.makedirs(SAVEDIR)


print("Reading centers")
CX,CY,CZ = ROOT.PIG(SNAPNUM).FOFGroups.MassCenterPosition()[gid-1]       #1 for gid
CVX,CVY,CVZ = ROOT.PIG(SNAPNUM).FOFGroups.MassCenterVelocity()[gid-1]       #1 for gid


if True:
    BLOBS = ['00000C', '00000D', '00000E', '00000F']

    with open(SAVEDIR+os.sep+f"region_info_{SUFFIX}.txt","w") as fp:
        # fp.write("# lengths in ckpc/h then velocity\n")
        # fp.write(f"{CX},{CY},{CZ}\n{SPAN},{SPAN},{SPAN}\n")
        # fp.write(f"{CVX},{CVY},{CVZ}")
        fp.write(f"GID:{gid}\n")
        fp.write("\nPART HEADER"+'-'*32+"\n")
        fp.write("\n".join([f"{key}:{val}" for key,val in ROOT.PART(SNAPNUM).Header().items()]))
        fp.write("\n\nPIG HEADER"+'-'*32+"\n")
        fp.write("\n".join([f"{key}:{val}" for key,val in ROOT.PIG(SNAPNUM).Header().items()]))
        fp.write("\n\nOTHER"+'-'*32+"\n")
        fp.write(f"Center of Mass:{CX},{CY},{CZ}\n")
        fp.write(f"Stellar Mass:{ROOT.PIG(SNAPNUM).FOFGroups.MassByType().T[4][gid-1]}\n")
        fp.write(f"Region Span (Center to Edge) (ckpc/h):{SPAN}\n")


    if PTEXT=="gas":
        print("Reading particle pos")

        X,Y,Z = PTYPE.Position(BLOBS).T          #<------
        VX,VY,VZ = PTYPE.Velocity(BLOBS).T          #<------


        print("Reading particle mass")

        M = PTYPE.Mass(BLOBS)                    #<------
        IID = PTYPE.ID(BLOBS)                    #<------
        GID = PTYPE.GroupID(BLOBS)                    #<------
        rho = PTYPE.Density(BLOBS)
        sml = PTYPE.SmoothingLength(BLOBS)          #<-------
        inteng = PTYPE.InternalEnergy(BLOBS)
        Zm = PTYPE.Metallicity(BLOBS)                    #<------
        NH1 = PTYPE.NeutralHydrogenFraction(BLOBS)                    #<------
        metals = PTYPE.Metals(BLOBS)
        elec_abdn = PTYPE.ElectronAbundance(BLOBS)
        

        print("masking X")
        maskx = (CX-SPAN<X)&(X<CX+SPAN)
        print("masking Y")
        masky = (CY-SPAN<Y)&(Y<CY+SPAN)
        print("masking Z")
        maskz = (CZ-SPAN<Z)&(Z<CZ+SPAN)
        print("combining mask")


        mask = maskx & masky & maskz

        print("Applying mask")
        X,Y,Z = X[mask],Y[mask],Z[mask]
        VX,VY,VZ = VX[mask],VY[mask],VZ[mask]
        M=M[mask]
        rho=rho[mask]
        sml=sml[mask]
        inteng=inteng[mask]
        Zm=Zm[mask]
        NH1=NH1[mask]
        IID=IID[mask]
        GID=GID[mask]
        metals=metals[mask]
        elec_abdn=elec_abdn[mask]
        print(f"Found {len(M)} particles with masking.")

        print("stacking")
        pos = numpy.column_stack((X,Y,Z))
        vel = numpy.column_stack((VX,VY,VZ))

        with open(SAVEDIR+os.sep+f"pos_{SUFFIX}.dat","wb") as fp:     #<-----
            pickle.dump(pos,fp)
        print("Position dumped.")

        with open(SAVEDIR+os.sep+f"vel_{SUFFIX}.dat","wb") as fp:     #<-----
            pickle.dump(vel,fp)
        print("Velocity dumped.")

        with open(SAVEDIR+os.sep+f"mass_{SUFFIX}.dat","wb") as fp:    #<-----
            pickle.dump(M,fp)
        print("Mass dumped.")

        with open(SAVEDIR+os.sep+f"metallicity_{SUFFIX}.dat","wb") as fp:    #<-----
            pickle.dump(Zm,fp)
        print("Metallicity dumped.")

        with open(SAVEDIR+os.sep+f"dens_{SUFFIX}.dat","wb") as fp:    #<-----
            pickle.dump(rho,fp)
        print("Density dumped.")

        with open(SAVEDIR+os.sep+f"id_{SUFFIX}.dat","wb") as fp:    #<-----
            pickle.dump(IID,fp)
        print("Particle ID dumped.")

        with open(SAVEDIR+os.sep+f"gid_{SUFFIX}.dat","wb") as fp:    #<-----
            pickle.dump(GID,fp)
        print("Group ID dumped.")

        with open(SAVEDIR+os.sep+f"sml_{SUFFIX}.dat","wb") as fp:    #<-----
            pickle.dump(sml,fp)
        print("Smoothing length dumped.")

        with open(SAVEDIR+os.sep+f"ie_{SUFFIX}.dat","wb") as fp:    #<-----
            pickle.dump(inteng,fp)
        print("Internal Energy dumped.")

        with open(SAVEDIR+os.sep+f"NHI_{SUFFIX}.dat","wb") as fp:    #<-----
            pickle.dump(NH1,fp)
        print("Neutral Hydrogen Fraction dumped.")

        with open(SAVEDIR+os.sep+f"metals_{SUFFIX}.dat","wb") as fp:    #<-----
            pickle.dump(metals,fp)
        print("Metals dumped.")

        with open(SAVEDIR+os.sep+f"eabundance_{SUFFIX}.dat","wb") as fp:    #<-----
            pickle.dump(elec_abdn,fp)
        print("ElectronAbundance dumped.")

    if PTEXT=="star":
        print("Reading particle pos")

        X,Y,Z = PTYPE.Position(BLOBS).T          #<------
        VX,VY,VZ = PTYPE.Velocity(BLOBS).T          #<------


        print("Reading particle mass")

        M = PTYPE.Mass()

