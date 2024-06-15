import os
import numpy as np
import pandas as pd
import open3d as o3d
import ot

# Parameters
output_dir = "alldataset_Pretrain_noHyper_Denoise_delInput"
csv_results_dir = "csv_results/"
results = []

def compute_emd(source_points, target_points):
    # Normalize the point clouds
    source_points = (source_points - np.mean(source_points, axis=0)) / np.std(source_points, axis=0)
    target_points = (target_points - np.mean(target_points, axis=0)) / np.std(target_points, axis=0)
    
    # Compute the pairwise distance matrix
    M = ot.dist(source_points, target_points, metric='euclidean')
    
    # Uniform distribution over source and target points
    n = len(source_points)
    m = len(target_points)
    a = np.ones((n,)) / n
    b = np.ones((m,)) / m
    
    # Compute EMD
    emd_distance = ot.emd2(a, b, M)
    
    return emd_distance

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

        # Compute Earth Mover's Distance
        emd_distance = compute_emd(gt_points, completed_points)
        
        # Store the results
        results.append({
            "base_name": base_name,
            "EMD_Distance": emd_distance
        })

# Convert results to a DataFrame and calculate the mean EMD
df = pd.DataFrame(results)
mean_emd_distance = df["EMD_Distance"].mean()

# Append mean to the DataFrame using concat
mean_df = pd.DataFrame([{
    "base_name": "mean_emd_distance",
    "EMD_Distance": mean_emd_distance
}])
df = pd.concat([df, mean_df], ignore_index=True)

# Save the DataFrame with EMD distances to a CSV file
results_filename = f"point_cloud_emd_distance_results_{output_dir}.csv"
df.to_csv(os.path.join(csv_results_dir, results_filename), index=False)

print(f"Completed. EMD distance results, including the mean, are saved in the CSV file: {results_filename}.")
