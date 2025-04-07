from mpi4py import MPI
import os

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
print(f"{os.environ['HOSTNAME']} > Hi {os.environ['USER']}. I got rank {rank}.")