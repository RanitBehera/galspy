import argparse, os
import galterm.ansi as ANSI
import galterm.utfsym as UTF8
from galspy.utility.termutil import get_available_sim, get_available_snaps
from galspy.FileTypes.ConfigFile import ReadAsDictionary

import galspy.FileTypes.BigFile as bf
import numpy



def completion(env:dict):
    return {
        "-s" : None,
        "--sim" : None,
        "-n" : None,
        "--snap" : None,
        "-e" : None,
        "--exclude-sub" : None,
        "-c" : None,
        "--by-count" : None,
        "-m" : None,
        "--by-mass" : None,
        "--with-dm" : None,
        "--with-gas" : None,
        "--with-star" : None,
        "--with-bh" : None
    }




def main(env:dict):
    # ---- Get Arguments
    ap=argparse.ArgumentParser(description="Lists gaint halos by mass or particle count.")
    ap.add_argument("-s","--sim",help="Target SIMFILE name.",default=env.get("SIM"))
    ap.add_argument("-n","--snap",help="Target snapsort number.",type=int,default=env.get("SNAP"))
    
    ap.add_argument("-e","--exclude-sub",help="Exclude all descendants",action="store_true")
    gp1 = ap.add_mutually_exclusive_group()
    gp1.add_argument("-c","--by-count",help="Lists giant halos by particle count.",action="store_true")
    gp1.add_argument("-m","--by-mass",help="Lists giant halos by mass.",action='store_true')
    gp2 = ap.add_mutually_exclusive_group()
    gp2.add_argument("--dm",help="Sort with dark matter.",action='store_true')
    gp2.add_argument("--gas",help="Sort with gas.",action='store_true')
    gp2.add_argument("--star",help="Sort with stars.",action='store_true')
    gp2.add_argument("--bh",help="Sort with blackhole.",action='store_true')

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

    # if all()


    # ---- Logic
    SNAP_PATH = SIMFILE["ROCKSTAR_GALAXIES_OUTBASE"] + os.sep + target_snap
    fields_path = SNAP_PATH + os.sep + "RKSHalos" + os.sep



    table = None
    if args.by_mass:
        if args.exclude_sub:
            table = bf.Column(fields_path + "PP_MassByType").Read()
        else:
            table = bf.Column(fields_path + "PP_MassByTypeWithSub").Read()
    else:
        if args.exclude_sub:
            table = bf.Column(fields_path + "PP_LengthByType").Read()
        else:
            table = bf.Column(fields_path + "PP_LengthByTypeWithSub").Read()

    # Mask for valid HID
    hid = bf.Column(fields_path + "HaloID").Read()
    hidmask = (hid>=0)

    hid = hid[hidmask]
    table = table[hidmask]

    # Sort
    if args.gas:order = numpy.argsort(table[:,0])
    elif args.star:order = numpy.argsort(table[:,4])
    elif args.bh:order = numpy.argsort(table[:,5])
    else:order = numpy.argsort(table[:,1])
    # Decreasing Sort
    order = order[::-1]
    table = table[order]
    hid   = hid[order]
    # Head
    table = table[:10]
    hid = hid[:10]

    # Print
    if args.by_mass : table = table * 1e10
    CW = 12 # Cell Width
    print("HID".center(CW),"DM".center(CW),"GAS".center(CW),"STAR".center(CW),"BH".center(CW),sep=UTF8.LIGHT_VERTICAL)
    print(UTF8.VERTICAL_SINGLE_AND_HORIZONTAL_DOUBLE.join([UTF8.DOUBLE_HORIZONTAL * CW for _ in range(5)]))
    for ihid,row in zip(hid,table):
        if args.by_mass:
            print(str(ihid).center(CW),
                "{:.2e}".format(row[1]).center(CW),
                "{:.2e}".format(row[0]).center(CW),
                "{:.2e}".format(row[4]).center(CW),
                "{:.2e}".format(row[5]).center(CW),
                sep=UTF8.LIGHT_VERTICAL)
        else:
            print(str(ihid).center(CW),
                  str(row[1]).center(CW),
                  str(row[0]).center(CW),
                  str(row[4]).center(CW),
                  str(row[5]).center(CW),
                  sep=UTF8.LIGHT_VERTICAL)

