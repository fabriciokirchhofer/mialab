#!/bin/bash
#SBATCH --job-name="pipeline_mia"
#SBATCH --output=test_pipeline.txt
#SBATCH --partition=gpu
#SBATCH --gres=gpu:rtx3090:1  # Request one RTX 3090 GPU
#SBATCH --time=0:30:00  # Request runtime of 1 hour
#SBATCH --mem=32G  # Request 32GB of system memory
#SBATCH --cpus-per-task=2  # Request 2 CPUs

# Activate your conda environment
source activate mia

# Enter file to run and enter some print to ensure it ran appropriately
python pipeline.py
