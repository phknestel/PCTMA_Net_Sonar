import numpy as np
import h5py
import os

def center_point_cloud(point_cloud):
    centroid = np.mean(point_cloud, axis=0)
    return point_cloud - centroid

def process_file(file_path, dataset_key):
    with h5py.File(file_path, 'r+') as file:
        if dataset_key in file:
            point_cloud = file[dataset_key][:]
            centered_point_cloud = center_point_cloud(point_cloud)
            del file[dataset_key]
            file.create_dataset(dataset_key, data=centered_point_cloud)
            print(f"Processed {os.path.basename(file_path)}")

def process_directory(directory, dataset_key):
    for filename in os.listdir(directory):
        if filename.endswith(".h5"):
            file_path = os.path.join(directory, filename)
            process_file(file_path, dataset_key)

# Replace with your directory path and dataset key
your_directory = './'
dataset_key = 'point_cloud'  # Change this to your dataset key if different
process_directory(your_directory, dataset_key)
