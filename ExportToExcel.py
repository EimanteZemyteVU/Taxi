import zipfile
import pandas as pd
import re
import ProcessTrips
import openpyxl
import DataImport

trips_import = ProcessTrips.transformTrips(DataImport.trips)

trips_import.to_csv('trips_import_2020-01.csv', index=False)

