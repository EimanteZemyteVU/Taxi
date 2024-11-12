import pandas as pd
import scipy
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt



import DataImport
import ProcessTrips

trips = ProcessTrips.transformTrips(DataImport.trips)
zones = DataImport.zones

#cia bus funkcija kur paduodu trips ir zones ko gero ir paisysiu grafikus????
##################

pd.set_option('display.max_columns', None)  # None means no limit

trips.info(verbose = True) #A quick way to check the data types:
print(trips.describe()) #examine the summary statistics of each variable. Important for log's (>0)

print(trips.isnull().sum()) #Check null values count on each column

#Pasiskaiciuoju tik stiprias koreliacijas (virs 0.5) ir grazinu tiek jas, tiek sarasa stulpeliu. Sarasa naudoju vizualams
def filter_strong_correlations(df, threshold=0.5):
    """
    Filters a correlation matrix by keeping only correlations greater than a specified threshold
    and removes self-correlations (diagonal) and rows/columns with all NaN values.

    Parameters:
    - df (pd.DataFrame): The input DataFrame.
    - threshold (float): The correlation threshold for filtering (default is 0.5).

    Returns:
    - pd.DataFrame: The filtered correlation matrix.
    """
    # Compute correlation matrix for numeric columns only
    correlation_matrix = df.select_dtypes(include=['number']).corr()

    # Filter to keep only values > threshold or < -threshold
    filtered_corr = correlation_matrix.where((correlation_matrix > threshold) | (correlation_matrix < -threshold))

    # Set the diagonal (self-correlations) to NaN
    np.fill_diagonal(filtered_corr.values, np.nan)

    # Drop rows and columns where all values are NaN
    filtered_corr = filtered_corr.dropna(how='all').dropna(axis=1, how='all')

     # Get the list of columns retained
    retained_columns = filtered_corr.columns.tolist()

    return filtered_corr, retained_columns

#  usage
filtered_corr, retained_columns = filter_strong_correlations(trips, threshold=0.5)

# Create a new DataFrame with only the retained columns
filtered_trips = trips[retained_columns]

#Reikes pasikoreguoti spalvas kazkaip issiryskint kooreliuojancias vietas ir matosi multikolinearumas tarp fare ir total amount
def reg_coef(x, y, label=None, color=None, **kwargs):
    # A modified version of https://stackoverflow.com/a/63433499
    ax = plt.gca()
    r,p = scipy.stats.pearsonr(x, y)
    val = 'r = {:.3f}'.format(r)
    if p <= 0.001:
        val = val + "***"  
    elif p <= 0.01:
        val = val + "**"  
    elif p <= 0.05:
        val = val + "*"    
    ax.annotate(val, xy=(0.5, 0.5), xycoords='axes fraction', ha='center')
    ax.set_axis_off()
g = sns.PairGrid(filtered_trips, diag_sharey = False)
tmp_plt = g.map_diag(sns.histplot)
tmp_plt = g.map_lower(sns.scatterplot)
tmp_plt = g.map_upper(reg_coef)
#plt.show()


