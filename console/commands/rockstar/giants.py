import argparse, os
import galterm.ansi as ANSI
import galspy.utility.HaloQuery as hq
from galspy.utility.termutil import get_available_sim, get_available_snaps
from galspy.IO.ConfigFile import ReadAsDictionary

def main(env:dict):
    # ---- Get Arguments
    ap=argparse.ArgumentParser(description="Lists gaint halos by mass or particle count.")
    ap.add_argument("-s","--sim",help="Target SIMFILE name.",default=env.get("SIM"))
    ap.add_argument("-n","--snap",help="Target snapsort number.",type=int,default=env.get("SNAP"))
    
    ap.add_argument("-e","--exclude-childs",help="Exclude childs and descendants",action="store_true")
    gp1 = ap.add_mutually_exclusive_group()
    gp1.add_argument("-m","--by-mass",help="Lists giant halos by mass.",action='store_true')
    gp1.add_argument("-c","--by-count",help="Lists giant halos by particle count.",action="store_true")
    # gp2 = ap.add_mutually_exclusive_group()
    # gp2.add_argument("--dm")
    # gp2.add_argument("--gas")
    # gp2.add_argument("--star")
    # gp2.add_argument("--bh")

    args = ap.parse_args()


    # ---- Validate Arguments
    if not args.sim:print(ANSI.fmt_error("No target SIM."));return
    if not args.snap:print(ANSI.fmt_error("No target snapshot."));return
    SIMFILES = env["SIMFILES_CACHE"] if "SIMFILES_CACHE" in env.keys() else get_available_sim(env["PATH"])
    if args.sim not in SIMFILES.keys() : print(ANSI.fmt_error(f"Could not find target sim {args.sim}"));return
    SIMFILE = ReadAsDictionary(SIMFILES.get(args.sim))
    avail_snaps = get_available_snaps(SIMFILE["ROCKSTAR_GALAXIES_OUTBASE"],"RSG_")
    target_snap = "RSG_"+str(args.snap).rjust(3,'0')
    if target_snap not in avail_snaps : print(ANSI.fmt_error(f"Could not find target snap {target_snap}"));return

    # ---- Logic
    SNAP_PATH = SIMFILE["ROCKSTAR_GALAXIES_OUTBASE"] + os.sep + target_snap
    qr = hq.RSGQuery(SNAP_PATH)
    
    # print
    # 
    #  HID |       DM     |   GAS   |   STAR  | BH  |
    #      | COUNT | MASS |
    