#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed May 16 19:12:24 2018

@author: sccx
"""


import pandas as pd
import numpy as np
import os
import glob
from scipy.stats import circmean

'''
To prepare the data, all the extra spaces need to be removed. 
This was done with remove_spaces.py

The code below is adapted from: http://jonathansoma.com/lede/foundations-2017/classes/working-with-many-files/class/
I lays out a path to loading data from multiple text files into a Pandas dataframe.

Load data –> concatenate (axis=0 stacks vertically, axis=1 stacks adjacent, stacking in 3D may not matter/be possible) -->
do any statistical analysis, it does not matter what --> produce a data set for the simulator --> integrate it
'''


path = '/Users/sccx/Dropbox/seancox/PrevailingWind_Project/DataSources/MLRF1/MLRF1_Clean/'

filenames = glob.glob(path + "*.txt")

fnames = [os.path.basename(x) for x in glob.glob(path + '*.txt')]

#list_of_dfs = [pd.read_table(filename) for filename in filenames]
list_of_dfs = [pd.read_table(filename, delimiter=' ') for filename in filenames]


for dataframe, fname in zip(list_of_dfs, fnames):
    dataframe['filename'] = fname

combined_df = pd.concat(list_of_dfs, axis=0, ignore_index=True)


# Clean the data

# Rename problematic columns; In this case, the '#' prior to certain year column names
combined_df.columns = combined_df.columns.str.replace('#YY', 'YYY')
df = combined_df.copy()

#Remove unnecessary columns
drop_columns = ['GDR','GMN','GSP','GST','GTIME']
df.drop(drop_columns, inplace=True, axis=1)

#%%

# find an indexed row with: df.loc[row#,column_name]
#

year_cols = ['YY','YYY','YYYY']

df['year'] = df[year_cols].sum(1)
df['month'] = df['MM']
df['day'] = df['DD']
df['hour'] = df['hh']
df['minutes'] = df['mm']


wind_cols = ['DIR','WDIR']
df['bearing'] = df[wind_cols].sum(1)

spd_cols = ['SPD','WSPD']
df['speed'] = df[spd_cols].sum(1)

df = df.drop(year_cols, 1)
df = df.drop(wind_cols, 1)
df = df.drop(spd_cols, 1)
df = df.drop('MM', 1)
df = df.drop('DD', 1)
df = df.drop('mm', 1)
df = df.drop('hh', 1)

df = df[['year', 'month', 'day', 'hour', 'minutes', 'bearing', 'speed', 'filename']]
df = df.drop_duplicates()

df2 = df.copy()

# Add 1900 to year column for two-digit years
mask = df2['year'] <= 99
df2.loc[mask, 'year'] = df2.loc[mask, 'year'] + 1900

#%%

# Clean out bearing = 999.0 and speed = 99.0
df3 = df2.loc[df2.bearing != 999]
df4 = df3.loc[df3.speed != 99]

#%%
# Description of the data for each day in July

july = []
i = 0
while i <= 31:
   july.append(df4[(df4.month == 7) & (df4.day == i)].describe())
   i += 1

#%%
# Creatine Dataframe of 10-minute slices of specified days in July
#df5[(df5.month == 7) & (df5.day == 14) & (df5.hour == 6) & (df5.minutes == 0)].describe()

df5 = df4[(df4.month == 7)].copy()


#%%
bearing_10_minutes = []
speed_10_minutes = []


'''
df5.speed[(df5.month == 7) & (df5.day == 14) & (df5.hour == 0) & (df5.minutes == 00)].mean()
Out[61]: 3.8476190476190473

df5.bearing[(df5.month == 7) & (df5.day == 14) & (df5.hour == 0) & (df5.minutes == 00)].mean()
Out[62]: 154.0952380952381
'''


for day_slice in range(14, 16, 1):
    for hour_slice in range(0,23,1):
        for minute_slice in range(0,60,10):
            # Get the circle mean
            bearing_10_minutes.append(circmean(df5.bearing[(df5.day == day_slice) & (df5.hour == hour_slice) & (df5.minutes == minute_slice)], high= (df5.bearing[(df5.day == day_slice) & (df5.hour == hour_slice) & (df5.minutes == minute_slice)].max()), low= df5.bearing[(df5.day == day_slice) & (df5.hour == hour_slice) & (df5.minutes == minute_slice)].min()).round()
            # Get the mean speed
            #speed_10_minutes.append(df5.speed[(df5.day == day_slice) & (df5.hour == hour_slice) & (df5.minutes == minute_slice)], ignore_index=True)
            
            #speed_10_minutes.append(df5.speed[(df5.month == 7) & (df5.day == day_slice) & (df5.hour == hour_slice) & (df5.minutes == minute_slice)].mean()
            #bearing_10_minutes.append(df5.bearing[(df5.month == 7) & (df5.day == day_slice) & (df5.hour == hour_slice) & (df5.minutes == minute_slice)].mean()




#%%
# Compute vectors from bearing/speed readings, store in new dataframe
# Requires solving the average angle problem, as published here:
# "Statistics On Spheres", Geoffrey S. Watson, University of Arkansas Lecture
# Notes in the Mathematical Sciences, 1983 John Wiley & Sons, Inc.
# a = arctan(sum_i_from_1_to_N sin(a[i]) / sum_i_from_1_to_N cos(a[i]))

# Or, just do it with scipy...

'''
from scipy.stats import circmean
circmean(df5.bearing[(df5.day == 14) & (df5.hour == 0) & (df5.minutes == 00)], high= (df5.bearing[(df5.day == 14) & (df5.hour == 0) & (df5.minutes == 00)].max()), low= (df5.bearing[(df5.day == 14) & (df5.hour == 0) & (df5.minutes == 00)].min())).round()

'''


                                                      