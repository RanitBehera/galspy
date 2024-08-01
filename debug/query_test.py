import galspy.utility.HaloQuery as hq


qr=hq.RSGQuery("/mnt/home/student/cranit/Work/test_para_rock/OUT_L10N64/RSG_017")


val=qr.get_blobname_of_halo_id(100)
print(val)
