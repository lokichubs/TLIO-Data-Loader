import os

# Define the paths to the folders
gt_folder = 'GT_11_8'
imu_folder = 'IMU_11_8'

# Loop through the experiment folders in the IMU folder
for exp_folder in os.listdir(imu_folder):
    if exp_folder.startswith('Train_Data_') and exp_folder.endswith('_IMU'):
        exp_folder_path = os.path.join(imu_folder, exp_folder)
        
        # Loop through the CSV files in the experiment folder
        for file in os.listdir(exp_folder_path):
            if file.endswith('.csv'):
                file_path = os.path.join(exp_folder_path, file)
                print
                # Check which type of CSV file it is and renames it
                if 'WTRight_foot' in file:
                    new_name = 'right_rear.csv'
                elif 'WTDRS' in file:
                    new_name = 'left_rear.csv'
                elif 'WTLeft_foot' in file:
                    new_name = 'front.csv'
                else:
                    new_name = None
                    
                
                # Rename the file
                if new_name == None:
                    print(f"Files have already been renamed (or) check IMU naming convention")
                    break
                else:
                    os.rename(file_path, os.path.join(exp_folder_path, new_name))
    if new_name == None:
        break