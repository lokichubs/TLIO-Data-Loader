## Run the groundTruthFormat.ipynb script first before as the initial position is from the ground truth 
import os
import pandas as pd
from datetime import datetime
import math
import re
import json
import numpy as np
import json
import numpy as np

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

# Function to get initial translation from ground truth file
def get_initial_translation(directory, gt_file):
    # directory: the directory where the ground truth file is located
    # gt_file: the name of the ground truth numpy file (without extension)

    file_path = f"{directory}/{gt_file}.npy"
    data = np.load(file_path)
    translation = data[0, 11:14].tolist()
    return translation

def get_initial_quaternion(directory, gt_file):
    # directory: the directory where the ground truth file is located
    # gt_file: the name of the ground truth numpy file (without extension)

    file_path = f"{directory}/{gt_file}.npy"
    data = np.load(file_path)
    quaternion= data[0, 7:11].tolist()
    return quaternion

#Key Folders where data is stored
imu_folder = 'IMU_7_11'
formatted_data_folder = 'FORMATTED_DATA'

if not os.path.exists(formatted_data_folder):
            os.makedirs(formatted_data_folder)

#Sample Folder with properly formatted data
sample_dir = 'SAMPLE_RESULT'
sample_file = "imu_samples_0.csv"
sample_path = os.path.join(sample_dir, sample_file)
sample_data = pd.read_csv(sample_path,index_col=False)

# Creates necessary inputs for json calibration file
accel_bias = pd.DataFrame(np.nan, index=range(3), columns=range(3))
gyro_bias = pd.DataFrame(np.nan, index=range(3), columns=range(3))
        

# Loop through the experiment folders in the IMU folder
for raw_folder in os.listdir(imu_folder):
    if raw_folder.startswith('Train_Data_') and raw_folder.endswith('_IMU'):
        raw_folder_path = os.path.join(imu_folder, raw_folder)
        csv_files = [file for file in os.listdir(raw_folder_path) if file.endswith('.csv')]
        base_names = [os.path.splitext(file)[0] for file in csv_files]
    
    # Loop through the csv files in the raw  data folder
    trial_number = re.findall(r'\d+', raw_folder)[0]

    for i, base_name in enumerate(base_names):

        # Creates raw IMU data instance
        raw_dir = os.path.join(imu_folder,raw_folder)
        raw_file =  f"{base_name}.csv"
        raw_path = os.path.join(raw_dir, raw_file)
        raw_data = pd.read_csv(raw_path,index_col=False)

        # Duplicates sample format
        formatted_data = pd.DataFrame(columns=sample_data.columns)

        # format first column of raw_data
        time_datetime = raw_data.iloc[:, 0].apply(lambda x: datetime.strptime(x.strip(), "%H:%M:%S.%f"))
        time_ns = time_datetime.apply(lambda x: int(x.timestamp() * 1e9))
        time_ns = time_ns - time_ns.iloc[0]
        formatted_data.iloc[:, 0] = time_ns.values

        #copys the IMU remperature data into formatted_data
        formatted_data.iloc[:,1] = raw_data.values[:,15]

        # Copys the IMU gyro data into formatted_data
        formatted_data.iloc[:,2] = raw_data.values[:,6] * math.pi / 180 
        formatted_data.iloc[:,3] = raw_data.values[:,7] * math.pi / 180
        formatted_data.iloc[:,4] = raw_data.values[:,8] * math.pi / 180

        # Copys the IMU acceleration data into formatted_data
        formatted_data.iloc[:,5] = raw_data.values[:,3]*9.81  
        formatted_data.iloc[:,6] = raw_data.values[:,4]*9.81
        formatted_data.iloc[:,7] = raw_data.values[:,5]*9.81

        # Define the rotation matrix for a 90-degree anti-clockwise rotation about the z-axis 
        # This is to ensure the IMU is converted to the "gravity aligned frame"
        rotation_matrix = np.array([[0, -1, 0],
                            [1, 0, 0],
                            [0, 0, 1]])

        # Apply the rotation to the acceleration data
        formatted_data.iloc[:, 5:8] = np.dot(formatted_data.iloc[:, 5:8].values, rotation_matrix)

        # Apply the rotation to the gyro data
        formatted_data.iloc[:, 2:5] = np.dot(formatted_data.iloc[:, 2:5].values, rotation_matrix)

        formatted_data_v2 = formatted_data.groupby(formatted_data.columns[0]).mean().reset_index()

        # Create the formatted folder if it doesn't exist
        formatted_folder = f"data_{base_name}_{trial_number}"
        formatted_path = os.path.join(formatted_data_folder, formatted_folder)
        if not os.path.exists(formatted_path):
            os.makedirs(formatted_path)

        # Write the formatted data to a CSV file
        print(f"Creating csv for {base_name}_{trial_number}")
        csv_file = "imu_samples_0.csv"
        csv_path = os.path.join(formatted_path, csv_file)
        formatted_data_v2.to_csv(csv_path, index=False)  
        
        

        #Assigns the calibration variables the correct values 
        if int(trial_number) == 0:
            accel_bias.iloc[i,:] = formatted_data.iloc[:, 5:8].mean().tolist()
            gyro_bias.iloc[i,:] = formatted_data.iloc[:, 2:5].mean().tolist()
            accel_bias.iloc[i,2] = accel_bias.iloc[i,2] - 9.81
        time_offset_accel = 0.0013
        time_offset_gyro = 0.0013               
        translation = get_initial_translation(formatted_path,"imu0_resampled")
        unit_quaternion = get_initial_quaternion(formatted_path,"imu0_resampled")
        
        # Creates json calibration file
        print(f"Creating calibration for {base_name}_{trial_number}")
        create_imu_calibration_file(formatted_path,"calibration", accel_bias.iloc[i,:].tolist(), 
                                    gyro_bias.iloc[i,:].tolist(), time_offset_accel, time_offset_gyro, 
                                    translation, unit_quaternion)
