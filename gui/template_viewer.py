import galspy as gs
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
    "nebular_in_chabrier300_bin.specs",
    "nebular_out_chabrier300_bin.specs"
]

# ===== FILEPATHS
TEMPLATES_FILEPATHS = [TEMPLATES_DIR + os.sep + tmp for tmp in TEMPLATES]

# ===== HELPER FUNCTIONS
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
        specs = gs.SpectralTemplates.GetTemplates(TEMPLATES_DIR + os.sep + file)
        for Z in chk_metals:
            Z_index = METALLICITY.index(Z)
            for T in chk_ages:
                T_index = AGES.index(T)
                specindex = 1+(Z_index*len(AGES)+T_index)
                spec = specs[specindex]
                plt.plot(specs[0],spec,label=f"Z={Z},T={T}")

    plt.legend()

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


# Set default checks
default_files = ["nebular_in_chabrier300_bin.specs"]
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