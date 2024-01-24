import os
import h5py
from tqdm import tqdm

def is_h5_file_empty(h5_file_path):
    try:
        with h5py.File(h5_file_path, 'r') as h5f:
            for dataset in h5f.values():
                if dataset.size == 0:
                    return True
            return False
    except Exception as e:
        print(f"Error checking file {h5_file_path}: {e}")
        return False

def find_and_delete_empty_h5_files_with_counterparts(input_dir):
    target_dirs = ['gt', 'particle']
    all_files = [os.path.join(root, file) 
                 for root, dirs, files in os.walk(input_dir) 
                 for file in files if file.endswith(".h5") and os.path.basename(root) in target_dirs]

    with tqdm(total=len(all_files), desc="Checking files", unit="file") as pbar:
        for file_path in all_files:
            if is_h5_file_empty(file_path):
                print(f"Deleting empty file: {file_path}")
                os.remove(file_path)

                # Determine the counterpart directory (gt or particle)
                roll_blender_dir = os.path.dirname(os.path.dirname(file_path))
                counterpart_dir_name = "gt" if "particle" in os.path.basename(file_path) else "particle"
                counterpart_dir = os.path.join(roll_blender_dir, counterpart_dir_name)
                counterpart_file = os.path.join(counterpart_dir, os.path.basename(file_path))

                # Check if the counterpart file exists and delete
                if os.path.exists(counterpart_file):
                    print(f"Deleting counterpart file: {counterpart_file}")
                    os.remove(counterpart_file)

            pbar.update(1)

# Example usage
input_directory = "./"  # Specify the root directory
find_and_delete_empty_h5_files_with_counterparts(input_directory)
