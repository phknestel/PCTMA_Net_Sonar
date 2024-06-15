import os
import numpy as np
import h5py
from scipy.spatial.distance import cdist

# Function to load a point cloud from an HDF5 file
def load_point_cloud(file_path):
    with h5py.File(file_path, 'r') as f:
        return np.array(f['point_cloud'])

# Function to compute Chamfer distance between two point clouds
def chamfer_distance(pcd1, pcd2):
    dist1 = cdist(pcd1, pcd2, 'euclidean')
    dist2 = cdist(pcd2, pcd1, 'euclidean')
    chamfer_dist1 = np.mean(np.min(dist1, axis=1))
    chamfer_dist2 = np.mean(np.min(dist2, axis=1))
    return chamfer_dist1 + chamfer_dist2

def main():
    directory = './'

    # Set the filenames directly
    filenames = [
        '114_denoise.h5',
        '114_denoise_gt.h5',
        '114_noise.h5',
        '114_noise_gt.h5'
    ]

    # Load the point clouds
    pcd1 = load_point_cloud(os.path.join(directory, filenames[0]))
    gt1 = load_point_cloud(os.path.join(directory, filenames[1]))
    pcd2 = load_point_cloud(os.path.join(directory, filenames[2]))
    gt2 = load_point_cloud(os.path.join(directory, filenames[3]))

    # Compute Chamfer distances
    chamfer_dist1 = chamfer_distance(pcd1, gt1)
    chamfer_dist2 = chamfer_distance(pcd2, gt2)

    # Multiply Chamfer distances by 10^4
    chamfer_dist1 *= 10**4
    chamfer_dist2 *= 10**4

    # Compute percentage change
    percentage_change = ((chamfer_dist2 - chamfer_dist1) / chamfer_dist2) * 100

    # Print results
    print(f"Chamfer distance for first pair (denoise): {chamfer_dist1}")
    print(f"Chamfer distance for second pair (noise): {chamfer_dist2}")
    print(f"Percentage change from noise to denoise: {percentage_change:.2f}%")

if __name__ == "__main__":
    main()
