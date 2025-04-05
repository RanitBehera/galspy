#!/bin/bash
#PBS -N "CW"
#PBS -q "debug"
#PBS -l walltime=1:00:00
#PBS -l select=1:ncpus=4
#PBS -o "/dev/null"
#PBS -e "/dev/null"
#PBS -j oe
##PBS -M "ranit.behera@iucaa.in"
##PBS -m abe


# ===== JOB =====
cd $PBS_O_WORKDIR
SUFFIX=solar
exec > $PBS_O_WORKDIR/log/stdout_$SUFFIX.txt 2>&1

source $HOME/anaconda3/etc/profile.d/conda.sh
echo "[ STARTED ] $(date)"
conda activate galspy

while [[ "$CONDA_DEFAULT_ENV" != "galspy" ]]; do
    echo "Waiting for Conda environment 'galspy' to be active..."
    sleep 1
done
echo "Environment found."

python $HOME/RANIT/Repo/galspy/scripts_2/galaxy_statistics/gen_table_2.py
echo "[ ENDED ] $(date)"


