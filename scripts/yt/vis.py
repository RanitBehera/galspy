import yt
import galspy.IO.MPGadget as mp



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
data = {
    # GAS
    ("gas", "particle_position_x"): ppxg,
    ("gas", "particle_position_y"): ppyg,
    ("gas", "particle_position_z"): ppzg,
    ("gas", "particle_velocity_x"): pvxg,
    ("gas", "particle_velocity_y"): pvyg,
    ("gas", "particle_velocity_z"): pvzg,
    ("gas", "particle_mass"): mg,
    ("gas", "smoothing_length"): sml,
    ("gas", "density"): dens,
    # DM
    ("dm", "particle_position_x"): ppxd,
    ("dm", "particle_position_y"): ppyd,
    ("dm", "particle_position_z"): ppzd,
    ("dm", "particle_velocity_x"): pvxd,
    ("dm", "particle_velocity_y"): pvyd,
    ("dm", "particle_velocity_z"): pvzd,
    ("dm", "particle_mass"): md,
    # STAR
    ("star", "particle_position_x"): ppxs,
    ("star", "particle_position_y"): ppys,
    ("star", "particle_position_z"): ppzs,
    ("star", "particle_velocity_x"): pvxs,
    ("star", "particle_velocity_y"): pvys,
    ("star", "particle_velocity_z"): pvzs,
    ("star", "particle_mass"): ms,
}

ds = yt.load_particles(
        data,
        bbox=[[0,10000],[0,10000],[0,10000]]
    )




# ================ 
# Setup YT
# ================ 
yt.toggle_interactivity()
# ds_dm.add_sph_fields()


# slc.save("/mnt/home/student/cranit/Repo/galspy/temp/plots/yt.png")

p = yt.ParticlePlot(ds, ("all", "particle_position_x"), ("all", "particle_position_y"), color="b")

p.set_unit(("all", "particle_position_x"), "kpc")
# p.set_unit(("all", "particle_velocity_z"), "km/s")
# p.set_unit(("all", "particle_mass"), "Msun")

# p.set_width(500, "kpc")




# p.show()
p.save("/mnt/home/student/cranit/Repo/galspy/temp/plots/yt.png")