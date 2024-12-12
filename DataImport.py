
import os
import pandas as pd
import re

# Get the directory of the script itself
script_dir = os.path.dirname(os.path.abspath(__file__))

# # Read the CSV file into a DataFrame
filename = "yellow_tripdata_2020-06.csv"

trips = pd.read_csv(filename)
zones =  pd.read_csv("taxi+_zone_lookup.csv")

#Add a column 'file_date' to get date of the file
# Extract the date using regex
match = re.search(r"(\d{4}-\d{2})", filename)  # Match the pattern YYYY-MM

# Assign YYYY-MM-01 format, add column to dataframe and convert to datetime
formatted_date = f"{match.group(1)}-01" if match else None
trips['file_date'] = pd.to_datetime(formatted_date)


# import zipfile
# import pandas as pd
# import re


# # Lists to hold DataFrames for trips and zones
# dfs_trips = []
# dfs_zones = []

# # Open and process the ZIP file
# with zipfile.ZipFile('archive_tmp.zip', 'r') as archive:
#     for file_name in archive.namelist():
#         if file_name.endswith('.csv'):
#             # Extract the date from the filename (using regex YYYY-MM)
#             match = re.search(r"(\d{4}-\d{2})", file_name)
#             formatted_date = f"{match.group(1)}-01" if match else None

#             # Open and read the CSV file
#             with archive.open(file_name) as file:
#                 try:
#                     df = pd.read_csv(file)

#                     # Add a 'file_date' column if the date is extracted
#                     if formatted_date:
#                         df['file_date'] = pd.to_datetime(formatted_date)

#                     # Separate zones and trips data
#                     if 'taxi+_zone_lookup' in file_name:
#                         dfs_zones.append(df)
#                     else:
#                         dfs_trips.append(df)
#                 except Exception as e:
#                     print(f"Error reading {file_name}: {e}")

# # Concatenate DataFrames for trips and zones
# trips = pd.concat(dfs_trips, ignore_index=True) if dfs_trips else None
# zones = pd.concat(dfs_zones, ignore_index=True) if dfs_zones else None

