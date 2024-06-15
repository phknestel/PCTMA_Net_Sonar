import os
import numpy as np
import pandas as pd
import open3d as o3d

# Parameters
dataset_dirs = [
    "alldataset_NoPretrain_Hyper_Denoise_delInput",
    "alldataset_noPretrain_noHyper_noDenoise_delInput",
    "alldataset_Pretrain_Hyper_Denoise_delInput",
    "alldataset_Pretrain_noHyper_Denoise_delInput",
    "denoise_hyper_floor_delInput",
    "denoise_hyper_nofloor_delInput",
    "denoise_pretrain_hyper_floor_delInput",
    "denoise_pretrain_hyper_nofloor_delInput"
]
csv_results_dir = "csv_results/"
results = []

def compute_point_statistics(gt_files, completed_files):
    gt_point_counts = []
    reconstructed_point_counts = []

    for gt_file, completed_file in zip(gt_files, completed_files):
        # Load point clouds
        gt_cloud = o3d.io.read_point_cloud(gt_file)
        completed_cloud = o3d.io.read_point_cloud(completed_file)

        # Get point counts
        gt_point_count = len(np.asarray(gt_cloud.points))
        completed_point_count = len(np.asarray(completed_cloud.points))

        # Store the point counts
        gt_point_counts.append(gt_point_count)
        reconstructed_point_counts.append(completed_point_count)
    
    # Calculate statistics
    avg_gt_points = np.mean(gt_point_counts)
    min_gt_points = np.min(gt_point_counts)
    max_gt_points = np.max(gt_point_counts)
    
    avg_reconstructed_points = np.mean(reconstructed_point_counts)
    min_reconstructed_points = np.min(reconstructed_point_counts)
    max_reconstructed_points = np.max(reconstructed_point_counts)

    return avg_gt_points, min_gt_points, max_gt_points, avg_reconstructed_points, min_reconstructed_points, max_reconstructed_points

# Ensure the CSV results directory exists
os.makedirs(csv_results_dir, exist_ok=True)

# Process each dataset directory
for dataset_dir in dataset_dirs:
    gt_files = []
    completed_files = []

    for base_name in os.listdir(dataset_dir):
        if base_name.endswith("_gt.ply"):
            gt_file = os.path.join(dataset_dir, base_name)
            completed_file = os.path.join(dataset_dir, f"{base_name.split('_gt')[0]}_pc_recon_denoised.ply")
            
            if os.path.exists(completed_file):
                gt_files.append(gt_file)
                completed_files.append(completed_file)

    # Compute statistics for the current dataset
    avg_gt_points, min_gt_points, max_gt_points, avg_reconstructed_points, min_reconstructed_points, max_reconstructed_points = compute_point_statistics(gt_files, completed_files)
    
    # Store the results
    results.append({
        "Dataset": dataset_dir,
        "Avg_GT_Point_Count": avg_gt_points,
        "Min_GT_Point_Count": min_gt_points,
        "Max_GT_Point_Count": max_gt_points,
        "Avg_Reconstructed_Point_Count": avg_reconstructed_points,
        "Min_Reconstructed_Point_Count": min_reconstructed_points,
        "Max_Reconstructed_Point_Count": max_reconstructed_points
    })

# Convert results to a DataFrame
results_df = pd.DataFrame(results)

# Calculate overall statistics
overall_mean_gt_points = results_df["Avg_GT_Point_Count"].mean()
overall_min_gt_points = results_df["Min_GT_Point_Count"].min()
overall_max_gt_points = results_df["Max_GT_Point_Count"].max()

overall_mean_reconstructed_points = results_df["Avg_Reconstructed_Point_Count"].mean()
overall_min_reconstructed_points = results_df["Min_Reconstructed_Point_Count"].min()
overall_max_reconstructed_points = results_df["Max_Reconstructed_Point_Count"].max()

# Create DataFrame for overall statistics
overall_stats_df = pd.DataFrame([{
    "Dataset": "Overall",
    "Avg_GT_Point_Count": overall_mean_gt_points,
    "Min_GT_Point_Count": overall_min_gt_points,
    "Max_GT_Point_Count": overall_max_gt_points,
    "Avg_Reconstructed_Point_Count": overall_mean_reconstructed_points,
    "Min_Reconstructed_Point_Count": overall_min_reconstructed_points,
    "Max_Reconstructed_Point_Count": overall_max_reconstructed_points
}])

# Concatenate results DataFrame with overall statistics DataFrame
results_df = pd.concat([results_df, overall_stats_df], ignore_index=True)

# Save the results to a CSV file
results_filename = "point_cloud_point_count_statistics.csv"
results_df.to_csv(os.path.join(csv_results_dir, results_filename), index=False)

print(f"Completed. Point count statistics are saved in the CSV file: {results_filename}.")
