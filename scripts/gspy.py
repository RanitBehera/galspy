#!/mnt/home/student/cranit/Repo/galspy/gsconda/bin/python
import galspy.console.terminal as pyterm

term = pyterm.Terminal()
term.AddPath("/mnt/home/student/cranit/Repo/galspy/commands",True)
term.AddPath("/mnt/home/student/cranit/Repo/galspy/scripts/temp/sims")


# UTF-8 Symbols
IC_SIM     = "\U0001F7CA"  # Club-Leaf
IC_SNAP    = "\U0001F790"  # Box
IC_HALO    = "\U0001F78A"  # Ring

def set_rprompt(env:dict):
    SIM = env.get("SIM") or ""
    SNAP = env.get("SNAP") or ""
    HALO = env.get("HALO") or ""

    rp = ""
    if not (HALO=="" or SNAP=="" or SIM==""):rp += f'{HALO} {IC_HALO}   '
    if not (SNAP=="" or SIM==""):rp += f'{SNAP} {IC_SNAP}   '
    rp += f'{SIM} {IC_SIM} '
    return rp

term.rprompt=set_rprompt

# term.env["HALO"] = 2212
# term.env["SNAP"] = 191
# term.env["SIM"] = "L250N2048"

term.Start()
