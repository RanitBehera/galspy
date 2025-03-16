import numpy as np
import matplotlib.pyplot as plt
import os
import galspec.Cloudy as cd

PATH = "/mnt/home/student/cranit/RANIT/Repo/galspy/study/cloudy/bpass_1Myr/hden"
# FILES = ["r1","r2","r3","r4","r5"]
FILES = ["hd1","hd2","hd3","hd4","hd5"]


# BANKS
ri_bank=[]
rat_bank=[]
beta_in_bank=[]
beta_out_bank=[]
beta_tot_bank=[]

for FN in FILES:
    cld = cd.CloudyOutputReader(PATH,FN)
    ri=cld.Output.InnerRadius

    # ======================
    con = cld.Spectrum.Continuum

    LB_L = 1400
    LB_R = 1500
    HB_L = 2500
    HB_R = 2600

    mask_LB = (con.Frequency>LB_L)&(con.Frequency<LB_R)
    mask_HB = (con.Frequency>HB_L)&(con.Frequency<HB_R)

    LB_Lf,LB_Rf = con.Frequency[mask_LB][[0,-1]][::-1]
    HB_Lf,HB_Rf = con.Frequency[mask_HB][[0,-1]][::-1]

    def Integrate(ang,sflux,intg_mask):
        lam = ang[intg_mask][::-1]
        sflux = sflux[intg_mask][:-1]
        dlam = np.diff(lam)
        flux = np.sum(sflux*dlam)
        return flux
    
    flx_in_LB=Integrate(con.Frequency,con.Incident,mask_LB)/(LB_Rf-LB_Lf)
    flx_out_LB=Integrate(con.Frequency,con.DiffuseOut,mask_LB)/(LB_Rf-LB_Lf)
    flx_tot_LB=Integrate(con.Frequency,con.Total,mask_LB)/(LB_Rf-LB_Lf)
    
    flx_in_HB=Integrate(con.Frequency,con.Incident,mask_HB)/(HB_Rf-HB_Lf)
    flx_out_HB=Integrate(con.Frequency,con.DiffuseOut,mask_HB)/(HB_Rf-HB_Lf)
    flx_tot_HB=Integrate(con.Frequency,con.Total,mask_HB)/(HB_Rf-HB_Lf)
    # ======================

    ri_bank.append(ri)
    rat_bank.append(flx_tot_LB/flx_in_LB)

    def GetBeta(LB,HB):
        ratio = LB/HB
        beta = np.log10(ratio)/np.log10((LB_L+LB_R)/(HB_L+HB_R))
        return beta

    beta_in_bank.append(GetBeta(flx_in_LB,flx_in_HB))
    beta_out_bank.append(GetBeta(flx_out_LB,flx_out_HB))
    beta_tot_bank.append(GetBeta(flx_tot_LB,flx_tot_HB))

# plt.plot(ri_bank,rat_bank,'.-')
# plt.plot([1,2,3,4,5],rat_bank,'.-')

plt.plot(beta_in_bank,beta_tot_bank)

# plt.axhspan(0,10,color='k',alpha=0.1,ec=None)

plt.show()