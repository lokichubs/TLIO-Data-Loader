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
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt



def convert_time_to_seconds(time_str):
    # Split the time by colon and dot
    time_parts = time_str.split(':')
    hours = int(time_parts[0])
    minutes = int(time_parts[1])
    seconds_and_ms = time_parts[2].split('.')
    seconds = int(seconds_and_ms[0])
    milliseconds = int(seconds_and_ms[1]) if len(seconds_and_ms) > 1 else 0
    
    # Convert the entire time to seconds
    total_seconds = hours * 3600 + minutes * 60 + seconds + milliseconds / 1000.0
    return total_seconds

def adjust_repeated_timestamps(df):
    """
    Adjust repeated timestamps by distributing the time difference evenly across repeated values.
    
    Args:
    - df (pd.DataFrame): The input dataframe with repeated timestamps
    - time_column (str): The name of the column containing the timestamps
    
    Returns:
    - pd.DataFrame: The dataframe with adjusted timestamps
    """
    # Initialize an empty list to store the adjusted times
    adjusted_times = []
    frequency_hz = 200
    period_seconds = 1.0 / frequency_hz
    # Get the time column from the DataFrame
    time_col = df.values
    
    # Initialize variables to track the previous time and the starting index of repeated times
    prev_time = time_col[0]
    start_index = 0
    
    # Iterate over the DataFrame rows
    for i in range(1, len(df)):
        current_time = time_col[i]
        
        if current_time != prev_time:
            # Calculate the time difference between the first repeated time and the last one
            time_diff = current_time - prev_time
            num_repeats = i - start_index +1
            
            if num_repeats > 1:
                # Distribute the time difference evenly across the repeated timestamps
                for j in range(start_index, i):
                    adjusted_times.append(prev_time + (time_diff * (j - start_index) / (num_repeats - 1)))
            else:
                # If only one timestamp is repeated, no need to adjust
                adjusted_times.append(prev_time)
            
            # Update previous time and the starting index for the next group of repeated timestamps
            prev_time = current_time
            start_index = i
    
    # Handle the last group of repeated timestamps
    time_diff = time_col[-1] - prev_time
    num_repeats = len(df) - start_index
    if num_repeats > 1:
        for j in range(start_index, len(df)):
            adjusted_times.append(prev_time + (time_diff * (j - start_index) / (num_repeats - 1)))
    else:
        adjusted_times.append(prev_time)
    
    # If the last block is repeated, adjust it based on the 200 Hz frequency
    if num_repeats > 1:
        for j in range(start_index, len(df)):
            adjusted_times[j] = prev_time + (j - start_index) * period_seconds

    return pd.Series(adjusted_times)  # Return adjusted times as a pandas Series



#Key Folders where data is stored
imu_folder = 'IMU_11_8'
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
        num_samples = len(raw_data)  # Get the number of samples in your dataset
        frequency_hz = 198  # Frequency in Hz
        period_ns = int(1e9 / frequency_hz)  # Period in nanoseconds
        time_ns = pd.Series(range(num_samples)) * period_ns
        formatted_data.iloc[:,0] = time_ns.values

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

        formatted_data_v2 = formatted_data.copy()
        imu_smooth = formatted_data_v2.copy()
        # window_size = 5
        # imu_smooth.iloc[:,2:8] = imu_smooth.iloc[:,2:8].rolling(window=window_size,min_periods=1).mean()

        # Create the formatted folder if it doesn't exist
        formatted_folder = f"data_{base_name}_{trial_number}"
        formatted_path = os.path.join(formatted_data_folder, formatted_folder)
        if not os.path.exists(formatted_path):
            os.makedirs(formatted_path)

        # Write the formatted data to a CSV file
        print(f"Creating csv for {base_name}_{trial_number}")
        csv_file = "imu_samples_0.csv"
        csv_path = os.path.join(formatted_path, csv_file)
        imu_smooth.to_csv(csv_path, index=False)  
        
        

 