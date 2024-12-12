import os
import random
import re  # Import regular expressions module

# Change directory to "FORMATTED_DATA"
os.chdir("FORMATTED_DATA_V3_ALIGNED")

# Get the list of all folders in the directory
folders = [f for f in os.listdir() if os.path.isdir(f)]

# Separate folders based on their numeric values
greater_than_20 = []
less_than_equal_20 = []

for folder in folders:
    # Extract the numeric part from the folder name using regex
    match = re.search(r'(\d+)$', folder)  # This will match the last sequence of digits in the folder name
    if match:
        number = int(match.group(1))  # Convert the matched string to an integer
        if number >= 19:
            greater_than_20.append(folder)
        else:
            less_than_equal_20.append(folder)

# Shuffle both lists
random.shuffle(greater_than_20)
random.shuffle(less_than_equal_20)

# Split the folders with numbers 11 or greater
train_size_gt_20 = int(0.9 * len(greater_than_20))
val_size_gt_20 = int(0.05 * len(greater_than_20))
test_size_gt_20 = len(greater_than_20) - train_size_gt_20 - val_size_gt_20

train_list_gt_20 = greater_than_20[:train_size_gt_20]
val_list_gt_20 = greater_than_20[train_size_gt_20:train_size_gt_20 + val_size_gt_20]
test_list_gt_20 = greater_than_20[train_size_gt_20 + val_size_gt_20:]

# Split the folders with numbers less than or equal to 20
train_size_le_20 = int(0.6 * len(less_than_equal_20))
val_size_le_20 = int(0.2 * len(less_than_equal_20))
test_size_le_20 = len(less_than_equal_20) - train_size_le_20 - val_size_le_20

train_list_le_20 = less_than_equal_20[:train_size_le_20]
val_list_le_20 = less_than_equal_20[train_size_le_20:train_size_le_20 + val_size_le_20]
test_list_le_20 = less_than_equal_20[train_size_le_20 + val_size_le_20:]

# Combine the lists
train_list = train_list_gt_20 + train_list_le_20
val_list = val_list_gt_20 + val_list_le_20
test_list = test_list_gt_20 + test_list_le_20

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

# Write all folder names to "all_ids.txt"
with open("all_ids.txt", "w") as f:
    for folder in folders:
        f.write(folder + "\n")