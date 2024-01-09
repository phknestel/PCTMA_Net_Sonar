import h5py
import numpy as np

# Open the H5 file
with h5py.File('1556.h5', 'r') as file:
    # Load the point cloud data
    point_clouds = file['point_cloud'][:] 

# Calculate the centroid (center) of each point cloud
centroids = np.mean(point_clouds, axis=1)

# Calculate the range (max - min) along each axis
ranges = np.ptp(point_clouds, axis=1)

print("Centroids:", centroids)
print("Ranges:", ranges)

# Print the length of centroids and ranges
print("Length of centroids:", len(centroids))
print("Length of ranges:", len(ranges))

# Calculate and print the mean of these arrays
mean_centroids = np.mean(centroids, axis=0)
mean_ranges = np.mean(ranges, axis=0)
print("Mean of centroids:", mean_centroids)
print("Mean of ranges:", mean_ranges)
