#!/bin/bash
#SBATCH --job-name="pipeline_mia"
#SBATCH --output=test_pipeline.txt
#SBATCH --time=0:30:00  # Request runtime of 1 hour
#SBATCH --mem=48G  # Request 32GB of system memory
#SBATCH --job-name=my_python_job      # Job name
#SBATCH --ntasks=1                    # Number of tasks (1 process)
#SBATCH --cpus-per-task=8            # CPUs per task (1 core)


# Activate your conda environment
module load Anaconda3
source activate mialabenv

# Enter file to run and enter some print to ensure it ran appropriately
python pipeline.py
