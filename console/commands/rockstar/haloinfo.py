import argparse
from galspy.FileTypes.ConfigFile import ReadAsDictionary
import galspy.MPGadget as mp

def completion(env:dict):
    return{
        '-i' : None,
        '--info' : None
    }


def main(env:dict):
    if "SIM" not in env.keys():
        print("No SIM environment variable set.");return
    if "SIMFILE" not in env.keys():
        print("No SIMFILE environment variable set.");return
    if "SNAP" not in env.keys():
        print("No SNAP environment variable set.");return
    if "HALO" not in env.keys():
        print("No HALO environment variable set.");return
    
    ap = argparse.ArgumentParser()
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument('-i','--info',action="store_true")
    # group.add_argument('-n','--snap')

    args = ap.parse_args()

    if args.info:
        outbase = ReadAsDictionary(env["SIMFILE"])["ROCKSTAR_GALAXIES_OUTBASE"]
        
        print_halo_info(outbase,env["SNAP"],env["HALO"])






def print_halo_info(outbase:str,snap:int,halo_id:int):
    CCW = 32 # Column Character Width
    HCW = 50 # Header Character Width
    MASS_UNIT = 1e10
    HID = halo_id
    BULLET = "\u2022"
    HEADER = "\u2550" 

    h = mp.NavigationRoot(outbase).RSG(snap).RKSHalos

    if True:
        print(" KINEMATICS ".center(HCW,HEADER))
        print(BULLET,"Position (Mpc/h)".ljust(CCW),":",", ".join(str(crdn) for crdn in h.Position()[HID]))
        print(BULLET,"Velocity (km/s)".ljust(CCW),":",", ".join(str(crdn) for crdn in h.Velocity()[HID]))
        print(BULLET,"Angular Momentum (unit)".ljust(CCW),":",", ".join(str(crdn) for crdn in h.AngularMomentum()[HID]))
        print(BULLET,"Core Velocity (km/s)".ljust(CCW),":",", ".join(str(crdn) for crdn in h.CoreVelocity()[HID]))
        print(BULLET,"Bulk Velocity (km/s)".ljust(CCW),":",", ".join(str(crdn) for crdn in h.BulkVelocity()[HID]))
        print(BULLET,"Position Offset (unit)".ljust(CCW),":",h.PositionOffset()[HID])
        print(BULLET,"Velocity Offset (unit)".ljust(CCW),":",h.VelocityOffset()[HID])
        print(BULLET,"Position Error (unit)".ljust(CCW),":",h.PositionUncertainty()[HID])
        print(BULLET,"Velocity Error (unit)".ljust(CCW),":",h.VelocityUncertainty()[HID])
        print(BULLET,"Bulk Velocity Error (unit)".ljust(CCW),":",h.BulkVelocityUncertainty()[HID])
        print()

    if True:
        print(" MASSES (UNIT = 10\u00B9\u2070M\u2609) ".center(HCW,HEADER))
        print(BULLET,"Virial Mass".ljust(CCW),":",h.VirialMass()[HID]/MASS_UNIT)
        print(BULLET,"Gravitational Mass".ljust(CCW),":",h.mgrav()[HID]/MASS_UNIT)
        print(BULLET,"Gas Mass".ljust(CCW),":",h.GasMass()[HID]/MASS_UNIT)
        print(BULLET,"Stellar Mass".ljust(CCW),":",h.StellarMass()[HID]/MASS_UNIT)
        print(BULLET,"Blackhole Mass".ljust(CCW),":",h.BlackholeMass()[HID]/MASS_UNIT)
        alt_masses = h.AlternateMasses()
        print(BULLET,"Alternate Mass (200b)".ljust(CCW),":",alt_masses[HID][0]/MASS_UNIT)
        print(BULLET,"Alternate Mass (200c)".ljust(CCW),":",alt_masses[HID][1]/MASS_UNIT)
        print(BULLET,"Alternate Mass (500c)".ljust(CCW),":",alt_masses[HID][2]/MASS_UNIT)
        print(BULLET,"Alternate Mass (2500c)".ljust(CCW),":",alt_masses[HID][3]/MASS_UNIT)
        print("")

    if True:
        print(" PARTICLE COUNTS ".center(HCW,HEADER))
        print(BULLET,"Excluding Subhalos".ljust(CCW),":",h.ParticleLength()[HID])
        print(BULLET,"Including Subhalos".ljust(CCW),":",h.ChildParticleLength()[HID])
        print(BULLET,"Core".ljust(CCW),":",h.CoreLength()[HID])
        print(BULLET,"Dark Matter".ljust(CCW),":",'-')
        print(BULLET,"Gas".ljust(CCW),":",'-')
        print(BULLET,"Star".ljust(CCW),":",'-')
        print(BULLET,"Blackhole".ljust(CCW),":",'-')
        print("")

    if True:
        print(" SUBHALO HIRARCHY IDS".center(HCW,HEADER))
        print(BULLET,"HALO".ljust(CCW),":",h.HaloID()[HID])
        print(BULLET,"SUBHALO OF".ljust(CCW),":",h.Sub_of()[HID])

        sib = [h.Child()[HID]]
        next_coc = h.NextCochild()
        while sib[-1]> -1:sib.append(next_coc[sib[-1]])
        sib.pop()

        print(BULLET,"CHILDS".ljust(CCW),":",", ".join(str(s) for s in sib))


