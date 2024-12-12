import zipfile
import pandas as pd
import re
from sqlalchemy import create_engine
import psycopg2

# Database connection details
DATABASE_TYPE = 'postgresql'
DBAPI = 'psycopg2'
HOST = 'postgres'  # Use the service name defined in docker-compose.yml
USER = 'admin'
PASSWORD = 'admin'
DATABASE = 'taxi'
PORT = 5432

# Connection string 
default_db_url = f"{DATABASE_TYPE}://{USER}:{PASSWORD}@{HOST}:{PORT}/postgres"

# Create a connection to the default database (postgres) to check and create the 'taxi' database if needed
connection = psycopg2.connect(default_db_url)
connection.autocommit = True
cursor = connection.cursor()

# Check if 'taxi' database exists, and create it if necessary
cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'taxi';")
exists = cursor.fetchone()

if not exists:
    cursor.execute(f"CREATE DATABASE {DATABASE};")
    print(f"Database '{DATABASE}' created.")

cursor.close()
connection.close()

# Now create the full database URL for the 'taxi' database
DATABASE_URL = f"{DATABASE_TYPE}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"

# Create an SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Lists to hold DataFrames for trips and zones
dfs_trips = []
dfs_zones = []

# Open and process the ZIP file
with zipfile.ZipFile('archive_tmp.zip', 'r') as archive:
    for file_name in archive.namelist():
        if file_name.endswith('.csv'):
            # Extract the date from the filename (using regex YYYY-MM)
            match = re.search(r"(\d{4}-\d{2})", file_name)
            formatted_date = f"{match.group(1)}-01" if match else None

            # Open and read the CSV file
            with archive.open(file_name) as file:
                try:
                    df = pd.read_csv(file)

                    # Add a 'file_date' column if the date is extracted
                    if formatted_date:
                        df['file_date'] = pd.to_datetime(formatted_date)

                    # Separate zones and trips data
                    if 'taxi+_zone_lookup' in file_name:
                        dfs_zones.append(df)
                    else:
                        dfs_trips.append(df)
                except Exception as e:
                    print(f"Error reading {file_name}: {e}")

# Concatenate DataFrames for trips and zones
final_trips_df = pd.concat(dfs_trips, ignore_index=True) if dfs_trips else None
final_zones_df = pd.concat(dfs_zones, ignore_index=True) if dfs_zones else None

# Insert DataFrames into PostgreSQL
if final_trips_df is not None:
    final_trips_df.to_sql('trips', engine, if_exists='replace', index=False)
    print("Trips data successfully exported to the 'trips' table.")
else:
    print("No trips data to export.")

if final_zones_df is not None:
    final_zones_df.to_sql('zones', engine, if_exists='replace', index=False)
    print("Zones data successfully exported to the 'zones' table.")
else:
    print("No zones data to export.")
