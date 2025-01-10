import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import galspy, os
from galspy.utility.visualization import CubeVisualizer
import itertools
from scipy.spatial import KDTree
from scipy.ndimage import gaussian_filter
from scipy.signal import find_peaks



# Read