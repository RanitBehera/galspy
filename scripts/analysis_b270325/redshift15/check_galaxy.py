import galspy as gs
import matplotlib.pyplot as plt
from galspy.Utility.Visualization import Cube3D

SIM = gs.NavigationRoot(gs.NINJA.L150N2040)
z=13
SN = SIM.SnapNumFromRedshift(z)
PIG = SIM.PIG(SN)

SM=PIG.FOFGroups.MassByType().T[4]
GID = PIG.FOFGroups.GroupID()
print("Total :",len(SM))
limit=25*PIG.Header.MassTable()[4]
mask = SM>limit
print("Filter by Mass :",f"{limit*1e10/0.6736:0.02e}")
print("Filtered :",len(SM[mask]))

TGID =GID[mask] 
TSM = SM[mask]*1e10/0.6736
for itgid,ism in zip(TGID,TSM):
    print(f"{itgid} ---> SM={ism:02e}")


gas_pos = PIG.Gas.Position()
gas_gid = PIG.Gas.GroupID()

star_pos = PIG.Star.Position()
star_gid = PIG.Star.GroupID()


# exit()
for tg,tsm in zip(TGID,TSM):
    plt.figure("GID="+str(tg))
    c3d=Cube3D()
    mask = star_gid==tg
    tpos=star_pos[mask]
    c3d.add_points(tpos,points_size=50,points_color='r')
    
    mask = gas_gid==tg
    tpos=gas_pos[mask]
    c3d.add_points(tpos,points_size=2,points_color='y')

    plt.title(f"SM={tsm:02e}")
    c3d.show(False)

plt.show()
