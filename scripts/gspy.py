#!/mnt/home/student/cranit/Repo/galspy/gsconda/bin/python
import galspy.console.terminal as pyterm

term = pyterm.Terminal()
term.AddPath("/mnt/home/student/cranit/Repo/galspy/commands",True)
term.AddPath("/mnt/home/student/cranit/Repo/galspy/scripts/temp/sims")
term.Start()
