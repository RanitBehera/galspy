import yt
import yt.units
import galspy.MPGadget as mp
import numpy as np


PATH = "/mnt/home/student/cranit/Data/MP_Gadget/Nishi/L10N64/output"
SNAP = mp.NavigationRoot(PATH).PART(17)


ppxg,ppyg,ppzg     = (SNAP.Gas.Position()).T
ppxd,ppyd,ppzd     = (SNAP.DarkMatter.Position()).T
ppxs,ppys,ppzs     = (SNAP.Star.Position()).T

pvxg,pvyg,pvzg     = (SNAP.Gas.Velocity()).T
pvxd,pvyd,pvzd     = (SNAP.DarkMatter.Velocity()).T
pvxs,pvys,pvzs     = (SNAP.Star.Velocity()).T

mg = SNAP.Gas.Mass()
md = SNAP.DarkMatter.Mass()
ms = SNAP.Star.Mass()

sml       = SNAP.Gas.SmoothingLength()
dens      = SNAP.Gas.Density()





# ======================
# ----- Feed to YT -----
# ======================
data_gas = {
    # GAS
    ("io", "particle_position_x"): ppxg,
    ("io", "particle_position_y"): ppyg,
    ("io", "particle_position_z"): ppzg,
    ("io", "particle_velocity_x"): pvxg,
    ("io", "particle_velocity_y"): pvyg,
    ("io", "particle_velocity_z"): pvzg,
    ("io", "particle_mass"): mg,
    ("io", "smoothing_length"): np.double(sml),
    ("io", "density"): np.double(dens)
}

data_dm={
    # DM
    ("dm", "particle_position_x"): ppxd,
    ("dm", "particle_position_y"): ppyd,
    ("dm", "particle_position_z"): ppzd,
    ("dm", "particle_velocity_x"): pvxd,
    ("dm", "particle_velocity_y"): pvyd,
    ("dm", "particle_velocity_z"): pvzd,
    ("dm", "particle_mass"): md
}

data_star={
    # STAR
    ("star", "particle_position_x"): ppxs,
    ("star", "particle_position_y"): ppys,
    ("star", "particle_position_z"): ppzs,
    ("star", "particle_velocity_x"): pvxs,
    ("star", "particle_velocity_y"): pvys,
    ("star", "particle_velocity_z"): pvzs,
    ("star", "particle_mass"): ms
}


BoxSize=10000

UnitLength_in_cm = 3.08568e21
UnitMass_in_g = 1.989e43
UnitVelocity_in_cm_per_s = 100000

ds = yt.load_particles(
        data_gas,
        bbox=[[0,BoxSize],[0,BoxSize],[0,BoxSize]],
        length_unit= UnitLength_in_cm,
        mass_unit=UnitMass_in_g,
        velocity_unit=UnitVelocity_in_cm_per_s,
        periodicity=(True,True,True)
    )




# ================ 
# Setup YT
# ================ 
# ds.add_sph_fields()


# ------ PARTICLE PLOT
# pt = yt.ParticlePlot(ds,
#                     ("all", "particle_position_x"), ("all", "particle_position_z"),
#                     color="b")

# # pt.set_center((7000,3000))
# pt.set_origin(['lower','left','domain'])
# # pt.set_width(2, "Mpc")
# pt.save("/mnt/home/student/cranit/Repo/galspy/temp/plots/yt.png")

# ----- 
# slc = yt.SlicePlot(ds,'z',("io","density"),center=[7000,3000,600],width=(10000,'kpc'))
# # slc.set_origin(['lower','left','domain'])
# # slc.set_width(100, "kpc")

# slc.save("/mnt/home/student/cranit/Repo/galspy/temp/plots/yt.png")