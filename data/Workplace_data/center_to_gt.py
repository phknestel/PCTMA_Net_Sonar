import numpy as np
import h5py
import os
from tqdm import tqdm

def center_point_cloud(point_cloud, reference_centroid):
    return point_cloud - reference_centroid

def get_centroid(file_path, dataset_key):
    with h5py.File(file_path, 'r') as file:
        if dataset_key in file:
            point_cloud = file[dataset_key][:]
            return np.mean(point_cloud, axis=0)
    return None

def process_pair(gt_file_path, particle_file_path, dataset_key):
    reference_centroid = get_centroid(gt_file_path, dataset_key)
    if reference_centroid is not None:
        # Process ground truth file
        with h5py.File(gt_file_path, 'r+') as file:
            if dataset_key in file:
                point_cloud = file[dataset_key][:]
                centered_point_cloud = center_point_cloud(point_cloud, reference_centroid)
                del file[dataset_key]
                file.create_dataset(dataset_key, data=centered_point_cloud)

        # Process corresponding particle data file
        with h5py.File(particle_file_path, 'r+') as file:
            if dataset_key in file:
                point_cloud = file[dataset_key][:]
                centered_point_cloud = center_point_cloud(point_cloud, reference_centroid)
                del file[dataset_key]
                file.create_dataset(dataset_key, data=centered_point_cloud)

def process_directory(root_dir, dataset_key):
    target_dirs = ['gt', 'particle']
    all_files = [(os.path.join(root, file), os.path.join(root.replace('gt', 'particle'), file)) 
                 for root, dirs, files in os.walk(root_dir) 
                 for file in files if file.endswith(".h5") and 'gt' in root]

    with tqdm(total=len(all_files), desc="Processing files", unit="pair") as pbar:
        for gt_file_path, particle_file_path in all_files:
            if os.path.exists(particle_file_path):
                process_pair(gt_file_path, particle_file_path, dataset_key)
                pbar.update(1)

# Example usage
input_directory = "./"  # Specify the root directory
dataset_key = 'point_cloud'  # Change this to your dataset key if different
process_directory(input_directory, dataset_key)
