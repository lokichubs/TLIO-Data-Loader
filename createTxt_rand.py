import os
import random

# Change directory to "FORMATTED_DATA"
os.chdir("FORMATTED_DATA_V3_ALIGNED")

# Get the list of all folders in the directory
folders = [f for f in os.listdir() if os.path.isdir(f)]

# Write all folder names to "all_ids.txt"
with open("all_ids.txt", "w") as f:
    for folder in folders:
        f.write(folder + "\n")

# split the folders into three lists with 60% train and 20% test and 20% val
random.shuffle(folders)
train_size = int(0.6 * len(folders))
test_size = int(0.2 * len(folders))
val_size = int(0.2 * len(folders))
train_list = folders[:train_size]
test_list = folders[train_size:train_size + test_size]
val_list = folders[train_size + test_size:train_size + test_size + val_size]

# Write the lists to their respective files
with open("train_list.txt", "w") as f:
    for folder in train_list:
        f.write(folder + "\n")

with open("test_list.txt", "w") as f:
    for folder in test_list:
        f.write(folder + "\n")

with open("val_list.txt", "w") as f:
    for folder in val_list:
        f.write(folder + "\n")