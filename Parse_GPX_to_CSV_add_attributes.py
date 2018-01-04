"""

Convert a directory of GPX files to CSV
=======================================

Convert a directory of GPX files to CSV of timestamp, lat, long, elevation
Add cumulative time and distance per ride or run
Add type of activity ie. ride or run

Requirements
------------

:requires: gpxpy
:requires: os
:requires: pandas
:requires: numpy

Version
-------
:date: 04-Jan-18
"""

## Import libraries
import gpxpy
import os
import pandas as pd
import numpy as np

## Change these global variables to match your input and output data directories
INDIR = r'\my\input\folder'
OUTDIR = r'\my\output\folder'

def parsegpx(f):
    """
    Parse a GPX file into a list of dictionaries
    Each dict is one row of the final dataset
    Source: Ryan Baumann

    :param f: A .gpx file name with an activity described
    :type f: A .gpx file name

    :return points2: A list of dictionaries containing 'Elevation', 'Latitude', 'Longitude'
    and 'Timestamp' for each .gpx file
    :type points2: A list of dictionaries
    """
    
    points2 = []
    with open(f, 'r') as gpxfile:
        gpx = gpxpy.parse(gpxfile)
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    dict = {'Timestamp' : point.time,
                            'Latitude' : point.latitude,
                            'Longitude' : point.longitude,
                            'Elevation' : point.elevation
                            }
                    points2.append(dict)
    return points2

## Parse the gpx files into a pandas dataframe
files = os.listdir(INDIR)
my_data = pd.concat([pd.DataFrame(parsegpx(INDIR + '\\' + f)) for f in files], keys=files)

## Ensure index is part of data frame
my_data = my_data.reset_index()
my_data = my_data.rename(columns={ my_data.columns[0]: "Name", my_data.columns[1]: "ID" })

## Now calculate distance between points using Haversine distance
def haversine_np(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)

    All args must be of equal length

    :param lon1, lon2: Longitude of two locations
    :type lon1, lon2: Numeric

    :param lat1, lat2: Latitude of two locations
    :type lat1, lat2: Numeric

    :return km: Distance between two points in kilometres
    :type km: Numeric

    """
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2

    c = 2 * np.arcsin(np.sqrt(a))
    km = 6367 * c
    return km

my_data['dist_between_points'] = haversine_np(my_data.Longitude.shift(), my_data.Latitude.shift(), my_data.ix[1:, 'Longitude'], my_data.ix[1:, 'Latitude'])
## Ensure distance between points is reset at the start of each activity
my_data['dist_between_points'] = np.where(my_data['ID']==0, 0, my_data['dist_between_points'])

def add_attributes(df):
    """
    Add the following attributes to the data frame:
    - Type of activity (ride or run)
    - Track number (numbering of each activity sequentially)
    - Cumulative distance (distance cycled or run for each activity)
    - Time taken to ride / run between each point (setting time to zero if it has taken >3 minutes
    between points as I am likely to have stopped Strava (eg. at a cafe or pretty view))
    - Cumulative time for each activity

    :param df: An input data frame with column names 'dist_between_points', 'Timestamp' and 'Name' at least
    :type: df: Pandas data frame

    :return df: Data frame containing additional columns 'Type', 'Track_number', 'cum_dist',
    'segment_time' and 'cum_time'
    :type df: Pandas data frame

    """

    ## Add the type of activity ie. Ride or Run. I only ride or run
    df['Type'] = np.where(df['Name'].str.contains("Ride"), "Ride", "Run")
    
    ## Create a track number for each activity
    df['Track_number'] = pd.factorize(df.Name)[0]+1
    
    ## Calculate cumulative distance
    df['cum_dist']=df.groupby('Track_number')['dist_between_points'].transform(pd.Series.cumsum)
    
    ## Calculate time between points
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df['segment_time'] = df['Timestamp'] - df['Timestamp'].shift(1)
    
    ## Set segment_time to zero at the start of the ride / run or
    ## where segment_time > 3 minutes (where I am likely to have stopped Strava or stopped at a cafe)
    df['segment_time'] = np.where(df['ID']==0, 0, df['segment_time'])
    df['segment_time'] = np.where(df['segment_time'] / np.timedelta64(1, 's') > 60*3, 0, df['segment_time'])
    
    ## Calculate cumulative time over tracks
    df['cum_time']=df.groupby('Track_number')['segment_time'].transform(pd.Series.cumsum)
    
    return df

my_data = add_attributes(my_data)

## Write the data out to a CSV file
my_data.to_csv(OUTDIR + '\\rides.csv')
