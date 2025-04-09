# %%
import galspy as gs
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import KDTree
import time

from galspy.Utility.Visualization import Cube3D


SIM = gs.NavigationRoot(gs.NINJA.L150N2040)
PIG = SIM.PIG(z=7)
UNITS=PIG.Header.Units


print("READING","-"*62)
gid = PIG.Gas.GroupID()
pos = PIG.Gas.Position()
met = PIG.Gas.Metallicity()
sml = PIG.Gas.SmoothingLength()
den = PIG.Gas.Density()
mass = PIG.Gas.Mass()

gid_star = PIG.Star.GroupID()
pos_star = PIG.Star.Position()
pot_star = PIG.Star.Potential()



def CubicSpline(r,h): #q=r/h
    C = (8/(np.pi*h**3))
    q = r/h
    I1=C*(1 - 6*(q**2) + 6*(q**3))
    I2=C*(2*((1-q)**3))
    I3=np.zeros_like(q)
    conditions = [q <= 0.5, np.logical_and(0.5 < q, q <= 1), q > 1]
    output = np.select(conditions,[I1,I2,I3])

    return output






# %%
tgid=2
# def Target(tgid):
    # STEP 0 - Mask for target particles 
print("- STEP 0 : Masking for target particles ...")
tmask=gid==tgid
tpos=pos[tmask]
tmet=met[tmask]
tsml=sml[tmask]
tmass=mass[tmask]
tstar_pos = pos_star[gid_star==tgid]
tstar_pot = pot_star[gid_star==tgid]



cind = np.argmin(tstar_pot)

avg_ips = PIG.Header.BoxSize()/2040

# print("avg ips :",avg_ips)


# ---------------------------------------
G_PROBE_SPACING=avg_ips
G_PROBE_RADIUS=np.max(tsml)
# ---------------------------------------


fig,ax=plt.subplots(1,1)

def GetCD(PROBE_SPACING,PROBE_RADIUS):
    # Sightline
    start_point=tstar_pos[cind]
    end_points_z = np.min(tpos.T[2]) + 0.8*(np.max(tpos.T[2])-np.min(tpos.T[2]))
    end_point = np.array(start_point)
    end_point[2] = end_points_z

    # print("start_pos",start_point)
    # probe_z = np.arange(start_point[2],end_point[2],PROBE_SPACING)

    num_points = np.int32((end_point[2]-start_point[2])/PROBE_SPACING)
    probe_z = np.linspace(start_point[2],end_point[2],num_points)
    probe_points = np.array([[start_point[0],start_point[1],zp] for zp in probe_z])
    # print(probe_points)

    if False:
        c3d=Cube3D()
        c3d.add_points(tpos,points_size=1,points_color=(0.8,0.8,0.8),points_alpha=1)
        c3d.add_points(probe_points,points_color='r',points_size=100,points_marker='+')
        # for pp in probe_points:
            # c3d.add_sphere_wire(pp,PROBE_RADIUS,'k')
        c3d.show()


    # Tree
    tree = KDTree(tpos)
    res=tree.query_ball_point(probe_points,PROBE_RADIUS)

    # for i in range(len(res)):
    #     print(i+1,len(res[i]))

    probe_val=np.zeros(len(probe_points))
    # print("-"*32)
    # print("Radius",PROBE_RADIUS)
    ax=plt.axes()
    for i in range(len(res)):
        cngb_ids=res[i]
        pp=probe_points[i]
        ngb_sml = tsml[cngb_ids]
        ngb_dist = np.linalg.norm(tpos[cngb_ids]-pp,axis=1)
        
        
        
        
        
        
        
        # 
        # ngb_mass = tmass[cngb_ids]*(tmet[cngb_ids]/0.02)**0.7
        ngb_mass = tmass[cngb_ids]
        # probe_val[i]=np.sum(ngb_mass*CubicSpline(ngb_dist,ngb_sml))
        
        ngb_met = tmet[cngb_ids]

        ax.plot(ngb_mass,ngb_met)
        
        # 
        continue
    
    return
    # print("Probe Vals")
    probe_val=probe_val*PIG.Header.Units.Density*(0.6736**2)
    ndens=probe_val/1.67e-24
    ndens=ndens*0.75


    ds=np.diff(probe_z)
    ds *=PIG.Header.Units.Length/0.6736

    N=np.sum(ndens[:-1]*ds)
    N*=((1+7))**2

    AV=N/3.05e21


    ax.plot((probe_z[:-1]-probe_z[0])*PIG.Header.Units.Length/0.6736/3.08e21,ndens[:-1],'-',label=f"{num_points} - {N:0.2e} - AV={AV:.02f}")


    return N, end_points_z-probe_z[0]




# Ni,end_points_z=GetCD(0.001*G_PROBE_SPACING,G_PROBE_RADIUS)
# Ni,end_points_z=GetCD(0.01*G_PROBE_SPACING,G_PROBE_RADIUS)
# Ni,end_points_z=GetCD(0.02*G_PROBE_SPACING,G_PROBE_RADIUS)

# SPC = np.arange(0.001*G_PROBE_SPACING,0.1*G_PROBE_SPACING,0.01*G_PROBE_SPACING)

# ax.axvline(end_points_z)

ax.legend()
ax.set_yscale("log")
plt.show()








# %%
