import galspec.Cloudy as gc
import numpy
import matplotlib.pyplot as plt
# from gen_sed import GenSED 

EH_DIR = "/mnt/home/student/cranit/RANIT/Repo/galspy/study/cloudy/uveffect/EH"
ES_DIR = "/mnt/home/student/cranit/RANIT/Repo/galspy/study/cloudy/uveffect/ES"
FH_DIR = "/mnt/home/student/cranit/RANIT/Repo/galspy/study/cloudy/uveffect/FH"
FS_DIR = "/mnt/home/student/cranit/RANIT/Repo/galspy/study/cloudy/uveffect/FS"
NH_DIR = "/mnt/home/student/cranit/RANIT/Repo/galspy/study/cloudy/uveffect/NH"

TEST_DIR = "/mnt/home/student/cranit/RANIT/Repo/galspy/study/cloudy/uveffect/Test"


# ================
clr=['r','g','b','c','m']
alp=[0.2,0.4,0.6,0.8,1]

MAX_INCIDENT = 0
ES_LEVEL = 0
for i in range(5):
    out = gc.CloudyOutput(NH_DIR,"nh"+str(i+1))
    # out = gc.CloudyOutput(NH_DIR,"nh"+str(i+1))
    con = out.Continuum

    plt.plot(con.Con.Frequency,con.Con.Incident/con.Con.Frequency,ls='-',lw=1,c=clr[i],alpha=1)
    plt.plot(con.Con.Frequency,con.Con.DiffuseOut/con.Con.Frequency,ls='-',c=clr[i],alpha=1)
    # plt.plot(con.Con.Frequency,con.Con.Reflection/con.Con.Frequency,ls='--',c='k',alpha=1)

    # plt.plot(con.TwoPhoton.Energy,con.TwoPhoton.Nu,c=clr[i])
    

    # plt.plot(con.Con.Frequency,con.Con.Total,ls='-',c=clr[i])#,label="Total")


    # inci = con.Con.Incident/con.Con.Frequency
    # max_inci = max(inci)
    # if max_inci>MAX_INCIDENT:MAX_INCIDENT=max_inci

    # if i==2:
    #     index=(con.Con.Frequency<800) & (con.Con.Frequency>400)
    #     ES_LEVEL=(con.Con.Incident/con.Con.Frequency)[index][-1]

    # plt.plot(con.Diffuse.Energy,con.Diffuse.ConEmitLocal,ls='-',lw=1,c=clr[i])
    # plt.plot(con.Diffuse.Energy,con.Diffuse.DiffuseLineEmission)
    # plt.plot(con.Diffuse.Energy,con.Diffuse.Total)
    # plt.plot(con.Grain.Energy,con.Grain.Grapahite)
    # plt.plot(con.Grain.Energy,con.Grain.Rest)
    # plt.plot(con.TwoPhoton.Energy,con.TwoPhoton.Nu)
    # break



plt.xscale('log')
plt.yscale('log')
# plt.xlim(200,8000)
# maxL=max(con.Con.Incident/con.Con.Frequency)
# plt.ylim(maxL*1e-6,maxL*1e3) #EH
# plt.ylim(maxL*1e-5,maxL*1e1) #ES

# plt.ylim(0.9e30,1.1e40)



# Lines
# LINES ={
#     "Ha"    : [6564.61,"H $\\alpha$"], 
#     "Hb"    : [4862.68,"H $\\beta$"],
#     "OII"   : [3727.092,"O II"],
#     "OIII"  : [5008.240,"O III"],
#     "OI"    : [6302.046,"O I"],
#     "NeV"   : [3346.79,"Ne V"],
#     "OIII2" : [1665.85,"O III"],
#     "HeII"  : [1640.4,"He II"],
#     "CIV"   : [1549.48,"C IV"],
#     "SiIV"  : [1397.61,"Si IV"],
#     "CII"   : [1335.31,"C II"],
#     "CIII"  : [1908.734,"C III"],
#     "OI"    : [1305.53,"O I"],
#     "NV"    : [1240.81,"N V"],
#     "Lya"   : [1215.24,"Ly $\\alpha$"]     
# }

# tloc=[]
# tname=[]
# for key,val in LINES.items():
#     tloc.append(val[0])
#     tname.append(val[1])
#     plt.axvline(val[0],ls='--',color='k',lw=1,alpha=0.2)

ax=plt.gca()
# ax2=ax.twiny()
# ax2.set_xscale('log')
# min_lam,max_lam = ax.get_xlim()
# ax2.set_xlim(min_lam,max_lam)
# ax2.set_xticks(tloc)
# ax2.set_xticklabels(tname)
# ax2.minorticks_off()
# plt.setp( ax2.xaxis.get_majorticklabels(), rotation=90 )


if False:#EH
    plt.plot((200,1000),(MAX_INCIDENT,MAX_INCIDENT),ls='--',color='k',alpha=0.3)
    plt.annotate('$\\times$0.800',xy=(500,MAX_INCIDENT*0.8),xytext=(0,-2),textcoords="offset pixels",ha="center",va='top',alpha=0.5)
    plt.annotate('$\\times$0.150',xy=(500,MAX_INCIDENT*0.150),xytext=(0,-2),textcoords="offset pixels",ha="center",va='top',alpha=0.5)
    plt.annotate('$\\times$0.028',xy=(500,MAX_INCIDENT*0.028),xytext=(0,-2),textcoords="offset pixels",ha="center",va='top',alpha=0.5)
    plt.annotate('$\\times$0.005',xy=(500,MAX_INCIDENT*0.005),xytext=(0,-2),textcoords="offset pixels",ha="center",va='top',alpha=0.5)
    plt.annotate('$\\times$0.001',xy=(500,MAX_INCIDENT*0.001),xytext=(0,-2),textcoords="offset pixels",ha="center",va='top',alpha=0.5)

if False:#ES
    plt.annotate('$\\times$0.500',xy=(300,ES_LEVEL),xytext=(0,-2),textcoords="offset pixels",ha="center",va='top',alpha=0.5)

if False:#FH
    plt.plot((200,1000),(MAX_INCIDENT,MAX_INCIDENT),ls='--',color='k',alpha=0.3)
    plt.annotate('$\\times$0.001',xy=(500,MAX_INCIDENT*0.001),xytext=(0,-2),textcoords="offset pixels",ha="center",va='top',alpha=0.5)

if True:#FS
    pass




ax.set_xlabel("Wavelength $(\\AA)$")
ax.set_ylabel("Luminosity (erg s$^{-1}$ $\\AA^{-1}$)")

plt.show()