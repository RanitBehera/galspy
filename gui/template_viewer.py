from galspy.Spectra import SpectralTemplates
import tkinter as tk
from tkinter import messagebox
import os
import numpy
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk

TEMPLATES_DIR = "/mnt/home/student/cranit/RANIT/Repo/galspy/cache/spectra/array" 
TEMPLATES = [
    "stellar_chabrier300_bin.specs",
    # "nebular_in_chabrier300_bin.specs",
    # "nebular_out_chabrier300_bin.specs",
    "stellar_chabrier100_bin.specs",
    "stellar_salpeter100_bin.specs"
]

# Check default_check variable below

# ===== FILEPATHS
TEMPLATES_FILEPATHS = [TEMPLATES_DIR + os.sep + tmp for tmp in TEMPLATES]

# ===== HELPER FUNCTIONS
def blank_callback_mpl(event):
    return

def tkinter_show_info(msg:str,title:str="Info"):
    messagebox.showinfo(title, msg)






_FIRST_DRAW=True
def update_matplotlib():
    global _FIRST_DRAW
    chk_files=[file for file, status in file_checks.items() if status.get()]
    chk_metals=[Z for Z, status in Z_checks.items() if status.get()]
    chk_ages=[T for T, status in T_checks.items() if status.get()]

    if not _FIRST_DRAW:
        xlim = plt.gca().get_xlim()
        ylim = plt.gca().get_ylim()

    plt.clf()
    for file in chk_files:
        specs = SpectralTemplates.GetTemplates(TEMPLATES_DIR + os.sep + file)
        for Z in chk_metals:
            Z_index = METALLICITY.index(Z)
            for T in chk_ages:
                T_index = AGES.index(T)
                specindex = 1+(Z_index*len(AGES)+T_index)
                spec = specs[specindex]
                plt.plot(specs[0],spec,label=f"Z={Z},T={T}")

    handles, labels = plt.gca().get_legend_handles_labels()
    if handles:
        plt.legend(ncol=len(chk_files))

    if not _FIRST_DRAW:
        plt.xlim(xlim)
        plt.ylim(ylim)

    plt.xscale("log")
    plt.yscale("log")

    plt.xlabel("Wavelength $(\AA)$")
    plt.ylabel("Spectral Luminosity $(L_\odot/\AA)$")

    plt.draw()
    _FIRST_DRAW=False





# ===== TKINTER
root = tk.Tk()
root.title("Spectral Template Viewer")

# ----- Pack matplotlib figure

fig, ax = plt.subplots()
# fig= plt.figure(figsize=(6, 4), dpi=100)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()
toolbar.pack(side=tk.TOP, fill=tk.X)

# ----- Menubar
menubar = tk.Menu(root)

# Template
file_checks = {file: tk.BooleanVar() for file in TEMPLATES}
file_menu = tk.Menu(menubar, tearoff=0)
for file in TEMPLATES:
    file_menu.add_checkbutton(
        label=file,
        variable=file_checks[file],
        onvalue=True,
        offvalue=False,
        command=lambda:update_matplotlib()
    )
menubar.add_cascade(label="Files", menu=file_menu)

# Metallicity
METALLICITY=[0.00001,0.0001,0.001,0.002,0.003,0.004,0.006,0.008,0.010,0.014,0.020,0.040]
Z_checks = {Z: tk.BooleanVar() for Z in METALLICITY}
metallicity_menu = tk.Menu(menubar, tearoff=0)
for Z in METALLICITY:
    metallicity_menu.add_checkbutton(
        label=f"{Z}",
        variable=Z_checks[Z],
        onvalue=True,
        offvalue=False,
        command=lambda:update_matplotlib()
    )
menubar.add_cascade(label="Metallicity", menu=metallicity_menu)

# Ages
AGES=[numpy.round(T,1) for T in numpy.arange(6.0,11.1,0.1)]
T_checks = {T: tk.BooleanVar() for T in AGES}
age_menu = tk.Menu(menubar, tearoff=0)
for T in AGES:
    age_menu.add_checkbutton(
        label=str(T),
        variable=T_checks[T],
        onvalue=True,
        offvalue=False,
        command=lambda:update_matplotlib()
    )
    if int(10*T)%10==9:age_menu.add_separator()
menubar.add_cascade(label="Age", menu=age_menu)

# Utility
# Utility State Variables
TK_SHOW_FILENAME_ON_HOVER=tk.BooleanVar()

def on_move(event):
    ax=plt.gca()
    if not event.inaxes == ax:return
    x_min, x_max = numpy.array(ax.get_xlim())
    y_min, y_max = numpy.array(ax.get_ylim())

    if plt.gca().get_xscale()=="log":
        x_min,x_max=numpy.log10(x_min),numpy.log10(x_max)
    if plt.gca().get_yscale()=="log":
        y_min,y_max=numpy.log10(y_min),numpy.log10(y_max)

    x_span = x_max - x_min
    y_span = y_max - y_min
    

    # mouse position
    mouse_x = (event.xdata-x_min)/x_span
    mouse_y = (event.ydata-y_min)/y_span

    inax_lines = plt.gca().get_lines()

    slice_points = []
    for line in inax_lines:
        # normalised
        xdata = (numpy.log10(line.get_xdata())-x_min)/x_span
        ydata = (numpy.log10(line.get_ydata())-y_min)/y_span

        closest_x_index = numpy.argmin(numpy.abs(xdata-mouse_x))
        cxi = closest_x_index
        slice_points.append((xdata[cxi],ydata[cxi])) 

    ngb_dist=[]
    for x,y in slice_points:
        dist = (((x-mouse_x)/x_span)**2 + ((y-mouse_y)/y_span))**0.5
        ngb_dist.append(dist)

    min_dist_line_index = numpy.argmin(ngb_dist)
    print(ngb_dist[min_dist_line_index])



_listener_obj = None
def toggle_view_filename_on_hover():
    global _listener_obj
    if TK_SHOW_FILENAME_ON_HOVER.get():
        _listener_obj = fig.canvas.mpl_connect('motion_notify_event', on_move)
    else:
        fig.canvas.mpl_disconnect(_listener_obj)





view_menu = tk.Menu(menubar,tearoff=0)
view_menu.add_checkbutton(label="Filename on Hover",variable=TK_SHOW_FILENAME_ON_HOVER,onvalue=True,offvalue=False,command=toggle_view_filename_on_hover)

menubar.add_cascade(label="View", menu=view_menu)


# Set default checks
default_files = ["stellar_salpeter100_bin.specs"]
default_metals = [0.00001]
default_ages = [6.0]

for file in default_files:
    if file in file_checks:
        file_checks[file].set(True)

for Z in default_metals:
    if Z in Z_checks:
        Z_checks[Z].set(True)

for T in default_ages:
    if T in T_checks:
        T_checks[T].set(True)

update_matplotlib()



root.config(menu=menubar)
root.protocol("WM_DELETE_WINDOW", lambda:root.quit())
root.mainloop()