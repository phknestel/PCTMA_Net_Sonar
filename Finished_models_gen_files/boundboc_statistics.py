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

def compute_statistics(gt_files, completed_files):
    gt_point_counts = []
    reconstructed_point_counts = []
    gt_bounding_boxes = []
    reconstructed_bounding_boxes = []

    for gt_file, completed_file in zip(gt_files, completed_files):
        # Load point clouds
        gt_cloud = o3d.io.read_point_cloud(gt_file)
        completed_cloud = o3d.io.read_point_cloud(completed_file)

        # Get point counts
        gt_point_count = len(np.asarray(gt_cloud.points))
        completed_point_count = len(np.asarray(completed_cloud.points))

        # Get bounding box dimensions
        gt_bbox = gt_cloud.get_axis_aligned_bounding_box()
        completed_bbox = completed_cloud.get_axis_aligned_bounding_box()
        gt_bbox_dims = gt_bbox.get_extent()
        completed_bbox_dims = completed_bbox.get_extent()

        # Store the point counts and bounding boxes
        gt_point_counts.append(gt_point_count)
        reconstructed_point_counts.append(completed_point_count)
        gt_bounding_boxes.append(gt_bbox_dims)
        reconstructed_bounding_boxes.append(completed_bbox_dims)
    
    # Calculate point count statistics
    avg_gt_points = np.mean(gt_point_counts)
    min_gt_points = np.min(gt_point_counts)
    max_gt_points = np.max(gt_point_counts)
    avg_reconstructed_points = np.mean(reconstructed_point_counts)
    min_reconstructed_points = np.min(reconstructed_point_counts)
    max_reconstructed_points = np.max(reconstructed_point_counts)

    # Calculate bounding box statistics
    gt_bounding_boxes = np.array(gt_bounding_boxes)
    reconstructed_bounding_boxes = np.array(reconstructed_bounding_boxes)
    avg_gt_bbox = np.mean(gt_bounding_boxes, axis=0)
    min_gt_bbox = np.min(gt_bounding_boxes, axis=0)
    max_gt_bbox = np.max(gt_bounding_boxes, axis=0)
    avg_reconstructed_bbox = np.mean(reconstructed_bounding_boxes, axis=0)
    min_reconstructed_bbox = np.min(reconstructed_bounding_boxes, axis=0)
    max_reconstructed_bbox = np.max(reconstructed_bounding_boxes, axis=0)

    return (avg_gt_points, min_gt_points, max_gt_points, avg_reconstructed_points, min_reconstructed_points, max_reconstructed_points, 
            avg_gt_bbox, min_gt_bbox, max_gt_bbox, avg_reconstructed_bbox, min_reconstructed_bbox, max_reconstructed_bbox)

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
    stats = compute_statistics(gt_files, completed_files)
    
    # Store the results
    results.append({
        "Dataset": dataset_dir,
        "Avg_GT_Point_Count": stats[0],
        "Min_GT_Point_Count": stats[1],
        "Max_GT_Point_Count": stats[2],
        "Avg_Reconstructed_Point_Count": stats[3],
        "Min_Reconstructed_Point_Count": stats[4],
        "Max_Reconstructed_Point_Count": stats[5],
        "Avg_GT_BBox_X": stats[6][0],
        "Avg_GT_BBox_Y": stats[6][1],
        "Avg_GT_BBox_Z": stats[6][2],
        "Min_GT_BBox_X": stats[7][0],
        "Min_GT_BBox_Y": stats[7][1],
        "Min_GT_BBox_Z": stats[7][2],
        "Max_GT_BBox_X": stats[8][0],
        "Max_GT_BBox_Y": stats[8][1],
        "Max_GT_BBox_Z": stats[8][2],
        "Avg_Reconstructed_BBox_X": stats[9][0],
        "Avg_Reconstructed_BBox_Y": stats[9][1],
        "Avg_Reconstructed_BBox_Z": stats[9][2],
        "Min_Reconstructed_BBox_X": stats[10][0],
        "Min_Reconstructed_BBox_Y": stats[10][1],
        "Min_Reconstructed_BBox_Z": stats[10][2],
        "Max_Reconstructed_BBox_X": stats[11][0],
        "Max_Reconstructed_BBox_Y": stats[11][1],
        "Max_Reconstructed_BBox_Z": stats[11][2],
    })

