import os
import h5py
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn import metrics

def denoise_point_cloud_h5(file_path, eps=0.06, min_samples=10):
    """
    Apply DBSCAN clustering to denoise a point cloud in an HDF5 file.

    :param file_path: Path to the HDF5 file.
    :param eps: The maximum distance between two samples for them to be considered as in the same neighborhood.
    :param min_samples: The number of samples in a neighborhood for a point to be considered as a core point.
    :return: Denoised point cloud as a numpy array.
    """
    # Load point cloud from HDF5 file
    with h5py.File(file_path, 'r') as file:
        # Assuming the dataset name inside the HDF5 file is 'point_cloud'
        # Modify this if your dataset has a different name
        point_cloud = file['point_cloud'][:]

    # Apply DBSCAN
    db = DBSCAN(eps=eps, min_samples=min_samples).fit(point_cloud)
    labels = db.labels_

    # Extract the points belonging to clusters (ignoring noise)
    denoised_point_cloud = point_cloud[labels != -1]

    return denoised_point_cloud

def process_directories(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if os.path.basename(dirpath) == 'particle':
            for filename in filenames:
                if filename.endswith('.h5'):
                    file_path = os.path.join(dirpath, filename)
                    print(f"Processing {file_path}")
                    denoised_cloud = denoise_point_cloud_h5(file_path)

                    # Overwrite the old file with the denoised point cloud
                    with h5py.File(file_path, 'w') as file:
                        # Assuming the dataset name inside the HDF5 file is 'point_cloud'
                        # Modify this if your dataset has a different name
                        file.create_dataset('point_cloud', data=denoised_cloud)
                    print(f"Denoised point cloud saved to {file_path}")

# Root directory of your dataset
root_dataset_dir = './'

process_directories(root_dataset_dir)
