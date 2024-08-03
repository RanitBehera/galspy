import argparse
import galterm.ansi as ANSI
import galspy.utility.HaloQuery


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
    if not args.sim:print(ANSI.fmt_error("Could not target a SIM."));return
    if not args.snap:print(ANSI.fmt_error("Could not target a snapshot."));return

    # ---- Logic
    print(args)
    
    
    
   