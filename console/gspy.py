#!/mnt/home/student/cranit/Repo/galspy/gsconda/bin/python
import galterm.terminal as pyterm

term = pyterm.Terminal()
term.AddPath("/mnt/home/student/cranit/Repo/galspy/console/commands",True)
term.AddPath("/mnt/home/student/cranit/Repo/galspy/temp/sims")


# UTF-8 Symbols
IC_SIM     = "\U0001F7CA"  # Club-Leaf
IC_SNAP    = "\U0001F790"  # Box
IC_HALO    = "\U0001F78A"  # Ring

def set_rprompt(env:dict):
    SIM = env.get("SIM","")
    SNAP = env.get("SNAP","")
    HALO = env.get("HALO","")

    rp = ""
    if not (HALO=="" or SNAP=="" or SIM==""):rp += f'{HALO} {IC_HALO}   '
    if not (SNAP=="" or SIM==""):rp += f'{SNAP} {IC_SNAP}   '
    rp += f'{SIM} {IC_SIM} '
    return rp

term.rprompt=set_rprompt
term.Start()
