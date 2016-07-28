"""
Program: preprocessing.py

Takes in data files and standardises them by applying a coordinate transform and converting all files to csv,.

This is an ad hoc step so is best run line by line!

@author Chris Williams
"""

import pandas as pd
import pyproj 
import matplotlib.pyplot as plt

# read data in
print("Reading data in...")
meas = pd.read_csv("../data/original_data/measurement.txt", sep='	')
bore = pd.read_csv("../data/original_data/borehole.txt", sep='	')
foss = pd.read_csv("../data/original_data/fossil.txt", sep='	')
rock = pd.read_csv("../data/original_data/rock.txt", sep='	')

#coordinate transformation - BNG to latlon
print("Converting to lat/lon...")
bng=pyproj.Proj("+init=EPSG:27700")
lon_bore, lat_bore = bng(bore['X'].values, bore['Y'].values, inverse=True)
lon_rock, lat_rock = bng(rock['X'].values, rock['Y'].values, inverse=True)

bore=bore.drop('X', axis=1)
bore=bore.drop('Y', axis=1)
bore['Latitude_WGS84']=pd.Series(lat_bore, index=bore.index)
bore['Longitude_WGS84']=pd.Series(lon_bore, index=bore.index)

rock=rock.drop('X', axis=1)
rock=rock.drop('Y', axis=1)
rock['Latitude_WGS84']=pd.Series(lat_rock, index=rock.index)
rock['Longitude_WGS84']=pd.Series(lon_rock, index=rock.index)

# overview plot
plt.scatter(meas['Latitude (WGS84)'].values, meas['Longitude (WGS84)'].values, c='red', label='measurement')
plt.scatter(foss['Latitude (WGS84)'].values, foss['Longitude (WGS84)'].values, c='blue', label='fossil')
plt.scatter(bore['Latitude_WGS84'].values, bore['Longitude_WGS84'].values, c='black', label='borehole')
plt.scatter(rock['Latitude_WGS84'].values, rock['Longitude_WGS84'].values, c='green', label='rock')
plt.legend(loc=4)
plt.title("Relative measurement locations")
plt.show()

# convert all to csv (same headers - no spaces in names)
foss.columns = ['Name','Type','Latitude_WGS84','Longitude_WGS84','Z','Date','Time','Recorded_by','Species', 'Image']
foss.to_csv('../data/fossil_WGS84.csv', sep=',', index=False)

meas.columns = ['Name','Type','Latitude_WGS84','Longitude_WGS84','Z','Date','Time','Recorded_by','Porosity']
meas.to_csv('../data/measurement_WGS84.csv', sep=',', index=False)

bore.columns = ['Name','Type','Z','Date','Time','Recorded_by','Drilled_depth_m','Latitude_WGS84','Longitude_WGS84']
bore.to_csv('../data/borehole_WGS84.csv', sep=',', index=False)

rock.columns = ['Name','Type','Z','Date','Time','Recorded_by','Rock_name','Image','Latitude_WGS84','Longitude_WGS84']
rock.to_csv('../data/rock_WGS84.csv', sep=',', index=False)


