import galspy as gs


SIM = gs.NavigationRoot(gs.NINJA.L250N2040)
PIG=SIM.PIG(z=6)
PIG.print_box_info()

cs=PIG.GetCentralStarPosition()