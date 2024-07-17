import galspy.utility.rockstar as rs
import galspy.IO.MPGadget as mp

path = "/mnt/home/student/cranit/Work/test_para_rock/OUT_L10N64/RSG_017"

rq = rs.RockstarQuery(path)
rsg = mp.RSGRoot(path)

ms = rq.get_massive_halos()
print(ms)
hid = ms[0] #==77

# blob = rq.get_blobname_of(hid)
# child_internal = rsg.RKSHalos.Sub_of()[hid]
# child = rq.get_halo_id_of(blob,child_internal)

# print(f"{hid} is sub of {child[0]}")



# # -------------------------
# nhid = 80

# blob = rq.get_blobname_of(nhid)


# def int_to_ext(int_id):
#     return rq.get_halo_id_of(blob,int_id)


# fchild = rsg.RKSHalos.Child()[nhid]
# fchild = int_to_ext(fchild)
# print(fchild)
# # nchilds = rsg.RKSHalos.NextCochild()
# # child_halos =[fchild]
# # while not child_halos[-1] == -1:
# #     int_child_halo_next = nchilds[child_halos[-1]]
# #     child_halo_next = int_to_ext(int_child_halo_next)
# #     child_halos.append(child_halo_next)

# # print(child_halos)
