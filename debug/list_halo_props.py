import galspy.MPGadget as mp
import galspy.utility.HaloQuery as rs

path = "/mnt/home/student/cranit/Work/test_para_rock/L10N64"
root = mp.NavigationRoot(path)

snap = 17


qr = rs.RSGQuery(root.RSG(snap).path)

hids = root.RSG(snap).RKSHalos.HaloID()
mask = (hids>=0)
hids = hids[mask]

mvirs = root.RSG(snap).RKSHalos.VirialMass()[mask]
mbts  = root.RSG(snap).RKSHalos.PP_MassByType()[mask]
mbtwss  = root.RSG(snap).RKSHalos.PP_MassByTypeWithSub()[mask]

for hid,mvir,mbt,mbtws in zip(hids,mvirs,mbts,mbtwss):
    mvir = mvir/1e10
    print(hid,mvir,sum(mbt)/mvir,sum(mbtws)/mvir)
