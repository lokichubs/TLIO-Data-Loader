# TLIO Data Loader for IMU and MOCAP

This github repo contains the code for a data loader built to format the IMU and MOCAP data to be usable in the a href="https://github.com/CathIAS/TLIO">TLIO</a> model.

[Naming Convention](naming-convention)
[MOCAP Data Transform](#mocap-data-transform)  
[IMU Data Transform](#imu-data-transform)  
[IMU Interpolation](#imu-interpolation-and-alignment)
[Data Time Alignment](#data-time-alignment)
[Create Data Batches](#create-data-batches)  

## Naming Convention
### Ground Truth naming Convention
Ensure to name any of the ground trust data following the structure below
    "Train_data_##.csv"

Also ensure that the MOCAP data is saved as a .csv file

### IMU Naming convention:
The IMU data pipeline generates a folder from the software. Ensure to name the resulting folder as follows
    "Train_Data_##_IMU"

The folder will contain n (the number of IMU's) .csv, .wplay, and 1 Matlab folder. Double check to ensure
you have three separate csv files each IMU - the IMU pipeline default is to combine all the active IMU's into
one csv file

## MOCAP Data Transform

## IMU Data Transform

## IMU Interpolation

## Data Time Alignment

## Create Data Batches
