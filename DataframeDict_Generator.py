"""
Created on Wed Feb  6 19:48:26 2019

@author: sccx
"""
import os
import numpy as np
import pandas as pd
from scipy.stats import circmean


class FormatWindInDictionary:
    """
        Organize and clean NOAA wind data to be used in the simulation.
        Returns: Pandas dataframe of wind data
    """

    def __init__(self, wind_folder_name=None):
        self.wind_folder_name = wind_folder_name

    def get_filenames(self):
        """
            Returns: all txt files in wind_folder_name subdir of wherever file is located
        """
        f_dir = os.path.join(os.path.dirname(__file__), self.wind_folder_name)
        fns = [os.path.join(f_dir, t) for t in os.listdir(f_dir) if
               os.path.isfile(os.path.join(f_dir, t)) and t.endswith(".txt")]
        if len(fns) > 0:
            return fns
        else:
            print('No txt files in current directory.')
            return False

    def create_dataframe(self):
        """
            Returns: dataframe with extra filename column
        """
        fns = self.get_filenames()
        if fns:
            dfs = [pd.read_table(f, delimiter=' ') for f in fns]
        if dfs:
            for dataframe, filename in zip(dfs, fns):
                dataframe['filename'] = filename
                df = pd.concat(dfs, axis=0, ignore_index=True, sort=False)
            return df
        else:
            return False

    def clean_data(self, dataframe):
        '''
            The data sets have been combined and are next cleaned.
            Extraneous data are removed and columns renamed.
            Returns: standardized dataframe
        '''
        # Rename columns
        year_cols = dataframe.filter(like='YY').columns
        dataframe['year'] = dataframe[year_cols].sum(1)
        wind_direction_columns = dataframe.filter(like='DIR').columns
        dataframe['direction'] = dataframe[wind_direction_columns].sum(1)
        wind_speed_columns = dataframe.filter(like='SPD').columns
        dataframe['speed'] = dataframe[wind_speed_columns].sum(1)
        dataframe.rename(columns={'MM': 'month', 'DD': 'day',
                                  'hh': 'hour', 'mm': 'minutes'}, inplace=True)

        # Drop columns
        poison_columns = ['GDR', 'GMN', 'GSP', 'GST', 'GTIME',
                          wind_speed_columns[0], wind_direction_columns[0]]
        dataframe.drop(poison_columns, inplace=True, axis=1)

        # Specify new column names
        dataframe = dataframe[['year', 'month', 'day', 'hour',
                               'minutes', 'direction', 'speed', 'filename']]
        dataframe = dataframe.drop_duplicates()

        # Add 1900 to year column to make all years four digits
        mask = dataframe['year'] <= 99
        dataframe.loc[mask, 'year'] = dataframe.loc[mask, 'year'] + 1900

        # Clean out direction = 999.0 and speed = 99.0
        dataframe = dataframe.loc[dataframe.direction != 999]
        dataframe = dataframe.loc[dataframe.speed != 99]
        return dataframe

    def circular_mean(self, df):
        '''
        Broadcasting Scipy's circmean function on a datafram with 
        aggfunc does not allow space for the 'high' and 'low' parameters, 
        necessary for accurate calculation. This solves that.
        Return: Dataframe with Scipy's circmean function applied to all bearing data.
        '''
        return circmean(df, high=df.max(), low=df.min())


    def three_day_slice(self, df):
        '''
        Receive a dataframe of wind data and return
        3-day slices of the dataframe in a dict.
    
        '''        
        '''
        # THIS IS THE TEST CODE FOR A SINGLE, 3-day slice of wind data
        day = 1
        a_dict = {}
        trimmed_df = df.loc[(day <= df['day']) & (df['day'] < (day + 3))]
        a_dict[day] = trimmed_df.dropna()
        '''
        # Replace above with this code, for the entire month of July
        days = df.day.unique()
        a_dict = {}
        for day in days:
            trimmed_df = df.loc[(day <= df['day']) & (df['day'] < (day + 3))]
            a_dict[day] = trimmed_df.dropna()
        del a_dict[30], a_dict[31]
        return a_dict


    def mean_df_to_dict(self, mean_df):
        '''
            Stacks the dataframes horozontally into a dictionary (making 3D array, with each dictionary key as a 'day')
            Returns dictionary.
        '''
        the_wind = mean_df.copy()
        the_wind.rename(index=str, columns={"direction": "WDIR", "speed": "WSPD"}, inplace=True)
        the_wind = the_wind.reset_index()
        the_wind['day'] = pd.to_numeric(the_wind.day)
        the_wind['hour'] = pd.to_numeric(the_wind.hour)
        the_wind['minutes'] = pd.to_numeric(the_wind.minutes)
        wind_dictionary = self.three_day_slice(the_wind)
        dict_of_wind_dfs = {k: pd.DataFrame(v) for k,v in wind_dictionary.items()}
        return dict_of_wind_dfs
        
        
class RunProcess:
    fw = FormatWindInDictionary(wind_folder_name='WindData')
    df = fw.create_dataframe()
    clean_df = fw.clean_data(df)
    #months = [i for i in range(1, 13)]
    month = 8
    month_df = clean_df.loc[clean_df['month'] == month]
    mean_month = month_df.pivot_table(values=['direction', 'speed'], 
                                      index=['day', 'hour', 'minutes'], 
                                      aggfunc = {'direction': fw.circular_mean, 'speed': np.mean})
    data = fw.mean_df_to_dict(mean_month)



wind_dict = RunProcess
winds = wind_dict.data

