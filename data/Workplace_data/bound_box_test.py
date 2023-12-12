import numpy as np
import h5py
import os

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

def process_directory(directory, scale_factor, translation, dataset_key):
    for filename in os.listdir(directory):
        if filename.endswith('.h5'):
            file_path = os.path.join(directory, filename)
            process_file(file_path, scale_factor, translation, dataset_key)

# Average scale factor and translation calculated from ground truth data
avg_scale_factor = np.array([-0.27, -0.23, -0.25])
avg_translation = np.array([0.27, 0.23, 0.25])

# Dataset key
dataset_key = 'point_cloud'

# Path to the test directory
test_directory = './'

# Process the test directory
process_directory(test_directory, avg_scale_factor, avg_translation, dataset_key)
