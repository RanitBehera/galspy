import galspy
import matplotlib.pyplot as plt
import numpy as np
from sphviewer.tools import camera_tools
import sphviewer as sph
import os


# Read From Box
L150N2040 = "/mnt/home/student/cranit/NINJA/simulations/L150N2040/SNAPS"
root = galspy.NavigationRoot(L150N2040)
parti = root.PART(63).DarkMatter
print("Reading Pos",flush=True)
pos = parti.Position(["00003A"]) /1000
print("Reading Mass",flush=True)
mass = parti.Mass(["00003A"])

# Create Scene
print("sph->particle",flush=True)
P = sph.Particles(pos, mass)
print("sph->Scene",flush=True)
S = sph.Scene(P)

# Set up Camera Angles
subject1 = [115.41,70.66,44.17]
subject2 = [110,75,50]

targets = [subject1,subject2]


anchors = {}
anchors['sim_times']    = [0.0, 1.0]
anchors['id_frames']    = [0, 50]
anchors['r']            = [2, 0.5]
anchors['id_targets']   = [0, 1]
anchors['t']            = [0, 'same']
anchors['p']            = [0, 'same']
anchors['zoom']         = [1., 1]
anchors['extent']       = [10, 'same']

data = camera_tools.get_camera_trajectory(targets, anchors)

FRAME_DUMP_PATH="/mnt/home/student/cranit/RANIT/Repo/galspy/scripts_2/pysphviewer/media/frames"
h = 0
for i in data:
    i['xsize'] = 1920
    i['ysize'] = 1080
    i['roll'] = 0
    S.update_camera(**i)
    R = sph.Render(S)
    img = R.get_image()
    # R.set_logscale()
    plt.imsave(f'{FRAME_DUMP_PATH}{os.sep}fr_' + str('%04d.png' % h), img, cmap='cubehelix')

    print('fr_' + str('%04d.png' % h))
    h += 1