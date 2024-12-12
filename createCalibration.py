import numpy as np
import pandas as pd
import os
import json
import matplotlib.pyplot as plt
import pygetwindow as gw
import re

# Function that creates the groudn truth description json file required for the TLIO model
def create_gt_description_file(num_rows,frequency,t_start_us, t_end_us, directory, filename):
    
# num rows: the number of samples we have in the ground truth:
# frequency : the polling rate of the MOCAP system
# t_start_us: the start time of the recording in microseconds
# t_end_us: the end time of the recording in microseconds
# directory: the directory where the json file will be saved
# filename: the name of the json file to be saved

    data = {
        "columns_name(width)": [
            "ts_us(1)", #Time in microseconds
            "gyr_compensated_rotated_in_World(3)", #gyro in x y z directions
            "acc_compensated_rotated_in_World(3)", #accerleration in x y z directions
            "qxyzw_World_Device(4)", #quaternion in x y z directions
            "pos_World_Device(3)", #position in x y z directions
            "vel_World(3)" #velocity in x y z directions
        ],
        "num_rows": num_rows,
        "approximate_frequency_hz": frequency, 
        "t_start_us": t_start_us,
        "t_end_us": t_end_us
    }

    with open(f"{directory}/{filename}.json", 'w') as f:
        json.dump(data, f, indent=4)

# Function to create calibration.json file as needed
def create_imu_calibration_file(file_directory, file_name, accel_bias, gyro_bias, time_offset_accel, time_offset_gyro, translation, unit_quaternion):
    # file_directory: the directory where the JSON file will be saved
    # file_name: the name of the JSON file to be saved
    # accel_bias: the bias values for the accelerometer
    # gyro_bias: the bias values for the gyroscope
    # time_offset_accel: the time offset for the accelerometer
    # time_offset_gyro: the time offset for the gyroscope
    # translation: the translation vector for the IMU
    # unit_quaternion: the unit quaternion representing the IMU orientation

    accel_rectification_matrix = np.eye(3).tolist()
    gyro_rectification_matrix = np.eye(3).tolist()

    imu_calibration_data = {
        "Accelerometer": {
            "Bias": {
                "Name": "Constant",
                "Offset": accel_bias
            },
            "Model": {
                "Name": "Linear",
                "RectificationMatrix": accel_rectification_matrix
            },
            "TimeOffsetSec_Device_Accel": time_offset_accel
        },
        "Calibrated": True,
        "Gyroscope": {
            "Bias": {
                "Name": "Constant",
                "Offset": gyro_bias
            },
            "Model": {
                "Name": "Linear",
                "RectificationMatrix": gyro_rectification_matrix
            },
            "TimeOffsetSec_Device_Gyro": time_offset_gyro
        },
        "Label": "unlabeled_imu_0",
        "SerialNumber": "rift://",
        "T_Device_Imu": {
            "Translation": translation,
            "UnitQuaternion": unit_quaternion
        }
    }

    file_path = f"{file_directory}/{file_name}.json"
    with open(file_path, 'w') as f:
        json.dump(imu_calibration_data, f, indent=4)

interpolated_data_folder = "FORMATTED_DATA_V3_ALIGNED_INTERPOLATED"
imu_file = 'imu_samples_0.csv'
imu_json = 'calibration.json'
mocap_file = 'imu0_resampled.npy'
mocap_json = 'imu0_resampled_description.json'

## Main Loop to match time is below.
accel_bias = pd.DataFrame(np.nan, index=range(1), columns=range(3))
gyro_bias = pd.DataFrame(np.nan, index=range(1), columns=range(3))

specific_file = 0

folder_count = 1
for root, dirs, files in os.walk(interpolated_data_folder):
    for dir in dirs:
        folder_count += 1
        if folder_count >= specific_file :

            current_folder = os.path.join(root, dir)
            print(f"Processing folder: {current_folder}")

            # Construct file paths
            imu_file_path = os.path.join(current_folder, imu_file)
            mocap_file_path = os.path.join(current_folder, mocap_file)

            # Read IMU data
            if os.path.exists(imu_file_path):
                imu_data = pd.read_csv(imu_file_path)
                print("IMU data loaded")

            # Read MoCap data
            if os.path.exists(mocap_file_path):
                mocap_data = np.load(mocap_file_path)
                print("MoCap data loaded")

            trial_number = re.findall(r'\d+', current_folder)[-1]
            print(f"Trial Number: {int(trial_number)}")

            if int(trial_number) == 0:
                accel_bias.iloc[0,:] = imu_data.iloc[:, 5:8].mean().tolist()
                gyro_bias.iloc[0,:] = imu_data.iloc[:, 2:5].mean().tolist()
                accel_bias.iloc[0,2] = accel_bias.iloc[0,2] - 9.81
                print(f"Acceleration bias is: {accel_bias}")
            
            time_offset_accel = 0.0013
            time_offset_gyro = 0.0013               
            translation =  mocap_data[0, 11:14].tolist()
            unit_quaternion = mocap_data[0,7:11].tolist()

            num_rows = mocap_data.shape[0]
            t_start_us = mocap_data[0,0]
            t_end_us = mocap_data[-1,0]
            freq_VICON = 200
            
            print(f"Creating IMU JSON calibtation file for {current_folder}")
            create_imu_calibration_file(current_folder,"calibration", accel_bias.iloc[0,:].tolist(), 
                                gyro_bias.iloc[0,:].tolist(), time_offset_accel, time_offset_gyro, 
                                translation, unit_quaternion)
            
            #Creates file with time aligned MOCAP data description json file
            print(f"Creating MOCAP JSON calibtation file for {current_folder}")
            create_gt_description_file(num_rows,freq_VICON,t_start_us, t_end_us, current_folder, "imu0_resampled_description")
            

        