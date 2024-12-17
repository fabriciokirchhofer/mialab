import os
import csv
import SimpleITK as sitk
import numpy as np
from skimage.measure import marching_cubes, mesh_surface_area, euler_number

# Define the test directory containing subdirectories with volumes
base_dir = r"C:\GitRepos\MedImgLab\mialab\mialab\data\test"
output_csv = r"C:\GitRepos\MedImgLab\mialab\output_metrics.csv"

# Define voxel spacing (update this if actual spacing is known)
spacing = (1.0, 1.0, 1.0)  # Default isotropic spacing

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
    """Compute the Euler characteristic of a 3D binary label mask."""
    return euler_number(label_mask)

def compute_surface_area_to_volume_ratio(label_mask, spacing):
    """Compute the Surface Area to Volume Ratio (SA:V) of a 3D binary label mask."""
    voxel_volume = np.prod(spacing)
    volume = np.sum(label_mask) * voxel_volume

    verts, faces, _, _ = marching_cubes(label_mask, level=0.5, spacing=spacing)
    surface_area = mesh_surface_area(verts, faces)

    sa_to_vol_ratio = surface_area / volume
    return sa_to_vol_ratio, surface_area, volume

def compute_sphericity(label_mask, spacing):
    """Compute the sphericity of a 3D binary label mask."""
    sa_to_vol_ratio, surface_area, volume = compute_surface_area_to_volume_ratio(label_mask, spacing)
    sphericity = (np.pi**(1/3) * (6 * volume)**(2/3)) / surface_area
    return sphericity, surface_area, volume

# Prepare the CSV file
with open(output_csv, mode="w", newline="") as csv_file:
    fieldnames = ["Filename", "Label", "Euler Characteristic", "Surface Area", "Volume", "SA:V Ratio", "Sphericity"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    # Process all volumes in the test directory
    for subdir, _, files in os.walk(base_dir):
        for file in files:
            if file == "labels_native.nii.gz" and "resampled" not in subdir:  # Ignore resampled files
                volume_path = os.path.join(subdir, file)
                filename = os.path.relpath(volume_path, base_dir)  # Relative file path

                print(f"Processing: {filename}")

                # Load the NIfTI file
                try:
                    image = sitk.ReadImage(volume_path)
                    image_array = sitk.GetArrayFromImage(image)
                    print(f"  File loaded successfully! Shape: {image_array.shape}")
                except Exception as e:
                    print(f"  Error loading file: {e}")
                    continue

                # Iterate over unique labels
                unique_labels = np.unique(image_array)
                for label_id in unique_labels:
                    if label_id not in label_names:  # Skip unknown labels
                        continue

                    # Create binary mask for the current label
                    label_mask = (image_array == label_id).astype(np.uint8)

                    # Compute metrics
                    euler_num = compute_euler_characteristic(label_mask)
                    sa_to_vol_ratio, surface_area, volume = compute_surface_area_to_volume_ratio(label_mask, spacing)
                    sphericity, _, _ = compute_sphericity(label_mask, spacing)

                    # Write results to the CSV file
                    writer.writerow({
                        "Filename": filename,
                        "Label": label_names[label_id],
                        "Euler Characteristic": euler_num,
                        "Surface Area": f"{surface_area:.2f}",
                        "Volume": f"{volume:.2f}",
                        "SA:V Ratio": f"{sa_to_vol_ratio:.4f}",
                        "Sphericity": f"{sphericity:.4f}",
                    })

                print()
