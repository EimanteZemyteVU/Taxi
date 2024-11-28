import os
import pandas as pd

# # Define directory
# new_directory = r"C:\Users\Eimante\OneDrive - Vilnius University\Documents\GitHub\Taxi"
# # Change the current working directory
# os.chdir(new_directory)

# Get the directory of the script itself
script_dir = os.path.dirname(os.path.abspath(__file__))

# Read the CSV file into a DataFrame
trips = pd.read_csv("yellow_tripdata_2019-01_full.csv")
zones =  pd.read_csv("taxi+_zone_lookup.csv")


