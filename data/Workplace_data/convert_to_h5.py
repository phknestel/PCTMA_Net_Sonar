import os
import numpy as np
import h5py
from tqdm import tqdm

def convert_to_h5_and_replace_txt(input_dir):
    # Define target directories
    target_dirs = ['gt', 'particle']

    # Collect all .txt files in the specified target directories
    all_files = [os.path.join(root, file) 
                 for root, dirs, files in os.walk(input_dir) 
                 for file in files if file.endswith(".txt") and os.path.basename(root) in target_dirs]

    # Initialize progress bar
    with tqdm(total=len(all_files), desc="Converting files", unit="file") as pbar:
        for file_path in all_files:
            # Load data from the .txt file
            data = np.loadtxt(file_path)

            # Define the .h5 file path (same as .txt but with .h5 extension)
            h5_file_path = file_path.replace(".txt", ".h5")

            # Write data to the .h5 file
            with h5py.File(h5_file_path, 'w') as h5f:
                h5f.create_dataset('point_cloud', data=data)

            # Delete the original .txt file
            # os.remove(file_path)

            # Update progress bar
            pbar.update(1)

# Example usage
input_directory = "./"  # Specify the root directory
convert_to_h5_and_replace_txt(input_directory)
