import os
import h5py
from tqdm import tqdm

def is_h5_file_to_be_deleted(h5_file_path):
    try:
        with h5py.File(h5_file_path, 'r') as h5f:
            # Check for empty dataset
            for dataset in h5f.values():
                if dataset.size == 0:
                    return True
            
            # Check if point_cloud dataset is a 1D array
            if 'point_cloud' in h5f and h5f['point_cloud'].ndim == 1:
                return True

        return False
    except Exception as e:
        print(f"Error checking file {h5_file_path}: {e}")
        return False

def find_and_delete_h5_files(input_dir):
    all_files = [os.path.join(root, file)
                 for root, dirs, files in os.walk(input_dir)
                 for file in files if file.endswith(".h5")]

    with tqdm(total=len(all_files), desc="Checking files", unit="file") as pbar:
        for file_path in all_files:
            if is_h5_file_to_be_deleted(file_path):
                print(f"Deleting file: {file_path}")
                os.remove(file_path)

                # Determine counterpart file
                counterpart_path = file_path.replace('particle', 'gt') if 'particle' in file_path else file_path.replace('gt', 'particle')
                if os.path.exists(counterpart_path):
                    print(f"Deleting counterpart file: {counterpart_path}")
                    os.remove(counterpart_path)

            pbar.update(1)

# Example usage
input_directory = "./"  # Specify the root directory
find_and_delete_h5_files(input_directory)
