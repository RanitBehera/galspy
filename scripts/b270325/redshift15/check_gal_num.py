import galspy as gs

SIM = gs.NavigationRoot(gs.NINJA.L150N2040_WIND_WEAK)
z=15
SN = SIM.SnapNumFromRedshift(z)
PIG = SIM.PIG(SN)


SM=PIG.FOFGroups.MassByType().T[4]

print("Total :",len(SM))

mask = SM>10*PIG.Header.MassTable()[4]

print("Filter by Mass :",f"{10*PIG.Header.MassTable()[4]*1e10/0.6736:0.02e}")
print("Filtered :",len(SM[mask]))