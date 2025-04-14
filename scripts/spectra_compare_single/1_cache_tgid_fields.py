import galspy as gs
import numpy as np
import matplotlib.pyplot as plt
import os, pathlib, pickle

SIM = gs.NavigationRoot(gs.NINJA.L150N2040)
PIG = SIM.PIG(z=7)


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

print("- Star".ljust(8),">","GroupIDs")
star_gid = PIG.Star.GroupID()
print("- Star".ljust(8),">","Positions")
star_pos = PIG.Star.Position()
print("- Star".ljust(8),">","Masses")
star_mass = PIG.Star.Mass()
print("- Star".ljust(8),">","Potentials")
star_pot = PIG.Star.Potential()

DDIR = "/mnt/home/student/cranit/RANIT/Repo/galspy/scripts/spectra_compare_single/data"
def Dump(tgid,field,name:str):
    ddir = DDIR+os.sep+f"GID_{tgid}"
    pathlib.Path(ddir).mkdir(parents=True,exist_ok=True)

    with open(ddir + os.sep + name + ".dat","wb") as fp:
        pickle.dump(field,fp)


def DoFor(TGID):
    maskg = gas_gid==TGID
    masks = star_gid==TGID

    m_gas_gid   = gas_gid[maskg]
    m_gas_pos   = gas_pos[maskg]
    m_gas_mass  = gas_mass[maskg]
    m_gas_met   = gas_met[maskg]
    m_gas_sml   = gas_sml [maskg]

    m_star_gid  = star_gid[masks]
    m_star_pos  = star_pos[masks]
    m_star_mass = star_mass[masks]
    m_star_pot  = star_pot[masks]

    
    Dump(TGID,m_gas_gid,"gas_gid")
    Dump(TGID,m_gas_pos,"gas_pos")
    Dump(TGID,m_gas_mass,"gas_mass")
    Dump(TGID,m_gas_met,"gas_met")
    Dump(TGID,m_gas_sml,"gas_sml")
    Dump(TGID,m_star_gid,"star_gid")
    Dump(TGID,m_star_pos,"star_pos")
    Dump(TGID,m_star_mass,"star_mass")
    Dump(TGID,m_star_pot,"star_pot")


DoFor(3)
DoFor(4)