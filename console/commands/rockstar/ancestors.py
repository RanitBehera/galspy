import argparse,os
import galspy.utility.HaloQuery as hq
from galspy.IO.ConfigFile import ReadAsDictionary
from treelib import Tree, Node

from galterm import utfsym

def main(env:dict):
    if "SIM" not in env.keys():     print("No SIM environment variable set.");return
    if "SIMFILE" not in env.keys(): print("No SIMFILE environment variable set.");return
    if "SNAP" not in env.keys():    print("No SNAP environment variable set.");return   

    ap = argparse.ArgumentParser()
    ap.add_argument("-l","--hid",type=int)
    args = ap.parse_args()

    if args.hid:
        HID = args.hid
    elif "HALO" in env.keys():
        HID = env["HALO"]
    else:
        print("No HALO environment variable set.");return



    RSG_PATH = ReadAsDictionary(env["SIMFILE"])["ROCKSTAR_GALAXIES_OUTBASE"] + os.sep + "RSG_" + str(env["SNAP"]).rjust(3,'0')
    qr = hq.RSGQuery(RSG_PATH)
    # IHID = qr.get_internal_halo_id(HID)
    BLOBNAME = qr.get_blobname(HID)
    anc_data = qr.get_ancenstor_track_of(HID,BLOBNAME)

    render_string = f" {utfsym.ARROW} ".join([str(a) for a in anc_data[::-1]])

    print(render_string)

    
