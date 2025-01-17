import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import shutil
import os
import scipy

formatted_data_folder = 'FORMATTED_DATA'
imu_file = 'imu_samples_0.csv'
imu_json = 'calibration.json'
mocap_file = 'imu0_resampled.npy'
mocap_json = 'imu0_resampled_description.json'
interpolated_data_folder = 'FORMATTED_DATA_INTERPOLATED'

# Interpolation Parameters
target_frequency = 200  # in Hz
target_time_interval = 1 / target_frequency  # in seconds
target_time_interval_ns = target_time_interval * 1e9  # convert to nanoseconds

if os.path.exists(interpolated_data_folder) == False:
    shutil.copytree(formatted_data_folder, interpolated_data_folder)


for root, dirs, files in os.walk(formatted_data_folder):
    for dir in dirs:
        current_folder = os.path.join(root, dir)
        print(f"Processing folder: {current_folder}")

        # Construct file paths
        imu_file_path = os.path.join(current_folder, imu_file)

        # Read IMU data
        if os.path.exists(imu_file_path):
            imu_data = pd.read_csv(imu_file_path)
            print("IMU data loaded")
        
        imu_data_interpolated = pd.DataFrame(columns=imu_data.columns)
        num_samples = int(np.floor(imu_data.iloc[-1,0]/target_time_interval_ns))
        print(f"Number of samples interp: {num_samples}")
        print(f"Number of samples OG: {len(imu_data)}")
        start_time_ns = imu_data.iloc[0, 0]  # The first timestamp in the original data
        imu_data_interpolated.iloc[:, 0] = np.linspace(start_time_ns, start_time_ns + (num_samples) * target_time_interval_ns, num_samples+1)
        print("Final Time interpolated: ", imu_data_interpolated.iloc[-1, 0])
        print("Final Time OG: ", imu_data.iloc[-1, 0])
        print(f"Difference in time ={imu_data.iloc[-1, 0]-imu_data_interpolated.iloc[-1, 0]} ns")
        print(f"New time interval: {target_time_interval_ns} ns")


        interp2 = scipy.interpolate.interp1d(imu_data.iloc[:,0], imu_data.iloc[:,1])
        interp3 = scipy.interpolate.interp1d(imu_data.iloc[:,0], imu_data.iloc[:,2])
        interp4 = scipy.interpolate.interp1d(imu_data.iloc[:,0], imu_data.iloc[:,3])
        interp5 = scipy.interpolate.interp1d(imu_data.iloc[:,0], imu_data.iloc[:,4])
        interp6 = scipy.interpolate.interp1d(imu_data.iloc[:,0], imu_data.iloc[:,5])
        interp7 = scipy.interpolate.interp1d(imu_data.iloc[:,0], imu_data.iloc[:,6])
        interp8 = scipy.interpolate.interp1d(imu_data.iloc[:,0], imu_data.iloc[:,7])

        imu_data_interpolated.iloc[:, 1] = interp2(imu_data_interpolated.iloc[:, 0])  # Interpolate the second column
        imu_data_interpolated.iloc[:, 2] = interp3(imu_data_interpolated.iloc[:, 0])  # Interpolate the third column
        imu_data_interpolated.iloc[:, 3] = interp4(imu_data_interpolated.iloc[:, 0])  # Interpolate the fourth column
        imu_data_interpolated.iloc[:, 4] = interp5(imu_data_interpolated.iloc[:, 0])  # Interpolate the fifth column
        imu_data_interpolated.iloc[:, 5] = interp6(imu_data_interpolated.iloc[:, 0])  # Interpolate the sixth column
        imu_data_interpolated.iloc[:, 6] = interp7(imu_data_interpolated.iloc[:, 0])  # Interpolate the seventh column
        imu_data_interpolated.iloc[:, 7] = interp8(imu_data_interpolated.iloc[:, 0])  # Interpolate the eighth column

        # Uncomment to verify interpolation for each experment and IMU
        # Assuming imu_data and imu_data_interpolated are available
        time_imu_original = imu_data.iloc[:, 0]  # Original IMU timestamps (in nanoseconds)
        time_imu_interpolated = imu_data_interpolated.iloc[:, 0]  # Interpolated IMU timestamps (in nanoseconds)

        # Convert timestamps to seconds
        time_imu_original_modified = (time_imu_original - time_imu_original.iloc[0]) / 1e9
        time_imu_interpolated_modified = (time_imu_interpolated - time_imu_interpolated.iloc[0]) / 1e9

        # Extract acceleration data (original and interpolated)
        accel_x_imu_original = imu_data.iloc[:, 5]  # (original acceleration x-axis)
        accel_y_imu_original = imu_data.iloc[:, 6]  # (original acceleration y-axis)
        accel_z_imu_original = imu_data.iloc[:, 7]-9.81 # (original acceleration z-axis) - subtracting gravity for Z axis

        accel_x_imu_interpolated = imu_data_interpolated.iloc[:, 5]  # (interpolated acceleration x-axis)
        accel_y_imu_interpolated = imu_data_interpolated.iloc[:, 6]  # (interpolated acceleration y-axis)
        accel_z_imu_interpolated = imu_data_interpolated.iloc[:, 7] - 9.81  # (interpolated acceleration z-axis)

        print(f"Creating Interpolated IMU CSV file for {interpolated_data_folder}/{dir}")
        csv_file = "imu_samples_0.csv"
        csv_path = os.path.join(interpolated_data_folder,dir,csv_file)
        print(csv_path)
        imu_data_interpolated.to_csv(csv_path, index=False)  




