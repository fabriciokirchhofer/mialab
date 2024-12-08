import SimpleITK as sitk
import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import regionprops, label, perimeter
import skimage
import skimage.measure
# Load the NIfTI file
file_path = r"C:\GitRepos\MIALAB\mialab\data\test\117122\labels_native.nii.gz"

try:
    # Load the image using SimpleITK
    image = sitk.ReadImage(file_path)
    image_array = sitk.GetArrayFromImage(image)

    print("File loaded successfully!")
    print(f"Image shape: {image_array.shape}")
except Exception as e:
    print(f"Error loading file: {e}")
    exit()

label_0_mask = (image_array == 0).astype(np.uint8)
label_1_mask = (image_array == 1).astype(np.uint8)
label_2_mask = (image_array == 2).astype(np.uint8)
label_3_mask = (image_array == 3).astype(np.uint8)
label_4_mask = (image_array == 4).astype(np.uint8)
label_5_mask = (image_array == 5).astype(np.uint8)

labeled_image_2 = label(label_2_mask)
properties = regionprops(labeled_image_2)
for region in properties:
    # Basic properties
    region.
    area = region.area
    #perimeter = region.perimeter
    bbox = region.bbox
    #eccentricity = region.eccentricity

    print(f"Label 2 - Area: {area}")
    print(f"Label 2 - Bounding Box: {bbox}")







# Loop through each slice
def complexity(label_mask):
    slices_with_perimeter = 0
    total_perimeter = 0.0
    for i in range(label_mask.shape[0]):  # Iterate over slices along the Z-axis
        slice_mask = label_mask[i, :, :]  # Extract the 2D slice
        slice_perimeter = perimeter(slice_mask, neighborhood=4)  # Compute perimeter for the slice
        if slice_perimeter > 1:
            slices_with_perimeter += 1       
        total_perimeter += slice_perimeter  # Accumulate the perimeter
    # Calculate the area of the binary mask
    total_area = np.sum(label_2_mask)
    print(total_area)

    # Compute complexity for the 3D object
    avg_perimeter = total_perimeter / slices_with_perimeter
    complexity = (avg_perimeter ** 2) / (4 * np.pi * total_area)
    # Output results
    print(f"Total Area: {total_area}")
    print(f"Total Perimeter: {total_perimeter}")
    print(f"Complexity: {complexity}")

complexity(label_5_mask)