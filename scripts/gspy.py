#!/mnt/home/student/cranit/Repo/galspy/gsconda/bin/python
import galspy.console.terminal as pyterm

term = pyterm.Terminal()
term.AddPath("/mnt/home/student/cranit/Repo/galspy/commands")
term.AddPath("/mnt/home/student/cranit/Repo/galspy/commands/bigfile")
term.AddPath("/mnt/home/student/cranit/Repo/galspy/scripts/temp/sims")
term.Start()