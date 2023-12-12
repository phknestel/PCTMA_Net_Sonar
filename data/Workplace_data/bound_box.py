import numpy as np
import h5py
import os

def calculate_scale_and_translation(gt_point_cloud, target_min, target_max):
    pc_min = np.min(gt_point_cloud, axis=0)
    pc_max = np.max(gt_point_cloud, axis=0)
    scale_factor = (target_max - target_min) / (pc_max - pc_min)
    translation = target_min - pc_min * scale_factor
    return scale_factor, translation

def normalize_point_cloud(point_cloud, scale_factor, translation):
    return point_cloud * scale_factor + translation

def process_file(file_path, scale_factor, translation, dataset_key):
    with h5py.File(file_path, 'r+') as file:
        if dataset_key in file:
            point_cloud = file[dataset_key][:]
            normalized_point_cloud = normalize_point_cloud(point_cloud, scale_factor, translation)
            del file[dataset_key]
            file.create_dataset(dataset_key, data=normalized_point_cloud)
            print(f"Normalized {file_path}")

def process_pair(gt_file_path, partial_file_path, target_min, target_max, dataset_key):
    # Read the ground truth file to calculate the scale and translation
    with h5py.File(gt_file_path, 'r') as gt_file:
        if dataset_key in gt_file:
            gt_point_cloud = gt_file[dataset_key][:]
            scale_factor, translation = calculate_scale_and_translation(gt_point_cloud, target_min, target_max)

    # Now, process the ground truth and partial files
    process_file(gt_file_path, scale_factor, translation, dataset_key)
    process_file(partial_file_path, scale_factor, translation, dataset_key)

# Define target bounding box range
target_min = np.array([-0.27, -0.23, -0.25])
target_max = np.array([0.27, 0.23, 0.25])

# Dataset key
dataset_key = 'point_cloud'

# Paths to the gt and partial directories
current_directory = os.getcwd()
gt_directory = os.path.join(current_directory, 'gt/02691156')
partial_directory = os.path.join(current_directory, 'partial/02691156')

# Process each pair of ground truth and partial files
for gt_file in os.listdir(gt_directory):
    if gt_file.endswith('.h5'):
        gt_file_path = os.path.join(gt_directory, gt_file)
        partial_file_path = os.path.join(partial_directory, gt_file)
        if os.path.exists(partial_file_path):
            process_pair(gt_file_path, partial_file_path, target_min, target_max, dataset_key)
        else:
            print(f"Partial file for {gt_file} not found.")
