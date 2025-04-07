#!/bin/bash
#PBS -N "M4P"
#PBS -q "debug"
#PBS -l walltime=1:00:00
#PBS -l select=2:ncpus=32:mpiprocs=32
#PBS -l place=scatter
#PBS -o "/dev/null"
#PBS -e "/dev/null"
#PBS -j oe
##PBS -M "ranit.behera@iucaa.in"
##PBS -m abe


# ===== JOB =====
cd $PBS_O_WORKDIR
# 
PBS_OUTDIR=$PBS_O_WORKDIR/log/${PBS_JOBID}_${PBS_JOBNAME}
mkdir -p $PBS_OUTDIR
exec > $PBS_OUTDIR/stdout.txt 2>&1
# 
source $HOME/anaconda3/etc/profile.d/conda.sh
#
module load gcc/11.2.0
module load mpich-4.1.1
echo "[ STARTED ] $(date)">>$PBS_OUTDIR/pbs.log
#
conda activate galspy
while [[ "$CONDA_DEFAULT_ENV" != "galspy" ]]; do
    echo "Waiting for Conda environment 'galspy' to be active...">>$PBS_OUTDIR/pbs.log
    sleep 1
done
echo "Environment found.">>$PBS_OUTDIR/pbs.log
#=======================================================================================
# python /mnt/home/student/cranit/RANIT/Repo/galspy/debug/mpicheck/test1.py
/mnt/csoft/compilers/mpich-3.3.1/bin/mpiexec --hostfile $PBS_NODEFILE -n 64 python /mnt/home/student/cranit/RANIT/Repo/galspy/debug/mpicheck/test1.py
#=======================================================================================
echo "[ ENDED ] $(date)">>$PBS_OUTDIR/pbs.log


