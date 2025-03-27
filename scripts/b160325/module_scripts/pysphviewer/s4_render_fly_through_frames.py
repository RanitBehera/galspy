# %%
import galspy
import matplotlib.pyplot as plt
import numpy as np
from sphviewer.tools import camera_tools
import sphviewer as sph
import os
import pickle

SUFFIX = "gas"

with open(f"/mnt/home/student/cranit/RANIT/Repo/galspy/scripts_2/pysphviewer/data/pos_{SUFFIX}.dat","rb") as fp:
    pos=pickle.load(fp)/1000

with open(f"/mnt/home/student/cranit/RANIT/Repo/galspy/scripts_2/pysphviewer/data/mass_{SUFFIX}.dat","rb") as fp:
    mass=pickle.load(fp)




# Create Scene
print("sph->particle",flush=True)
P = sph.Particles(pos, mass)
print("sph->Scene",flush=True)
S = sph.Scene(P)


# Set up Camera Angles

subject1 = [131.46260496180426,15.102526179407781,91.82829217856088]
subject2 = [131.46260496180426,15.102526179407781,91.82829217856088]

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

FRAME_DUMP_PATH=f"/mnt/home/student/cranit/RANIT/Repo/galspy/scripts_2/pysphviewer/media/fr_{SUFFIX}"     #<-----
h = 0
for i in data:
    i['xsize'] = 1080
    i['ysize'] = 1080
    i['roll'] = 0
    S.update_camera(**i)
    R = sph.Render(S)
    img = R.get_image()
    # R.set_logscale()
    img=img**0.3
    # img=1/(1+np.exp(-1*(img-0.5)))
    # img=np.clip((img/1)**0.3,0,)
    plt.imsave(f'{FRAME_DUMP_PATH}{os.sep}fr_' + str('%04d.png' % h), img, cmap='plasma')

    print('fr_' + str('%04d.png' % h))
    h += 1
