import os
import numpy as np
import pandas as pd
import open3d as o3d
from scipy.spatial import cKDTree as KDTree

# Parameters
#output_dir = "alldataset_noPretrain_noHyper_noDenoise_delInput"
output_dir = "alldataset_Pretrain_noHyper_Denoise_delInput"
csv_results_dir = "csv_density_resultsx100/"
results = []

def compute_median_distance_metric(points, k=100):
    # Build a KD-tree for the points
    tree = KDTree(points)
    
    # Query the tree for the k nearest neighbors of each point (excluding itself)
    distances, _ = tree.query(points, k=k+1)
    
    # The first column returns zero distance (point to itself), so use the remaining columns
    median_distances = np.median(distances[:, 1:], axis=1)
    
    # Using median distance between points as a proxy for density
    return np.median(median_distances)

# Ensure the CSV results directory exists
os.makedirs(csv_results_dir, exist_ok=True)

for base_name in os.listdir(output_dir):
    if base_name.endswith("_gt.ply"):
        gt_file = os.path.join(output_dir, base_name)
        completed_file = os.path.join(output_dir, f"{base_name.split('_gt')[0]}_pc_recon_denoised.ply")

        # Print statement indicating which files are being compared
        print(f"Comparing GT file: {gt_file} with completed file: {completed_file}")

        # Load point clouds
        gt_cloud = o3d.io.read_point_cloud(gt_file)
        completed_cloud = o3d.io.read_point_cloud(completed_file)

        # Convert Open3D PointClouds to numpy arrays
        gt_points = np.asarray(gt_cloud.points)
        completed_points = np.asarray(completed_cloud.points)

        # Compute Median Distance Metrics
        gt_median_distance_metric = compute_median_distance_metric(gt_points)
        completed_median_distance_metric = compute_median_distance_metric(completed_points)
        
        # Store the results
        results.append({
            "base_name": base_name,
            "GT_Median_Distance_Metric": gt_median_distance_metric,
            "Completed_Median_Distance_Metric": completed_median_distance_metric
        })

# Convert results to a DataFrame and calculate medians
df = pd.DataFrame(results)
median_gt_median_distance = df["GT_Median_Distance_Metric"].mean()
median_completed_median_distance = df["Completed_Median_Distance_Metric"].mean()

# Append medians to the DataFrame using concat
medians_df = pd.DataFrame([{
    "base_name": "median_distance_metric",
    "GT_Median_Distance_Metric": median_gt_median_distance,
    "Completed_Median_Distance_Metric": median_completed_median_distance
}])
df = pd.concat([df, medians_df], ignore_index=True)

# Save the DataFrame with median distance metrics to a CSV file
results_filename = f"point_cloud_median_distance_metrics_results_{output_dir}.csv"
df.to_csv(os.path.join(csv_results_dir, results_filename), index=False)

print(f"Completed. Median distance metric results, including the overall medians, are saved in the CSV file: {results_filename}.")
