import galspy
from galspy.Spectra.Templates import Templates


tp = Templates()

sal100=tp.GetStellarTemplates("SALPETER_UPTO_100M","Binary")
chab100=tp.GetStellarTemplates("CHABRIER_UPTO_100M","Binary")

