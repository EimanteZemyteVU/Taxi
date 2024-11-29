import pandas as pd

def transformTrips(trips):

    # Convert pickup and dropoff columns to datetime
    trips['tpep_pickup_datetime'] = pd.to_datetime(trips['tpep_pickup_datetime'], errors='coerce')
    trips['tpep_dropoff_datetime'] = pd.to_datetime(trips['tpep_dropoff_datetime'], errors='coerce')

    # Filter rows to include only those with dropoff/pickup dates up to and including 2020-08-01"
    # Define the cutoff date as the end of date of all sheets
    cutoff_date = pd.Timestamp("2019-02-01") #laikinai --- pd.Timestamp("2020-08-01")
    trips = trips[trips['tpep_dropoff_datetime'] < cutoff_date]
    trips = trips[trips['tpep_pickup_datetime'] < cutoff_date]

    cutoff_date_left = pd.Timestamp("2019-01-01")
    trips = trips[trips['tpep_dropoff_datetime'] >= cutoff_date_left]
    trips = trips[trips['tpep_pickup_datetime'] >= cutoff_date_left]


    # Filter out negative values
    # List of columns to check for values >= 0
    columns_to_check = ['extra', 'mta_tax', 'tip_amount', 'tolls_amount', 'improvement_surcharge', 'total_amount']
    trips = trips[(trips[columns_to_check] >= 0).all(axis=1)]


    # # Extract date and time for pickup
    trips['pickup_date'] = trips['tpep_pickup_datetime'].dt.floor('D')
    trips['pickup_time'] = trips['tpep_pickup_datetime'].dt.strftime('%H:%M:%S')

    # # Extract date and time for dropoff
    trips['dropoff_date'] = trips['tpep_dropoff_datetime'].dt.floor('D')
    trips['dropoff_time'] = trips['tpep_dropoff_datetime'].dt.strftime('%H:%M:%S')

    # Calculate the duration of each trip in seconds
    trips['trip_duration'] = (trips['tpep_dropoff_datetime'] - trips['tpep_pickup_datetime']).dt.total_seconds()


    # Adjust total_amount to exclude tips
    # Reason: total_amount has only card tips included (cash tips are not registered),
    trips['total_amount'] -= trips['tip_amount']

    # Add columns for visuals
    trips['pickup_hour'] = trips['tpep_pickup_datetime'].dt.hour
    trips['pickup_weekday'] = trips['tpep_pickup_datetime'].dt.day_name()

    #LAIKINAS: - PASISALINU OUTLIERS NAUDOJANT IQR nes labai iskraipo grafikus ir negaliu apimti 
    #visu atveju su vieno excelio duomenim

    # List of numerical columns to check for outliers
    columns_to_check = ['fare_amount', 'extra', 'mta_tax', 'tip_amount', 'tolls_amount', 
                        'improvement_surcharge', 'total_amount', 'trip_distance', 'passenger_count']

    # Calculate IQR and filter out outliers for each column
    Q1 = trips[columns_to_check].quantile(0.25)
    Q3 = trips[columns_to_check].quantile(0.75)
    IQR = Q3 - Q1

    # Define lower and upper bounds for outliers
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Apply the filtering condition to remove outliers
    filtered_trips = trips[~((trips[columns_to_check] < lower_bound) | (trips[columns_to_check] > upper_bound)).any(axis=1)]

    # Update the trips dataframe with the filtered rows
    trips = filtered_trips

    # Optional: Verify the number of rows before and after filtering
    print(f"Original number of rows: {len(trips)}")
    print(f"Number of rows after removing outliers: {len(filtered_trips)}")


    return trips

def MergeZones(trips, zones):
    trips = trips.merge(zones, left_on='PULocationID', right_on='LocationID', how='left', suffixes=('_pickup', '_pickup_zone'))
    trips = trips.merge(zones, left_on='DOLocationID', right_on='LocationID', how='left', suffixes=('_pickup', '_dropoff'))
    trips = trips.drop(columns=['LocationID_pickup', 'LocationID_dropoff'])
    trips = trips.rename(columns={'Zone_pickup': 'pickup_zone', 'Zone_dropoff': 'dropoff_zone'})
    return trips