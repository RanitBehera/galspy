import numpy
import tkinter as tk
import matplotlib.pyplot as plt
import tkinter.font as tkfont

# ====== TKINTER ======
root = tk.Tk()
root.title("Rockstar-Galaxies Halo Explorer")
root.geometry("800x600")
def quit_me():
    root.destroy()
    root.quit()
root.protocol("WM_DELETE_WINDOW", quit_me)

MENU_FONT = ("gothic",12)

# MENUBAR
menu_root = tk.Menu()

menu_fof = tk.Menu(menu_root,tearoff=0)
menu_fof.add_command(label="Next",font=MENU_FONT)
menu_fof.add_command(label="Prev",font=MENU_FONT)
menu_fof.add_command(label="Jump",font=MENU_FONT)
menu_root.add_cascade(label="SubHalo",font=MENU_FONT,menu=menu_fof)



# fof = tk.Menu(menu,tearoff=0)



# menu.add_checkbutton(label="Log X",command=None)
# menu.add_checkbutton(label="Log Y",command=None)


root.config(menu=menu_root)
root.mainloop()




