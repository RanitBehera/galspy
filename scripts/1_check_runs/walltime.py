import numpy as np
import matplotlib.pyplot as plt
import io

import matplotlib
matplotlib.rcParams['font.size']=12


# PBS_PATH = "/mnt/home/student/cranit/NINJA/simulations/L150N2040/run/PBS"
# JOB_IDS = [58553,64554,66876]


fig,axs = plt.subplots(1,1)

# Get stdout filepaths
def DoFor(PBS_PATH,JOB_IDS,clr='k'):
    STDOUTS = [f"{PBS_PATH}/{jid}.hn1/stdout.txt" for jid in JOB_IDS]

    # Initialise global variables
    wall_time = np.array([])
    redshift = np.array([])
    count_bh = np.array([])
    count_star = np.array([])

    # Read stdout and scrape text
    job_wall_time_offset = 0
    for filepath in STDOUTS: 
        with open(filepath) as fp:stdout = fp.read()
        line_begin_step = [line for line in stdout.split("\n") if line[14:24]=="Begin Step"]
        line_num_part = [line for line in stdout.split("\n") if line[14:24]=="TotNumPart"]
        # Buffer Files
        bf_step = io.StringIO("\n".join(line_begin_step).replace(',',''))
        bf_part = io.StringIO("\n".join(line_num_part).replace(',',''))
        
        job_wall_time,job_scale_factor,job_redshift = np.loadtxt(bf_step,usecols=[1,7,10]).T
        job_count_bh,job_count_star = np.loadtxt(bf_part,usecols=[8,10]).T

        job_wall_time +=job_wall_time_offset
        wall_time = np.concatenate((wall_time,job_wall_time))
        job_wall_time_offset = wall_time[-1]

        redshift = np.concatenate((redshift,job_redshift))
        count_bh = np.concatenate((count_bh,job_count_bh))
        count_star = np.concatenate((count_star,job_count_star))
    
        # PLOT
        wall_time_hr=wall_time/3600
        axs.plot(wall_time_hr,redshift,color=clr)
        # axs.plot(wall_time/3600,scale_factor,'-')

DoFor("/mnt/home/student/cranit/NINJA/simulations/L150N2040/run/PBS",[58553,64554,66876],'r')
DoFor("/mnt/home/student/cranit/NINJA/simulations/L250N2040/run/PBS",[68839],'b')

# BEAUTIFY
UNIT_SPAN = 12
TIME_RANGE = 24*12
TIME_REFS = np.arange(0,TIME_RANGE+UNIT_SPAN,UNIT_SPAN)
for span_start,span_end in zip(TIME_REFS[:-1],TIME_REFS[1:]):
    if (span_start/UNIT_SPAN)%2 == 0: alp = 0.05
    else: alp = 0.03
    plt.axvspan(span_start,span_end,color='k',alpha = alp,ec=None)
    if span_start % 24 ==0:
        plt.axvline(span_start,color='k',linestyle='-',alpha=0.2,lw=1)

# ANNONATION
ARROW_STYLE = dict(width=0.5,headwidth=8,headlength=8,shrink=0.1,facecolor=(0,0,0,1))
BBOX_FACECOLOR = (0,0,0,0.05)
BBOX_EDGECOLOR = (0,0,0,0.1)

# # First Star
# ind_first_star = np.where(count_star>0)[0][0]
# plt.plot(wall_time_hr[ind_first_star],redshift[ind_first_star],'k*',ms=16,markeredgecolor=(1,1,1))
# plt.annotate(f"First Star\n$z={round(redshift[ind_first_star],2)}$",(wall_time_hr[ind_first_star],redshift[ind_first_star]),
#              xytext=(0,100),textcoords="offset pixels",ha='center',
#              bbox=dict(facecolor=BBOX_FACECOLOR, edgecolor=BBOX_EDGECOLOR, boxstyle='round,pad=0.5'),
#              arrowprops=ARROW_STYLE)
# # First BH
# ind_first_bh = np.where(count_bh>0)[0][0]
# plt.plot(wall_time_hr[ind_first_bh],redshift[ind_first_bh],'k.',ms=16,markeredgecolor=(1,1,1))
# plt.annotate(f"First BH\n$z={round(redshift[ind_first_bh],2)}$",(wall_time_hr[ind_first_bh],redshift[ind_first_bh]),
#              xytext=(0,100),textcoords="offset pixels",ha='center',
#              bbox=dict(facecolor=BBOX_FACECOLOR, edgecolor=BBOX_EDGECOLOR, boxstyle='round,pad=0.5'),
#              arrowprops=ARROW_STYLE)

# Latest Redshift
# plt.plot(wall_time_hr[-1],redshift[-1],'ks',ms=4)
# plt.annotate(f"Latest\n$z={round(redshift[-1],2)}$",(wall_time_hr[-1],redshift[-1]),
#              xytext=(0,100),textcoords="offset pixels",ha='center',
#              bbox=dict(facecolor=BBOX_FACECOLOR, edgecolor=BBOX_EDGECOLOR, boxstyle='round,pad=0.5'),
#              arrowprops=ARROW_STYLE)


# Stellar Count
# plt.plot(50*count_star/max(count_star),'-',label="stars")




# CRUDE FITTING
#=========================
# SLOPE_START = 1600
# SLOPE_END = 3000
# # print(len(wall_time_hr))
# # plt.plot([wall_time_hr[SLOPE_START],wall_time_hr[SLOPE_END]],[redshift[SLOPE_START],redshift[SLOPE_END]],'.',ms=10)
# lwt = np.log10(wall_time_hr)
# lred = np.log10(redshift)
# slope = (lred[SLOPE_START]-lred[SLOPE_END])/(lwt[SLOPE_START]-lwt[SLOPE_END])
# xr = np.log10(np.linspace(50,24*12,200))
# yr = lred[SLOPE_END] + slope * (xr-lwt[SLOPE_END])

# lin_red = 10**yr
# lin_lwt = 10**xr
# plt.plot(lin_lwt,lin_red,'r:',zorder=-99)
#=========================



plt.xticks(range(0,TIME_RANGE+1,2*UNIT_SPAN))
plt.yticks(range(0,101,10))
plt.gca().yaxis.grid(True,alpha=0.5)
plt.xlabel("Wall-Time (Hours)")
plt.ylabel("Redshift ($z$)")
# plt.yscale('log')
# plt.xscale('log')
plt.ylim(1,100)
plt.xlim(0,TIME_RANGE)
plt.title("Run Time Log",fontsize=16)
plt.legend()
plt.show()