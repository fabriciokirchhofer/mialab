import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import sys


# Fabricio's version modified to call it as function in pipeline.py
def generate_plots(results_dir, results_folder):
    # Construct the file path for results.csv
    file_path = os.path.join(results_dir, 'results.csv')
    
    # Load the CSV file using a semicolon as the delimiter
    print("Trying to load file:", file_path)  # Debugging line
    data = pd.read_csv(file_path, delimiter=';')
    
    # Filter out labels for plotting
    labels = ["WhiteMatter", "GreyMatter", "Hippocampus", "Amygdala", "Thalamus"]
    
    # Identify metric columns (excluding 'SUBJECT' and 'LABEL')
    metrics = [col for col in data.columns if col not in ['SUBJECT', 'LABEL']]
    
    # Create a separate plot for each metric
    for metric in metrics:
        # Create a dictionary to store metric values by label
        metric_data = {label: data[data['LABEL'] == label][metric].tolist() for label in labels}
        
        # Plot the metric values per label in a boxplot
        plt.figure(figsize=(10, 6))
        plt.boxplot(metric_data.values(), labels=metric_data.keys())
        plt.xlabel('Label')
        plt.ylabel(metric)
        plt.title(f'{metric} per Label')
        plt.grid(True)
        
        plot_file = os.path.join(results_dir, f"{metric}_per_label.png")
        plt.savefig(plot_file)
    
    print(f"Plots saved in {results_dir}")

# Original to Fabios version
def main(sub_directory):
    # Construct the file path for results.csv
    file_path = os.path.join(directory, 'results.csv')
    
    # Load the CSV file using a semicolon as the delimiter
    print("Trying to load file:", file_path)  # Debugging line
    data = pd.read_csv(file_path, delimiter=';')
    
    # Filter out labels for plotting
    labels = ["WhiteMatter", "GreyMatter", "Hippocampus", "Amygdala", "Thalamus"]
    
    # Identify metric columns (excluding 'SUBJECT' and 'LABEL')
    metrics = [col for col in data.columns if col not in ['SUBJECT', 'LABEL']]
    
    # Create a separate plot for each metric
    for metric in metrics:
        # Create a dictionary to store metric values by label
        metric_data = {label: data[data['LABEL'] == label][metric].tolist() for label in labels}
        
        # Plot the metric values per label in a boxplot
        plt.figure(figsize=(10, 6))
        plt.boxplot(metric_data.values(), labels=metric_data.keys())
        plt.xlabel('Label')
        plt.ylabel(metric)
        plt.title(f'{metric} per Label')
        plt.grid(True)
    
    # Display all figures at once
    plt.show()

if __name__ == '__main__':
    # Check if the directory argument is provided
    if len(sys.argv) < 2:
        print("Usage: python plot_results.py <directory>")
    else:
        directory = sys.argv[1]
        main(directory)