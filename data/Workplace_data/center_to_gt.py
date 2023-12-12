import numpy as np
import h5py
import os

def center_point_cloud(point_cloud, reference_centroid):
    return point_cloud - reference_centroid

def get_centroid(file_path, dataset_key):
    with h5py.File(file_path, 'r') as file:
        if dataset_key in file:
            point_cloud = file[dataset_key][:]
            return np.mean(point_cloud, axis=0)
    return None

def process_pair(gt_file_path, generated_file_path, dataset_key):
    reference_centroid = get_centroid(gt_file_path, dataset_key)
    if reference_centroid is not None:
        # Process ground truth file
        with h5py.File(gt_file_path, 'r+') as file:
            if dataset_key in file:
                point_cloud = file[dataset_key][:]
                centered_point_cloud = center_point_cloud(point_cloud, reference_centroid)
                del file[dataset_key]
                file.create_dataset(dataset_key, data=centered_point_cloud)
                print(f"Processed ground truth {os.path.basename(gt_file_path)}")

        # Process corresponding generated data file
        with h5py.File(generated_file_path, 'r+') as file:
            if dataset_key in file:
                point_cloud = file[dataset_key][:]
                centered_point_cloud = center_point_cloud(point_cloud, reference_centroid)
                del file[dataset_key]
                file.create_dataset(dataset_key, data=centered_point_cloud)
                print(f"Processed generated data {os.path.basename(generated_file_path)}")

def process_directory(ground_truth_dir, generated_data_dir, dataset_key):
    for filename in os.listdir(ground_truth_dir):
        if filename.endswith(".h5"):
            gt_file_path = os.path.join(ground_truth_dir, filename)
            generated_file_path = os.path.join(generated_data_dir, filename)
            if os.path.exists(generated_file_path):
                process_pair(gt_file_path, generated_file_path, dataset_key)

# Replace with your directories path and dataset key
ground_truth_directory = './gt'
generated_data_directory = './partial'
dataset_key = 'point_cloud'  # Change this to your dataset key if different
process_directory(ground_truth_directory, generated_data_directory, dataset_key)
