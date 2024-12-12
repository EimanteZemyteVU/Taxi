import pandas as pd
from pandas.tseries.offsets import MonthEnd

def transformTrips(trips):

    # Convert pickup and dropoff columns to datetime
    trips['tpep_pickup_datetime'] = pd.to_datetime(trips['tpep_pickup_datetime'], errors='coerce')
    trips['tpep_dropoff_datetime'] = pd.to_datetime(trips['tpep_dropoff_datetime'], errors='coerce')

    # Drop the column 'congestion_surcharge' from the DataFrame (contains lots of null values)
    trips = trips.drop(columns=['congestion_surcharge'])

    #--- Add cutoff values and filter
    # Calculate End of Month and add 1 day 
    trips['eom_plus_1'] = trips['file_date'] + MonthEnd(1) + pd.Timedelta(days=1)

    #Create cutoff_date for filtering
    cutoff_date = trips['eom_plus_1'].iloc[0]  # Use first EOM date
    cutoff_date_left = trips['file_date'].iloc[0]  # Use first file_date

    # Filter trips based on dynamic cutoff_date
    trips = trips[
        (trips['tpep_dropoff_datetime'] <= cutoff_date) &
        (trips['tpep_pickup_datetime'] <= cutoff_date) &
        (trips['tpep_dropoff_datetime'] >= cutoff_date_left) &
        (trips['tpep_pickup_datetime'] >= cutoff_date_left)
]

    # Filter out negative values
    # List of columns to check for values >= 0
    columns_to_check = ['fare_amount', 'extra', 'mta_tax', 'tip_amount', 'tolls_amount', 'improvement_surcharge', 'total_amount']
    trips = trips[(trips[columns_to_check] >= 0).all(axis=1)]

    #Extract date and time for pickup and dropoff
    trips['pickup_date'] = trips['tpep_pickup_datetime'].dt.floor('D')
    trips['pickup_time'] = trips['tpep_pickup_datetime'].dt.strftime('%H:%M:%S')

    trips['dropoff_date'] = trips['tpep_dropoff_datetime'].dt.floor('D')
    trips['dropoff_time'] = trips['tpep_dropoff_datetime'].dt.strftime('%H:%M:%S')

    # Calculate the duration of each trip in seconds
    trips['trip_duration'] = (trips['tpep_dropoff_datetime'] - trips['tpep_pickup_datetime']).dt.total_seconds()

    # Adjust total_amount to exclude tips
    # Reason: total_amount has only card tips included (cash tips are not registered),
    trips['total_amount'] -= trips['tip_amount']

    #Add additional columns for visuals
    trips['pickup_hour'] = trips['tpep_pickup_datetime'].dt.hour
    trips['pickup_weekday'] = trips['tpep_pickup_datetime'].dt.day_name()

    # Encode locations
    # Replace each LocationID with the average total_amount for that LocationID
    # https://www.kaggle.com/code/ryanholbrook/target-encoding
    for col in ['PULocationID', 'DOLocationID', 'VendorID']:
        trips[f'{col}_encoded'] = trips.groupby(col)['total_amount'].transform('mean')
        

    # Remove outliers by calculating IQR and defining bounds
    # List of numerical columns to check for outliers
    columns_to_check = ['fare_amount', 'extra', 'mta_tax', 'tip_amount', 'tolls_amount', 'trip_duration',
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

    print("Outliers removed using IQR")

    # Filter out rows with NA values
    trips = trips.dropna()
    print(f"Number of rows after dropping NA values: {len(trips)}")


    return trips

def MergeZones(trips, zones):
    trips = trips.merge(zones, left_on='PULocationID', right_on='LocationID', how='left', suffixes=('_pickup', '_pickup_zone'))
    trips = trips.merge(zones, left_on='DOLocationID', right_on='LocationID', how='left', suffixes=('_pickup', '_dropoff_zone'))
    # trips = trips.drop(columns=['LocationID_pickup', 'LocationID_dropoff'])
    trips = trips.rename(columns={'Zone_pickup': 'pickup_zone', 'Zone_dropoff': 'dropoff_zone'})
    return trips