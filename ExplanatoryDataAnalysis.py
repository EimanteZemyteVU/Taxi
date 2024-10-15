import pandas as pd
import DataImport

trips = DataImport.trips
zones = DataImport.zones

#cia bus funkcija kur paduodu trips ir zones ko gero ir paisysiu grafikus????
##################

pd.set_option('display.max_columns', None)  # None means no limit

trips.info(verbose = True) #A quick way to check the data types:
print(trips.describe()) #examine the summary statistics of each variable. Important for log's (>0)

print(trips.isnull().sum()) #Check null values count on each column