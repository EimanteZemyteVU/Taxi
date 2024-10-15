import pandas as pd

def transformTrips(trips):

    # Convert pickup and dropoff columns to datetime
    trips['tpep_pickup_datetime'] = pd.to_datetime(trips['tpep_pickup_datetime'], errors='coerce')
    trips['tpep_dropoff_datetime'] = pd.to_datetime(trips['tpep_dropoff_datetime'], errors='coerce')


    # Extract date and time for pickup
    trips['pickup_date'] = trips['tpep_pickup_datetime'].dt.date
    trips['pickup_time'] = trips['tpep_pickup_datetime'].dt.time

    # Extract date and time for dropoff
    trips['dropoff_date'] = trips['tpep_dropoff_datetime'].dt.date
    trips['dropoff_time'] = trips['tpep_dropoff_datetime'].dt.time

    # Calculate the duration of each trip and format it to hh:mm:ss
    trips['trip_duration'] = (trips['tpep_dropoff_datetime'] - trips['tpep_pickup_datetime']).apply(lambda x: str(x).split()[2] if pd.notnull(x) else None)


    return trips
