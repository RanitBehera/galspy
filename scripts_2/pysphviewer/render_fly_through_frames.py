# %%
import galspy
import matplotlib.pyplot as plt
import numpy as np
from sphviewer.tools import camera_tools
import sphviewer as sph
import os
import pickle

# Read From Box
# L150N2040 = "/mnt/home/student/cranit/NINJA/simulations/L150N2040/SNAPS"
# root = galspy.NavigationRoot(L150N2040)
# parti = root.PART(43).DarkMatter
# print("Reading Pos",flush=True)
# pos = parti.Position(["00003A"]) /1000
# print("Reading Mass",flush=True)
# mass = parti.Mass(["00003A"])



with open("/mnt/home/student/cranit/RANIT/Repo/galspy/temp/share_somak/pos.dat","rb") as fp:
    pos=pickle.load(fp)/1000

with open("/mnt/home/student/cranit/RANIT/Repo/galspy/temp/share_somak/mass.dat","rb") as fp:
    mass=pickle.load(fp)




# Create Scene
print("sph->particle",flush=True)
P = sph.Particles(pos, mass)
print("sph->Scene",flush=True)
S = sph.Scene(P)

# %%
# Set up Camera Angles
subject1 = [82.84100556727144,42.78881572122996,109.84212366192622]
subject2 = [82.84100556727144,42.78881572122996,109.84212366192622]

targets = [subject1,subject2]


anchors = {}
anchors['sim_times']    = [0.0, 1.0]
anchors['id_frames']    = [0, 300]
anchors['r']            = [2, 'same']
anchors['id_targets']   = [0, 1]
anchors['t']            = [0, 'same']
anchors['p']            = [0, 359]
anchors['zoom']         = [1, 1]
anchors['extent']       = [10, 'same']

data = camera_tools.get_camera_trajectory(targets, anchors)

FRAME_DUMP_PATH="/mnt/home/student/cranit/RANIT/Repo/galspy/scripts_2/pysphviewer/media/frames"
h = 0
for i in data:
    i['xsize'] = 1080
    i['ysize'] = 1080
    i['roll'] = 0
    S.update_camera(**i)
    R = sph.Render(S)
    img = R.get_image()
    # R.set_logscale()
    plt.imsave(f'{FRAME_DUMP_PATH}{os.sep}fr_' + str('%04d.png' % h), img**0.1, cmap='cubehelix')

    print('fr_' + str('%04d.png' % h))
    h += 1

# %%
