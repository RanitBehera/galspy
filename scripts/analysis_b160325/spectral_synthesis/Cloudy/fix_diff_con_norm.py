import galspec.Cloudy as cd
import matplotlib.pyplot as plt
import numpy as np

out = cd.CloudyOutputReader("/mnt/home/student/cranit/RANIT/Repo/galspy/study/cloudy/toymodel/eh","eh1")

conlam = out.Spectrum.Continuum.Frequency
coninc = out.Spectrum.Continuum.Incident
conout = out.Spectrum.Continuum.DiffuseOut

# dconlam = out.Spectrum.DiffuseContinuum.Energy
# dconout = out.Spectrum.DiffuseContinuum.ConEmitLocal

# tconlam = out.Spectrum.TwoPhotonContinuum.Energy
# tconout = out.Spectrum.TwoPhotonContinuum.nuFnu

plt.plot(conlam,coninc,label="inci",alpha=0.3)
plt.plot(conlam,conout,label="con")


# ===========================
CM_IN_PC = 3.086e18
# D=out.Overview.Depth[-2]
# dR=out.Overview.Depth[-1]-out.Overview.Depth[0]
# # # print(D)
# R0=out.Output.InnerRadius*(3.086e18)
# R=R0+D
# # V=4*np.pi*(R**2)*dD

# R=1*CM_IN_PC
# V= 4*np.pi*(R**2)*dR
# vals = (dconout*V/dconlam)

# plt.plot(dconlam,4*vals,label="diff con")
# =========================

data = np.loadtxt("/mnt/home/student/cranit/RANIT/Repo/galspy/study/cloudy/test/cn.diffcon")

lam = data[0]
diff = data[1:]/lam

total=0*lam
for d in diff:
    total = total+d
# plt.plot(lam,diff[0],label="One")
# plt.plot(lam,diff[-1],label="Two")

plt.plot(lam,total)


plt.xscale("log")
plt.yscale("log")
plt.legend()
plt.show()







