#!/bin/bash
# Job name:
#SBATCH --job-name=test
# Account:
#SBATCH --account=account_name
# Partition:
#SBATCH --partition=gpu
# Number of GPUs per node:
#SBATCH --gres=gpu:1
# Number of nodes:
#SBATCH --nodes=1
# Number of tasks (one for each GPU desired for use case) (example):
#SBATCH --ntasks=1
# Processors per task:
# Always at least twice the number of GPUs (gpu2 and GTX2080TI in gpu2)
# Four times the number for TITAN and V100 in gpu3 and A5000 in gpu4
# Eight times the number for A40 in gpu3
#SBATCH --cpus-per-task=2
# Wall clock limit:
#SBATCH --time=00:10:00
#SBATCH --error=janus_test_%J.err
#SBATCH --output=janus_test_%J.out
#SBATCH -v

cd /home/AnirbanMondal_grp/23110077/Janus/tests
source /home/AnirbanMondal_grp/23110077/myenv/bin/activate
python3 /home/AnirbanMondal_grp/23110077/Janus/tests/example.py > jan.out

