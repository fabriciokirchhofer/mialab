#!/bin/bash
#SBATCH --job-name="pipeline_mia"
#SBATCH --output=doe_run.txt
#SBATCH --time=0:30:00  # Request runtime of 1 hour
#SBATCH --mem=32G  # Request 32GB of system memory
#SBATCH --ntasks=1                    # Number of tasks (1 process)
#SBATCH --cpus-per-task=6            # CPUs per task (1 core)


# Activate your conda environment
source activate mialab

# Enter file to run and enter some print to ensure it ran appropriately
python pipeline.py