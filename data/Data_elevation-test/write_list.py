import os

def create_list(data_dir, subfolder, list_file_path, prefix=""):
    data_partial_dir = os.path.join(data_dir, 'partial', subfolder)

    file_numbers = []

    if os.path.exists(data_partial_dir):
        for file in os.listdir(data_partial_dir):
            if file.endswith('.h5'):
                file_number = file.split('.')[0]
                file_numbers.append(int(file_number))  # Convert to int for numerical sorting

    file_numbers.sort()  # Sorts numerically

    with open(list_file_path, 'w') as f:
        for number in file_numbers:
            f.write(f"{prefix}{number}\n")  # Convert back to string for writing to file
        print(f"{list_file_path} created at {data_dir}")

# Example usage
test_directory = "./test"
train_directory = "./train"
val_directory = "./val"

create_list(test_directory, '', "./test.list")
create_list(train_directory, '02691156', "./train.list", "02691156/")
create_list(val_directory, '02691156', "./val.list", "02691156/")
