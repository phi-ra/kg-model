#!/bin/bash
#SBATCH --mem=32G
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --time=24:0:0    
#SBATCH --mail-type=ALL
#SBATCH --gres=gpu:v100l:1

cd $project/kg_model
module purge
module load python/3.10 
source ~/env_hpc_tuner/bin/activate

python tuner.py