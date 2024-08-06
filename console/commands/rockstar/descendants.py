import argparse,os
import galspy.utility.HaloQuery as hq
from galspy.IO.ConfigFile import ReadAsDictionary
from treelib import Tree, Node
import galterm.ansi as ANSI
import galspy.IO.BigFile as bf

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
    IHID = qr.get_internal_halo_id(HID)
    BLOBNAME = qr.get_blobname(HID)
    des_data = qr.get_descendant_tree_of(IHID,BLOBNAME)

    HIDS = bf.Blob(RSG_PATH + os.sep + "RKSHalos" + os.sep + "HaloID" + os.sep + BLOBNAME).Read()

    t=Tree()
    def AddNode(tree:Tree,parent:int,childs:dict):
        for node,subnode in childs.items():
            if HIDS[node]>=0:
                tree.create_node(ANSI.FG_GREEN + f"{node}" + ANSI.RESET,node,parent=parent)
            else:
                tree.create_node(ANSI.FG_RED + f"{node}"+ANSI.RESET ,node,parent=parent)
                # pass

            if type(subnode)==dict:
                AddNode(tree,node,subnode)

            # if subnode==None: return
    
    t.create_node(f"HaloID : {HID} in BLOB \"{BLOBNAME}\"",-1)
    AddNode(t,-1,des_data)
    print(t.show(stdout=False))
    print("NOTE : Desendant IDs are internal.")

