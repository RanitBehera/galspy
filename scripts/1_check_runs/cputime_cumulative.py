import numpy as np
import matplotlib.pyplot as plt
import io

import matplotlib
matplotlib.rcParams['font.size']=12

from galspy.utility.Figure.Beautification import SetMyStyle
SetMyStyle()


fig,axs = plt.subplots(1,1)

# Get stdout filepaths
def DoFor(PBS_PATH,JOB_IDS,label,clr='k'):
    STDOUTS = [f"{PBS_PATH}/{jid}.hn1/stdout.txt" for jid in JOB_IDS]

    # Initialise global variables
    wall_time = np.array([])
    redshift = np.array([])

    # Read stdout and scrape text
    job_wall_time_offset = 0
    for filepath in STDOUTS: 
        with open(filepath) as fp:stdout = fp.read()
        line_begin_step = [line for line in stdout.split("\n") if line[14:24]=="Begin Step"]
        # Buffer Files
        bf_step = io.StringIO("\n".join(line_begin_step).replace(',',''))
        
        job_wall_time,job_scale_factor,job_redshift = np.loadtxt(bf_step,usecols=[1,7,10]).T

        job_wall_time +=job_wall_time_offset
        wall_time = np.concatenate((wall_time,job_wall_time))
        job_wall_time_offset = wall_time[-1]

        redshift = np.concatenate((redshift,job_redshift))
    
        # PLOT
        wall_time_hr=wall_time/3600

        cpu_hrs = wall_time_hr * 1920 

        # cpu_hrs_cum = np.cumsum(cpu_hrs)
        axs.plot(redshift,cpu_hrs/1e5,color=clr,label=label)

DoFor("/mnt/home/student/cranit/NINJA/simulations/L150N2040/run/PBS",[58553,64554,66876],"L150N2040",'m')
DoFor("/mnt/home/student/cranit/NINJA/simulations/L250N2040/run/PBS",[68839,71230],"L250N2040",'c')



plt.yscale("log")
plt.xscale("log")
plt.xlim(1,100)
plt.ylim(0.01,50)
plt.axvline(5,ls='--',color='k')
plt.xlabel("Redshift")
plt.ylabel("Runtime (CPU Hours/$10^5$)")

plt.xticks([1,5,10,50,100],labels=["1","5","10","50","100"])
plt.yticks([0.01,0.1,1,10],["0.01","0.1","1","10"])


# MANUAL LEGEND
import matplotlib.lines as mlines
box_L150N2040 = mlines.Line2D([], [], color='m', marker='',markersize=8, label='L150N2040')
box_L250N2040 = mlines.Line2D([], [], color='c', marker='',markersize=8, label='L250N2040')

boxes =[]
boxes.append(box_L150N2040)
boxes.append(box_L250N2040)

leg2=plt.gca().legend(handles=boxes,fontsize=12, loc='upper right',ncol=1,frameon=False)
plt.gca().add_artist(leg2)

plt.show()