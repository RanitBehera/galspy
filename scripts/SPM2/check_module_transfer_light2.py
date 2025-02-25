import galspy as gs



root=gs.NavigationRoot(gs.NINJA.L150N2040)

PIG=root.PIG(43)

spm=gs.PIGSpectrophotometry(PIG)

spm.get_spectrum_dict(1)







