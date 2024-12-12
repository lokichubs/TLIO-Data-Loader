import numpy as np
import pandas as pd
import os
import json
import matplotlib.pyplot as plt
import pygetwindow as gw
import re

formatted_data_folder = 'FORMATTED_DATA_V3_ALIGNED'
imu_file = 'imu_samples_0.csv'
mocap_file = 'imu0_resampled.npy'


## Function that saves the numpy file
def save_numpy_file(data_frame, directory, filename):
    np.save(f"{directory}/{filename}.npy", data_frame)

def create_axs(imu_data,mocap_data,axs):
    # Extract time and acceleration data
    # Clear each subplot individually
    for ax in axs.flat:
        ax.clear()
    
    # Assuming imu_data is a Pandas DataFrame
    time_imu = imu_data.iloc[:, 0]  # First column (timestamp [ns])
    time_imu_modified = (time_imu - time_imu.iloc[0]) / 1e9
    accel_x_imu = imu_data.iloc[:, 5]  # (acceleration x-axis)
    accel_y_imu = imu_data.iloc[:, 6]  # (acceleration y-axis)
    accel_z_imu = imu_data.iloc[:, 7] - 9.81  # (acceleration z-axis)

    # Assuming mocap_data is a NumPy array
    time_mocap = mocap_data[:, 0]
    time_mocap_modified = (time_mocap - time_mocap[0]) / 1e6
    accel_x_mocap = mocap_data[:, 4]  # (acceleration x-axis)
    accel_y_mocap = mocap_data[:, 5]  # (acceleration y-axis)
    accel_z_mocap = mocap_data[:, 6]  # (acceleration z-axis)

    
    # Plot the first 30 seconds
    axs[0, 0].plot(time_imu_modified, accel_x_imu, label='Acceleration X (IMU)', color='red')
    axs[0, 0].plot(time_mocap_modified, accel_x_mocap, label='Acceleration X (MOCAP)', color='black')
    axs[0, 0].set_title('Acceleration X Data (First 30 seconds)')
    axs[0, 0].set_xlabel('Timestamp [s]')
    axs[0, 0].set_ylabel('Acceleration [m/s^2]')
    axs[0, 0].set_xlim(0, 30)
    axs[0, 0].legend()

    axs[1, 0].plot(time_imu_modified, accel_y_imu, label='Acceleration Y (IMU)', color='green')
    axs[1, 0].plot(time_mocap_modified, accel_y_mocap, label='Acceleration Y (MOCAP)', color='blue')
    axs[1, 0].set_title('Acceleration Y Data ( First 30 seconds)')
    axs[1, 0].set_xlabel('Timestamp [s]')
    axs[1, 0].set_ylabel('Acceleration [m/s^2]')
    axs[1, 0].set_xlim(0, 30)
    axs[1, 0].legend()

    axs[2, 0].plot(time_imu_modified, accel_z_imu, label='Acceleration Z (IMU)', color='purple')
    axs[2, 0].plot(time_mocap_modified, accel_z_mocap, label='Acceleration Z (MOCAP)', color='orange')
    axs[2, 0].set_title('Acceleration Z Data (First 30 seconds)')
    axs[2, 0].set_xlabel('Timestamp [s]')
    axs[2, 0].set_ylabel('Acceleration [m/s^2]')
    axs[2, 0].set_xlim(0, 30)
    axs[2, 0].legend()

    # Plot the last 30 seconds
    axs[0, 1].plot(time_imu_modified, accel_x_imu, label='Acceleration X (IMU)', color='red')
    axs[0, 1].plot(time_mocap_modified, accel_x_mocap, label='Acceleration X (MOCAP)', color='black')
    axs[0, 1].set_title('Acceleration X Data (Last 30 seconds)')
    axs[0, 1].set_xlabel('Timestamp [s]')
    axs[0, 1].set_ylabel('Acceleration [m/s^2]')
    axs[0, 1].set_xlim(max(time_imu_modified) - 30, max(time_imu_modified))
    axs[0, 1].legend()

    axs[1, 1].plot(time_imu_modified, accel_y_imu, label='Acceleration Y (IMU)', color='green')
    axs[1, 1].plot(time_mocap_modified, accel_y_mocap, label='Acceleration Y (MOCAP)', color='blue')
    axs[1, 1].set_title('Acceleration Y Data (Last 30 seconds)')
    axs[1, 1].set_xlabel('Timestamp [s]')
    axs[1, 1].set_ylabel('Acceleration [m/s^2]')
    axs[1, 1].set_xlim(max(time_imu_modified) - 30, max(time_imu_modified))
    axs[1, 1].legend()

    axs[2, 1].plot(time_imu_modified, accel_z_imu, label='Acceleration Z (IMU)', color='purple')
    axs[2, 1].plot(time_mocap_modified, accel_z_mocap, label='Acceleration Z (MOCAP)', color='orange')
    axs[2, 1].set_title('Acceleration Z Data (Last 30 seconds)')
    axs[2, 1].set_xlabel('Timestamp [s]')
    axs[2, 1].set_ylabel('Acceleration [m/s^2]')
    axs[2, 1].set_xlim(max(time_imu_modified) - 30, max(time_imu_modified))
    axs[2, 1].legend()

    return axs

