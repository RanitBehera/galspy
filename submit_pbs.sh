#!/bin/bash
#PBS -N "MAB"
#PBS -q "regular"
#PBS -l walltime=24:00:00
#PBS -l select=1:ncpus=1
#PBS -o "/dev/null"
#PBS -e "/dev/null"
#PBS -j oe
#PBS -M "ranit.behera@iucaa.in"
#PBS -m abe


# ===== JOB =====
cd $PBS_O_WORKDIR
exec > stdout.txt 2>&1

source $HOME/anaconda3/etc/profile.d/conda.sh
echo "[ STARTED ] $(date)"
conda activate galspy

while [[ "$CONDA_DEFAULT_ENV" != "galspy" ]]; do
    echo "Waiting for Conda environment 'galspy' to be active..."
    sleep 1
done
echo "Environment found."

python $HOME/RANIT/Repo/galspy/scripts/SPM/stellar_spm_steps.py
echo "[ ENDED ] $(date)"

