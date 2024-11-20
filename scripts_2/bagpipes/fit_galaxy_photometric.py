import numpy as np
import bagpipes as pipes
import matplotlib.pyplot as plt
import os

def load_data(ID:str):
    # Temporary now
    # Later relate to sim gid

    photometry = np.loadtxt("/mnt/home/student/cranit/RANIT/Repo/galspy/scripts_2/bagpipes/data/demo_model.phot")
    return photometry
