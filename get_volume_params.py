import os
import csv
import SimpleITK as sitk
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from skimage.measure import marching_cubes, mesh_surface_area, euler_number

# Define relative base directory
base_dir = os.path.join("data", "test")
output_csv = os.path.join("output", "output_metrics.csv")

# Ensure the output directory exists
os.makedirs(os.path.dirname(output_csv), exist_ok=True)

# Define voxel spacing (update this if actual spacing is known)
spacing = (1.0, 1.0, 1.0)

# Define label name mapping
label_names = {
    0: "background",
    1: "whitematter",
    2: "grey matter",
    3: "hippocampus",
    4: "amygdala",
    5: "thalamus",
}

# Functions to calculate metrics
def compute_euler_characteristic(label_mask):
    return euler_number(label_mask)

def compute_surface_area_to_volume_ratio(label_mask, spacing):
    voxel_volume = np.prod(spacing)
    volume = np.sum(label_mask) * voxel_volume

    verts, faces, _, _ = marching_cubes(label_mask, level=0.5, spacing=spacing)
    surface_area = mesh_surface_area(verts, faces)

    return surface_area / volume, surface_area, volume

def compute_sphericity(label_mask, spacing):
    sa_to_vol_ratio, surface_area, volume = compute_surface_area_to_volume_ratio(label_mask, spacing)
    return (np.pi**(1/3) * (6 * volume)**(2/3)) / surface_area, surface_area, volume

def create_boxplots(csv_file):
    """
    Creates separate boxplots for each metric across all labels.

    Parameters:
        csv_file (str): Path to the CSV file containing the metrics.
    """
    # Load the CSV file into a DataFrame
    df = pd.read_csv(csv_file)

    # Convert numerical columns to floats (ensure proper plotting)
    numeric_cols = ["Euler Characteristic", "Surface Area", "Volume", "SA:V Ratio", "Sphericity"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Filter out background label if not needed
    df = df[df["Label"] != "background"]

    # Set up the plotting style
    sns.set(style="whitegrid")

    # Define font sizes
    title_fontsize = 16
    label_fontsize = 16
    tick_fontsize = 16

    # Create a separate figure for each metric
    for metric in numeric_cols:
        plt.figure(figsize=(10, 6))  # Create a new figure for each plot with a larger size
        ax = sns.boxplot(x="Label", y=metric, data=df, linewidth=2.5)  # Increase line width

        # Set title and labels with specified font sizes
        ax.set_title(f"{metric} by Label", fontsize=title_fontsize)
        ax.set_xlabel("Label", fontsize=label_fontsize)
        ax.set_ylabel(metric, fontsize=label_fontsize)

        # Adjust tick parameters for both major and minor ticks
        ax.tick_params(axis='both', which='major', labelsize=tick_fontsize, width=2)
        ax.tick_params(axis='both', which='minor', labelsize=tick_fontsize, width=1.5)

        plt.tight_layout()
        plt.show()


# Prepare CSV file
with open(output_csv, mode="w", newline="") as csv_file:
    fieldnames = ["Filename", "Label", "Euler Characteristic", "Surface Area", "Volume", "SA:V Ratio", "Sphericity"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    for subdir, _, files in os.walk(base_dir):
        for file in files:
            if file == "labels_native.nii.gz" and "resampled" not in subdir:
                volume_path = os.path.join(subdir, file)
                filename = os.path.relpath(volume_path, base_dir)

                try:
                    image = sitk.ReadImage(volume_path)
                    image_array = sitk.GetArrayFromImage(image)
                except Exception as e:
                    print(f"Error loading file: {e}")
                    continue

                unique_labels = np.unique(image_array)
                for label_id in unique_labels:
                    if label_id not in label_names:
                        continue

                    label_mask = (image_array == label_id).astype(np.uint8)
                    euler_num = compute_euler_characteristic(label_mask)
                    sa_to_vol_ratio, surface_area, volume = compute_surface_area_to_volume_ratio(label_mask, spacing)
                    sphericity, _, _ = compute_sphericity(label_mask, spacing)

                    writer.writerow({
                        "Filename": filename,
                        "Label": label_names[label_id],
                        "Euler Characteristic": euler_num,
                        "Surface Area": f"{surface_area:.2f}",
                        "Volume": f"{volume:.2f}",
                        "SA:V Ratio": f"{sa_to_vol_ratio:.4f}",
                        "Sphericity": f"{sphericity:.4f}",
                    })

# Generate the boxplots
create_boxplots(output_csv)
