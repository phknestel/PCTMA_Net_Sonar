'''
import os
import h5py

def check_and_delete_file(file_path):
    """
    Check if the HDF5 file contains a 1D array and delete it if so.

    :param file_path: Path to the HDF5 file.
    :return: True if the file was deleted, False otherwise.
    """
    try:
        with h5py.File(file_path, 'r') as file:
            # Assuming the dataset name inside the HDF5 file is 'point_cloud'
            dataset = file['point_cloud']
            if dataset.ndim == 1:  # Check if it's a 1D array
                return True
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
    return False

def process_directories(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.h5'):
                file_path = os.path.join(dirpath, filename)
                if check_and_delete_file(file_path):
                    os.remove(file_path)
                    print(f"Deleted 1D array file: {file_path}")

# Root directory of your dataset
root_dataset_dir = './'

process_directories(root_dataset_dir)
'''

import os
import h5py

def check_and_delete_file(file_path):
    """

    Check if the HDF5 file contains a 1D array and delete it if so.

    :param file_path: Path to the HDF5 file.
    :return: True if the file was deleted or needs deletion, False otherwise.
    """
    try:
        with h5py.File(file_path, 'r') as file:
            # Assuming the dataset name inside the HDF5 file is 'point_cloud'
            dataset = file['point_cloud']
            if dataset.ndim == 1:  # Check if it's a 1D array
                return True
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
    return False

def process_directories(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.h5'):
                file_path = os.path.join(dirpath, filename)
                if check_and_delete_file(file_path):
                    # Delete the file and its counterpart in the other subdirectory
                    os.remove(file_path)
                    print(f"Deleted 1D array file: {file_path}")

                    # Construct path of the counterpart file
                    counterpart_path = file_path.replace('particle', 'gt') if 'particle' in file_path else file_path.replace('gt', 'particle')
                    if os.path.exists(counterpart_path):
                        os.remove(counterpart_path)
                        print(f"Deleted counterpart file: {counterpart_path}")

# Root directory of your dataset
root_dataset_dir = './'

process_directories(root_dataset_dir)
