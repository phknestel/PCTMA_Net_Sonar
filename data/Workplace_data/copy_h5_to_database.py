''''
import os
import shutil

def copy_gt_files(input_dir, train_dir, val_dir):
    # Initialize counters for 'train' and 'val'
    train_counter, val_counter = 1, 1

    # Loop through the directories and files
    for root, dirs, files in os.walk(input_dir):
        # Check if the current directory is a "gt" directory
        if os.path.basename(root) == "gt":
            for file in files:
                if file.endswith(".h5"):
                    file_path = os.path.join(root, file)
                    
                    # Determine the destination directory based on the filename
                    if int(file.split('.')[0]) < 1294:
                        dest_dir = train_dir
                        new_file_name = f"{train_counter}.h5"
                        train_counter += 1
                    elif int(file.split('.')[0]) < 1456:
                        dest_dir = val_dir
                        new_file_name = f"{val_counter}.h5"
                        val_counter += 1
                    else:
                        continue  # Skip files not in 'train' or 'val' range

                    # Copy the file and print old and new names and directory
                    shutil.copy2(file_path, os.path.join(dest_dir, 'gt', '02691156', new_file_name))
                    print(f"Old Name: {file} | New Name: {new_file_name} | Directory: {root}")

# Example usage
input_directory = "./dataset_18-3"
train_directory = "./train"
val_directory = "./val"

copy_gt_files(input_directory, train_directory, val_directory)
'''

import os
import shutil

def copy_files_and_counterparts(input_dir, train_dir, val_dir, test_dir):
    # Initialize counters for 'train', 'val', and 'test'
    train_counter, val_counter, test_counter = 1, 1, 1

    # Loop through the directories and files
    for root, dirs, files in os.walk(input_dir):
        if os.path.basename(root) == "gt":
            for file in sorted(files):
                if file.endswith(".h5"):
                    file_path = os.path.join(root, file)

                    # Determine the destination directory and file number
                    file_number = int(file.split('.')[0])
                    if file_number < 1294:
                        dest_dir = train_dir
                        new_file_name = f"{train_counter}.h5"
                        train_counter += 1
                    elif file_number < 1456:
                        dest_dir = val_dir
                        new_file_name = f"{val_counter}.h5"
                        val_counter += 1
                    else:
                        # Process 'test' files
                        dest_dir = test_dir
                        new_file_name = f"{test_counter}.h5"
                        test_counter += 1

                        particle_file_path = file_path.replace("/gt/", "/particle/")
                        if os.path.exists(particle_file_path):
                            shutil.copy2(particle_file_path, os.path.join(dest_dir, 'partial', new_file_name))
                            print(f"Particle copied to test: {file} to {new_file_name}")
                        continue  # Skip further processing for 'test' files

                    # Copy the 'gt' file for 'train' and 'val'
                    shutil.copy2(file_path, os.path.join(dest_dir, 'gt', '02691156', new_file_name))
                    print(f"GT copied: {file} to {new_file_name}")

                    # Find and copy the corresponding 'particle' file
                    particle_file_path = file_path.replace("/gt/", "/particle/")
                    if os.path.exists(particle_file_path):
                        shutil.copy2(particle_file_path, os.path.join(dest_dir, 'partial', '02691156', new_file_name))
                        print(f"Particle copied: {file} to {new_file_name}")

# Example usage
input_directory = "./dataset_18-3_denoised"
train_directory = "./train"
val_directory = "./val"
test_directory = "./test"

copy_files_and_counterparts(input_directory, train_directory, val_directory, test_directory)