def create_interactive_plot(imu_data, mocap_data,current_folder):

    # Create a figure and axis object with 6 subplots (3 rows x 2 columns)
    fig, axs = plt.subplots(3, 2, figsize=(9, 9))
    axs = create_axs(imu_data, mocap_data,axs)
    fig.tight_layout()

    plt.ion()
    plt.show()
    
    # Store clicked points
    points = []

    def onclick(event):
        nonlocal points
        if event.button == 1:  # Left mouse button
            points.append(event.xdata)
            print(f"Point clicked: {event.xdata}")

            if len(points) == 1:
                if points[0] == None:
                    print("Start Time cannot be Null. Reselect Ground Truth Start time")
                    points.pop(0)
                    return
                else:
                    print("Select the Ground Truth End time")
            elif len(points) == 2:
                if points[1] == None:
                    print("End Time cannot be Null. Reselect Ground Truth End time")
                    points.pop(1)
                    return
                elif points[1] <= points[0]:
                    print("End Time cannot be less than Start Time. Reselect Ground Truth End time")
                    points.pop(1)
                    return
                else:
                    print("Select the IMU Start time")

            elif len(points) == 3:
                if points[2] == None:
                    print("IMU Start Time cannot be Null. Reselect IMU Start time")
                    points.pop(2)
                    return
                else:
                    print("All points selected:")
                    print("Ground truth start:", points[0])
                    print("Ground truth end:", points[1])
                    print("IMU start:", points[2])

                
                # Here you can process the selected points and align the data
                [imu_data_aligned,mocap_data_aligned,]=align_and_plot(points,imu_data,mocap_data,axs)

                trial_number = re.findall(r'\d+', current_folder)[-1]
                print(f"Trial Number: {int(trial_number)}")


                
                #Creates file with time aligned IMU data
                print(f"Creating time aligned IMU CSV file for {current_folder}")
                csv_file = "imu_samples_0.csv"
                csv_path = os.path.join(current_folder, csv_file)
                imu_data_aligned.to_csv(csv_path, index=False)  


                #Creates file with time aligned MOCAP data
                print(f"Creating time aligned mocap npy for {current_folder}")
                save_numpy_file(mocap_data_aligned,current_folder,"imu0_resampled")

                print("Enter (y) to move onto the next plot")
                print("Enter (n) to redo the alignement of this plot")

                # Clear points for next selection
                points.clear()

    fig.canvas.mpl_connect('button_press_event', onclick)

    print("Select Ground Truth Start Time")

def align_and_plot(points,imu_data,mocap_data,axs):
    ground_truth_start, ground_truth_end, imu_start = points
    imu_end = imu_start + ground_truth_end - ground_truth_start
    
    time_imu = imu_data.iloc[:, 0]  # First column (timestamp [ns])
    time_imu_modified = (time_imu - time_imu.iloc[0]) / 1e9

    time_mocap = mocap_data[:, 0]
    time_mocap_modified = (time_mocap - time_mocap[0]) / 1e6  # Convert to seconds

    # Adjust MoCap data to the selected ground truth range
    mask_mocap = (time_mocap_modified >= ground_truth_start) & (time_mocap_modified <= ground_truth_end)
    mocap_data_aligned = mocap_data[mask_mocap]

    # Adjust IMU data to the selected start time
    mask_imu = (time_imu_modified >= imu_start) & (time_imu_modified <= imu_end)
    imu_data_aligned = imu_data[mask_imu]

    imu_data_aligned.iloc[:,0] = imu_data_aligned.iloc[:,0] - imu_data_aligned.iloc[0,0]
    mocap_data_aligned[:,0] = mocap_data_aligned[:,0] - mocap_data_aligned[0,0]

    axs = create_axs(imu_data_aligned,mocap_data_aligned,axs)

    plt.ion()
    plt.draw()

    return imu_data_aligned,mocap_data_aligned

## Main Loop to match time is below.
specific_file = 0

folder_count = 1
for root, dirs, files in os.walk(formatted_data_folder):
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

            create_interactive_plot(imu_data,mocap_data,current_folder)
        
        while True:
            if folder_count < specific_file:
                user_input = "y"
            else:
                user_input = input()

            if user_input == "y":
                plt.close()
                break  
            if user_input == "n":
                plt.close()
                print("Redo the alignment procedure for current folder")
                create_interactive_plot(imu_data,mocap_data,current_folder)

                
            

            
