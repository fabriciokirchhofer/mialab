#!/bin/bash
#SBATCH --job-name=pipeline_doe
#SBATCH --output=pipeline_doe_output.txt
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=48G
#SBATCH --time=24:00:00

source activate mialab  # Activate your Anaconda environment if necessary

python pipeline_doe.py 
