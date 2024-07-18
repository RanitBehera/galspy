import galspy.IO.MPGadget as mp
import galspy.utility.HaloQuery as rs


path = "/mnt/home/student/cranit/Work/test_para_rock/OUT_L10N64"
root = mp.NavigationRoot(path)
snap = 17
qr = rs.RSGQuery(root.RSG(snap).path)

# print(qr.get_massive_halos())

bn = qr.get_blobname_of_halo_id(91)
ihid = qr.get_internal_halo_id_of(91,bn)

childs1 = qr.get_descendant_tree_of(ihid,bn)

print(childs1)