import os
import numpy as np
import pandas as pd
import open3d as o3d
from scipy.spatial.distance import cdist

# Parameters
output_dir = "alldataset_Pretrain_noHyper_Denoise_delInput"
csv_results_dir = "csv_results/"
results = []

def compute_chamfer_distance(pcd1, pcd2):
    # Compute pairwise distances
    dist1 = cdist(pcd1, pcd2, 'euclidean')
    dist2 = cdist(pcd2, pcd1, 'euclidean')
    
    # Compute Chamfer distances
    chamfer_dist1 = np.mean(np.min(dist1, axis=1))
    chamfer_dist2 = np.mean(np.min(dist2, axis=1))
    
    # Return combined Chamfer distance multiplied by 10^4
    return (chamfer_dist1 + chamfer_dist2) * 10**3

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

        # Compute Chamfer Distance
        chamfer_dist = compute_chamfer_distance(gt_points, completed_points)
        
        # Store the results
        results.append({
            "base_name": base_name,
            "Chamfer_Distance": chamfer_dist
        })

# Convert results to a DataFrame and calculate the mean Chamfer distance
df = pd.DataFrame(results)
mean_chamfer_dist = df["Chamfer_Distance"].mean()

# Append mean to the DataFrame using concat
mean_df = pd.DataFrame([{
    "base_name": "mean_chamfer_distance",
    "Chamfer_Distance": mean_chamfer_dist
}])
df = pd.concat([df, mean_df], ignore_index=True)

# Save the DataFrame with Chamfer distances to a CSV file
results_filename = f"point_cloud_chamfer_distance_results_{output_dir}.csv"
df.to_csv(os.path.join(csv_results_dir, results_filename), index=False)

print(f"Completed. Chamfer distance results, including the mean, are saved in the CSV file: {results_filename}.")
