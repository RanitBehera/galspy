from mpi4py import MPI
import os
import socket

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
print(f"{socket.gethostname()} > Hi {os.environ['USER']}. I got rank {rank}.",flush=True)
