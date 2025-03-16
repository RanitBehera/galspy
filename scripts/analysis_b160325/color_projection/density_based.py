import galspy as gs
import numpy as np
import matplotlib.pyplot as plt

root = gs.NavigationRoot(gs.NINJA.L150N2040)

PIG = root.PIG(43)
cosmo=root.GetAstropyFlatLCDM()


sgids=PIG.Star.GroupID()
spos=PIG.Star.Position()
sdens=PIG.Star.BirthDensity()

PIG.Star.Generation()

brtime=PIG.Star.StarFormationTime()
brred = (1/brtime)-1
br_uniage = cosmo.age(brred).value*1000 #In Myr

crred=PIG.Header.Redshift()
cr_uniage = cosmo.age(crred).value*1000 #In Myr
age=cr_uniage-br_uniage


tgid=1
mask=sgids==tgid
spos=spos[mask]
sdens=sdens[mask]
age=age[mask]

mask2=sdens>0.0005
mask2=age>200

spos=spos[mask2]
sdens=sdens[mask2]
age=age[mask2]

x,y,z=spos.T
plt.scatter(x,y,c=age,cmap='gray',s=1)
plt.colorbar()
plt.axis("equal")
plt.show()







