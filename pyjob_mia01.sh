#!/bin/bash
#SBATCH --job-name="pipeline_mia"
#SBATCH --output=test_pipeline.txt
##SBATCH --partition=cpu
#SBATCH --time=2:00:00  # Request runtime of 1 hour
#SBATCH --mem=48G  # Request memory
#SBATCH --cpus-per-task=4  # Requested number of CPUs

# Activate your conda environment
source activate mia

# Enter file to run and enter some print to ensure it ran appropriately
python pipeline.py