# Convert results to a DataFrame
results_df = pd.DataFrame(results)

# Calculate overall statistics for point counts
overall_mean_gt_points = results_df["Avg_GT_Point_Count"].mean()
overall_min_gt_points = results_df["Min_GT_Point_Count"].min()
overall_max_gt_points = results_df["Max_GT_Point_Count"].max()
overall_mean_reconstructed_points = results_df["Avg_Reconstructed_Point_Count"].mean()
overall_min_reconstructed_points = results_df["Min_Reconstructed_Point_Count"].min()
overall_max_reconstructed_points = results_df["Max_Reconstructed_Point_Count"].max()

# Calculate overall statistics for bounding boxes
overall_mean_gt_bbox = results_df[["Avg_GT_BBox_X", "Avg_GT_BBox_Y", "Avg_GT_BBox_Z"]].mean().values
overall_min_gt_bbox = results_df[["Min_GT_BBox_X", "Min_GT_BBox_Y", "Min_GT_BBox_Z"]].min().values
overall_max_gt_bbox = results_df[["Max_GT_BBox_X", "Max_GT_BBox_Y", "Max_GT_BBox_Z"]].max().values
overall_mean_reconstructed_bbox = results_df[["Avg_Reconstructed_BBox_X", "Avg_Reconstructed_BBox_Y", "Avg_Reconstructed_BBox_Z"]].mean().values
overall_min_reconstructed_bbox = results_df[["Min_Reconstructed_BBox_X", "Min_Reconstructed_BBox_Y", "Min_Reconstructed_BBox_Z"]].min().values
overall_max_reconstructed_bbox = results_df[["Max_Reconstructed_BBox_X", "Max_Reconstructed_BBox_Y", "Max_Reconstructed_BBox_Z"]].max().values

# Create DataFrame for overall statistics
overall_stats = {
    "Dataset": "Overall",
    "Avg_GT_Point_Count": overall_mean_gt_points,
    "Min_GT_Point_Count": overall_min_gt_points,
    "Max_GT_Point_Count": overall_max_gt_points,
    "Avg_Reconstructed_Point_Count": overall_mean_reconstructed_points,
    "Min_Reconstructed_Point_Count": overall_min_reconstructed_points,
    "Max_Reconstructed_Point_Count": overall_max_reconstructed_points,
    "Avg_GT_BBox_X": overall_mean_gt_bbox[0],
    "Avg_GT_BBox_Y": overall_mean_gt_bbox[1],
    "Avg_GT_BBox_Z": overall_mean_gt_bbox[2],
    "Min_GT_BBox_X": overall_min_gt_bbox[0],
    "Min_GT_BBox_Y": overall_min_gt_bbox[1],
    "Min_GT_BBox_Z": overall_min_gt_bbox[2],
    "Max_GT_BBox_X": overall_max_gt_bbox[0],
    "Max_GT_BBox_Y": overall_max_gt_bbox[1],
    "Max_GT_BBox_Z": overall_max_gt_bbox[2],
    "Avg_Reconstructed_BBox_X": overall_mean_reconstructed_bbox[0],
    "Avg_Reconstructed_BBox_Y": overall_mean_reconstructed_bbox[1],
    "Avg_Reconstructed_BBox_Z": overall_mean_reconstructed_bbox[2],
    "Min_Reconstructed_BBox_X": overall_min_reconstructed_bbox[0],
    "Min_Reconstructed_BBox_Y": overall_min_reconstructed_bbox[1],
    "Min_Reconstructed_BBox_Z": overall_min_reconstructed_bbox[2],
    "Max_Reconstructed_BBox_X": overall_max_reconstructed_bbox[0],
    "Max_Reconstructed_BBox_Y": overall_max_reconstructed_bbox[1],
    "Max_Reconstructed_BBox_Z": overall_max_reconstructed_bbox[2]
}

overall_stats_df = pd.DataFrame([overall_stats])

# Concatenate results DataFrame with overall statistics DataFrame
results_df = pd.concat([results_df, overall_stats_df], ignore_index=True)

# Save the results to a CSV file
results_filename = "boundbox_statistics.csv"
results_df.to_csv(os.path.join(csv_results_dir, results_filename), index=False)

print(f"Completed. Point count and bounding box statistics are saved in the CSV file: {results_filename}.")
