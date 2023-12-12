import numpy as np
import h5py
import os
from plyfile import PlyData, PlyElement

def save_point_cloud_as_ply(points, filename):
    structured_points = np.array([(point[0], point[1], point[2]) for point in points],
                                 dtype=[('x', 'f4'), ('y', 'f4'), ('z', 'f4')])
    vertex = PlyElement.describe(structured_points, 'vertex')
    PlyData([vertex], text=True).write(filename)

def process_file(h5_file_path):
    with h5py.File(h5_file_path, 'r') as file:
        # Assuming 'point_cloud' is the key for your point clouds
        if 'point_cloud' in file:
            point_cloud = file['point_cloud'][:]  # This is now treated as a single point cloud

            # Replace the extension of the file name from .h5 to .ply
            ply_filename = h5_file_path.replace('.h5', '.ply')

            # Save the entire dataset as one PLY file
            save_point_cloud_as_ply(point_cloud, ply_filename)
            print(f"Saved point cloud to {ply_filename}")

def process_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.h5'):
            h5_file_path = os.path.join(directory, filename)
            process_file(h5_file_path)

# Replace with your directory path
your_directory = './'  # Current directory
process_directory(your_directory)
