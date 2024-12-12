To properly format any IMU and MOCAP dataset ensure to follow the process below:

** Note prior to executing these steps, Ensure to go through NAMING CONVENTION.txt file to ensure that the 
raw data files are named appropriatelt to enable automation.

1. Run the "renameCurrent.py" to properly assign each IMU its name (not the default names) if not already done.
    - You may have to go into the code and change the names based on the experiment

2. Run the "groundTruthFormat.py" to convert the MOCAP to the TLIO format
    - If you want to verify the plots run the ipynb file instead

3. Run the "imuFormat.py" to convert the IMU data to the TLIO format

4. Run the "createTxt.py" to assign create the training, test, validation split of the formatted data.

5. Run the "interpolateIMU.py" to emnsure the IMU sample frequency is ATLEAST 200 Hz (adjustable)

5. Run the "matchTimeV2.py" file to align the IMU and the MOCAP data manually

6. Run the "verifyAlignment.ipynb" file to double check the alignment for all the files.
    - If you want to go back and change any alignment open the "matchTimeV2.py" file and follow these steps
        - Change "folder_count" to the trial number that you want to change + 2 instead of  ">=0"
        - keep pressing "y" until a plot pops up.
        - Re-do the alignment for the dataset you want and then press "y" when its satisfactory
        - press "Ctrl+C" and press enter to terminate the script

The above should create a folder starting with "FORMATTED DATA" that ensures all the IMU and MOCAP data is formatted
as needed by the TLIO. Copy this into the instace whether the "TLIO~master" is on your device and move it to
the "local_data" file. Then it should be ready to train the model and run the EKF for the position and orientatione estimates
