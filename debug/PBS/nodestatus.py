import os, subprocess
import numpy


# ===== INPUT
job_id = 58130#int(input("Your JobID:"))

# ===== CAPTURE
# stdout_job:str=subprocess.run(['qstat','-f',str(job_id)],stdout=subprocess.PIPE).stdout.decode('utf-8')
stdout_node:str=subprocess.run(['pbsnodes','-aSj'],stdout=subprocess.PIPE).stdout.decode('utf-8')

# ===== CLASS
# est_cpus=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]





class NodeStatus:
    def __init__(self,line:str) -> None:
        clms  = line.split()
        self.Name       = clms[0]
        self.Number     = int(self.Name[-3:])
        self.State      = clms[1]
        # self.TotalMEM   = int(clms[5].split('/')[-1])
        # self.FreeMEM    = int(clms[5].split('/')[0])
        self.TotalCPU   = int(clms[6].split('/')[-1])
        self.FreeCPU    = int(clms[6].split('/')[0])

hpc_list:list[NodeStatus] = []
lines = stdout_node.split("\n")
lines = [" ".join(l.split()) for l in lines if l.startswith(("hpc"))]
for line in lines:hpc_list.append(NodeStatus(line))


# ===== ASNI
def ansi(n):return f"\033[{n}m"
RESET           = ansi(0)
DIM             = ansi(2)
FG_GREEN        = ansi(32)
FG_YELLOW       = ansi(33)
FG_MAGENTA      = ansi(35)
FG_RED          = ansi(31)


# ===== PRSENT
CELL_COUNT = 6
CELL_WIDTH = 20


def disp(name,acpu,wcpu):
    return f"{name}({wcpu}/{acpu})".ljust(CELL_WIDTH)

# Sort
hpc_num = [hpc.Number for hpc in hpc_list]
SORT = numpy.argsort(hpc_num)
hpc_list=numpy.array(hpc_list)
hpc_list = hpc_list[SORT]

for i,hpc in enumerate(hpc_list):
    if i//CELL_COUNT>0 and i%CELL_COUNT==0:print("")
    if i==80:print("\n-----")
    NAME  = hpc.Name
    STATE = hpc.State
    TCPU = hpc.TotalCPU
    FCPU = hpc.FreeCPU

    if STATE=="down,offline":
        print((FG_RED+disp(NAME,TCPU,FCPU)+RESET),end="")
    elif STATE=="free" and FCPU==TCPU:
        print((FG_GREEN+disp(NAME,TCPU,FCPU)+RESET),end="")
    elif STATE=="free" and FCPU>0:
        print((FG_YELLOW+disp(NAME,TCPU,FCPU)+RESET),end="")
    elif FCPU==0:
        print((FG_MAGENTA+disp(NAME,TCPU,FCPU)+RESET),end="") 



print("")
