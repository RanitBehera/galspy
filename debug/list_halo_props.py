import galspy.IO.MPGadget as mp
import galspy.utility.rockstar as rs

path = "/mnt/home/student/cranit/Work/test_para_rock/OUT_L10N64"
root = mp.NavigationRoot(path)

snap = 17


qr = rs.RockstarQuery(root.RSG(snap).path)
halos = root.RSG(snap).RKSHalos

hids = halos.HaloID()
ihids = halos.InternalHaloID()
sub_of = halos.Sub_of()
childs = halos.Child()
nextc  = halos.NextCochild()

nump   = halos.ParticleLength()
numcp = halos.ChildParticleLength()





print(f"BLOBNAME".ljust(8),
        "HALO ID".center(8),
        "INT ID".center(8),
        "SUB OF".center(8),
        "CHILD".center(8),
        "NEXT CH".center(8),
        "NUM P".center(8),
        "NUM CP".center(8),
        )

for i,hid in enumerate(hids):
    print(f"{qr.get_blobname_of(hid)}".ljust(8),
          str(hid).center(8),
          str(ihids[i]).center(8),
          str(sub_of[i]).center(8),
          str(childs[i]).center(8),
          str(nextc[i]).center(8),
          str(nump[i]).center(8),
          str(numcp[i]).center(8)
          )