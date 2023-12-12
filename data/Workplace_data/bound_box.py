import numpy as np
import h5py
import os

def calculate_scale_and_translation(point_cloud, target_min, target_max):
    pc_min = np.min(point_cloud, axis=0)
    pc_max = np.max(point_cloud, axis=0)
    scale_factor = (target_max - target_min) / (pc_max - pc_min)
    translation = target_min - pc_min * scale_factor
    return scale_factor, translation

def normalize_point_cloud(point_cloud, scale_factor, translation):
    return point_cloud * scale_factor + translation

def process_file(file_path, scale_factor, translation):
    with h5py.File(file_path, 'r+') as file:
        if 'point_cloud' in file:
            point_cloud = file['point_cloud'][:]
            normalized_point_cloud = normalize_point_cloud(point_cloud, scale_factor, translation)
            del file['point_cloud']
            file.create_dataset('point_cloud', data=normalized_point_cloud)
            print(f"Normalized {file_path}")

def process_pair(gt_file_path, partial_file_path, target_min, target_max):
    # Read the ground truth file to calculate the scale and translation
    with h5py.File(gt_file_path, 'r') as gt_file:
        if 'point_cloud' in gt_file:
            gt_point_cloud = gt_file['point_cloud'][:]
            scale_factor, translation = calculate_scale_and_translation(gt_point_cloud, target_min, target_max)
    
    # Now, reopen the ground truth file for modification
    process_file(gt_file_path, scale_factor, translation)
    process_file(partial_file_path, scale_factor, translation)


# Define target bounding box range
target_min = np.array([-0.27, -0.23, -0.25])  # Adjust as necessary
target_max = np.array([0.27, 0.23, 0.25])     # Adjust as necessary

# Paths to the gt and partial directories
current_directory = os.getcwd()
gt_directory = os.path.join(current_directory, 'gt')
partial_directory = os.path.join(current_directory, 'partial')

# Process each pair of ground truth and partial files
for gt_file in os.listdir(gt_directory):
    if gt_file.endswith('.h5'):
        gt_file_path = os.path.join(gt_directory, gt_file)
        partial_file_path = os.path.join(partial_directory, gt_file)
        if os.path.exists(partial_file_path):
            process_pair(gt_file_path, partial_file_path, target_min, target_max)
        else:
            print(f"Partial file for {gt_file} not found.")

