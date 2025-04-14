import numpy as np
import galspy.FileTypes.ConfigFile as cf

FILE="/mnt/home/student/cranit/NINJA/simulations/L50N2040/run/paramfile.gadget"

param = cf.ReadAsDictionary(FILE)


outlist = param["OutputList"]

CLM_SIZE=16
print("#".ljust(4),"|","a(t)".center(CLM_SIZE),"|","z".ljust(CLM_SIZE))
for i,ol in enumerate(outlist):
    print(
            f"{i}".ljust(4),
            "|",
            f"{ol:.06f}".center(CLM_SIZE),
            "|",
            f"{(1/ol)-1:.02f}".ljust(CLM_SIZE)
          )

