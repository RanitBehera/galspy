#!/home/ranit/MyDrive/Repo/galspy/gspy/bin/python
import galspy.console.terminal as pyterm

term = pyterm.Terminal("GalSpy Terminal")
term.AddPath("/home/ranit/MyDrive/Repo/galspy/commands")
term.AddPath("/home/ranit/MyDrive/Tests/gspy/Sims")

term.Start()
