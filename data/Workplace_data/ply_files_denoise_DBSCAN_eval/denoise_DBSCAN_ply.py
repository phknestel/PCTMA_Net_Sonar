import os
import numpy as np
import open3d as o3d
from sklearn.cluster import DBSCAN

def denoise_point_cloud_ply(file_path, eps=0.08, min_samples=50):
    """
    Apply DBSCAN clustering to denoise a point cloud in a PLY file.

    :param file_path: Path to the PLY file.
    :param eps: The maximum distance between two samples for them to be considered as in the same neighborhood.
    :param min_samples: The number of samples in a neighborhood for a point to be considered as a core point.
    :return: Denoised point cloud as an open3d.geometry.PointCloud object.
    """
    # Load point cloud from PLY file
    point_cloud_o3d = o3d.io.read_point_cloud(file_path)
    point_cloud_np = np.asarray(point_cloud_o3d.points)

    # Apply DBSCAN
    db = DBSCAN(eps=eps, min_samples=min_samples).fit(point_cloud_np)
    labels = db.labels_

    # Extract the points belonging to clusters (ignoring noise)
    denoised_point_cloud_np = point_cloud_np[labels != -1]

    # Create a new open3d point cloud object for the denoised cloud
    denoised_point_cloud_o3d = o3d.geometry.PointCloud()
    denoised_point_cloud_o3d.points = o3d.utility.Vector3dVector(denoised_point_cloud_np)

    return denoised_point_cloud_o3d

def process_directories(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if os.path.basename(dirpath) == 'particle':
            for filename in filenames:
                if filename.endswith('.ply'):
                    file_path = os.path.join(dirpath, filename)
                    print(f"Processing {file_path}")
                    denoised_cloud = denoise_point_cloud_ply(file_path)

                    # Save the denoised point cloud to a new PLY file
                    denoised_file_path = os.path.splitext(file_path)[0] + "_denoised.ply"
                    o3d.io.write_point_cloud(denoised_file_path, denoised_cloud)
                    print(f"Denoised point cloud saved to {denoised_file_path}")

# Root directory of your dataset
root_dataset_dir = './'

process_directories(root_dataset_dir)
