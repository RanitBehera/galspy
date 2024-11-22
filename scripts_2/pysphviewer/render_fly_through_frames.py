import galspy
import matplotlib.pyplot as plt
import numpy as np
from sphviewer.tools import camera_tools
import sphviewer as sph
import os


n1 = 10000

n1 = 10000

L150N2040 = "/mnt/home/student/cranit/NINJA/simulations/L150N2040/SNAPS"
root = galspy.NavigationRoot(L150N2040)
parti = root.PART(63).DarkMatter
print("Reading Pos",flush=True)
# BLOBS=["000000","000001","000002"]
pos = parti.Position(["000001"]) /1000
# gid = parti.GroupID()
print("Reading Mass",flush=True)
mass = parti.Mass(["000001"])

# mass=mass/np.max(mass)
# mass=mass

print("sph->particle",flush=True)
P = sph.Particles(pos, mass)
print("sph->Scene",flush=True)
S = sph.Scene(P)

cm_1 = [20,6,6]
cm_2 = [8,8,8]

targets = [cm_1,cm_2]

anchors = {}
anchors['sim_times'] = [0.0, 1.0]
anchors['id_frames'] = [0, 50]
anchors['r']         = [2, 'same']
anchors['id_targets'] = [0, 1]
anchors['t']         = [0, 'same']
anchors['p']         = [0, 'same']
anchors['zoom']      = [1., 'same']
anchors['extent']    = [10, 'same']

data = camera_tools.get_camera_trajectory(targets, anchors)

FRAME_DUMP_PATH="/mnt/home/student/cranit/RANIT/Repo/galspy/scripts_2/pysphviewer/media/frames"
h = 0
for i in data:
    i['xsize'] = 250
    i['ysize'] = 250
    i['roll'] = 0
    S.update_camera(**i)
    R = sph.Render(S)
    img = R.get_image()
    # R.set_logscale()
    plt.imsave(f'{FRAME_DUMP_PATH}{os.sep}fr_' + str('%04d.png' % h), img, cmap='cubehelix')

    print('fr_' + str('%04d.png' % h))
    h += 1