import pandas as pd
import ProcessTrips
import DataImport


tripsImport = DataImport.trips
zonesImport = DataImport.zones

trips = ProcessTrips.transformTrips(tripsImport)
print(trips)
# print(zones)


