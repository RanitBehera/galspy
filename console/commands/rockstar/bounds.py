import argparse,os
import galspy.utility.HaloQuery as hq
from galspy.FileTypes.ConfigFile import ReadAsDictionary

from galterm import utfsym

def main(env:dict):
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
    anc_data = qr.get_ancestor_track_of(HID,BLOBNAME)

    

    
