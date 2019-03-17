#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 20 17:59:59 2019

@author: sccx
"""

import pandas as pd
import numpy as np # I stick with Numpy here for the 'where' method.



class CompileWindOceanLee:
    '''
        Take the wind data, generates constant ocean current, and computes leeway drift, then compile into dataframe.
        Returns datafame.
    '''
    
    def __init__(self):
        print("CompileWindOceanLee is defined")
    
    def leeway_drift(self, leeway_to_wind_ratio, wind_conditions):
        ''' (float)(dataframe)-> (float)
        Calculates the leeway drift distance in centimeters of an object for a 10-minute slice of a
        wind dataframe.
    
        Returns a float, representing centimeters traveled during the 10-minute step.
        '''
        #leeway_speed = (leeway_to_wind_ratio * wind_conditions.WSPD) / 100 # meters/sec
        leeway_speed = (leeway_to_wind_ratio * wind_conditions.WSPD) # in cm/s # 600 second in 10 minutes
        wind_conditions['LSPD'] = pd.Series(leeway_speed, index=wind_conditions.index)
        return wind_conditions
    
    def ocean_current(self, lengh_of_wind_df):
        '''
        'Effects of low-frequencycurrent variability on near-inertial submesoscale vortices'
        Lynn K. Shay,Tom N. Lee, and Elizabeth J. Williams
    
        https://agupubs.onlinelibrary.wiley.com/doi/pdf/10.1029/98JC01007
    
        '''
        ocean_bearing = np.random.randint(39,51,size=(lengh_of_wind_df, 1))
        ocean_flow_rate = np.random.randint(20,40,size=(lengh_of_wind_df, 1))
        return ocean_bearing, (ocean_flow_rate / 100) # division by 100 to arrive at meters/sec
    
    
    def apply_mask(self, df):
        '''
        Applies a mask to the elements of a datafram, in the assigned ratio. Here, masks are applied to
        10% of the dataframe:5% for a left drift, 5% for a right drift.
        '''
        mask_left = (np.random.choice([True, False], size=df['WTRAV'].values.shape, p=[.05, .95]))
        mask_left_verified = df[mask_left]
        mask_right = (np.random.choice([True, False], size=df['WTRAV'].values.shape, p=[.05, .95]))
        mask_right_verified = df[mask_right]
        df.loc[mask_left, 'WCUR'] = mask_left_verified['WTRAV'] - 30
        df.loc[mask_right, 'WCUR'] = mask_right_verified['WTRAV'] + 30
        return df
    
    
    def left_or_right(self, df):
        ''' 
        Wind currents have a 10% chance of pushing an object to the left or the
        right of the leeway direction each hour. This function takes the direction of the wind's
        travel in a dataframe, and 5% of the time directs the wind current to the
        left, and 5% to the right. http://www.glts.org/articles/halpern/the_drift_of_wreckage.html
        '''
        self.apply_mask(df)
        df['WCUR'] = df.apply(lambda df: df['WTRAV'] * 1 if np.isnan(df['WCUR']) else df['WCUR'], axis=1)
        df['WCUR'] = np.where(df['WCUR'] < 0, df['WCUR'] +360, df['WCUR'])
        return df
    
    def load_drift_conditions(self, debris_dict, wind_conditions):
        ''' 
        '''
        density_air = 1.29 #kg m−3
        density_water = 1025 #kg m−3
        drag_coefficient_air = 0.8
        drag_coefficient_water = 1.2
        # drift_objects = {} # This is still empty when it returns.
        i = 1
        for obj in debris_dict:
            leeway_to_wind_ratio = np.sqrt(((density_air * drag_coefficient_air) \
                                            / (density_water * drag_coefficient_water)) \
                                            * ((1 - debris_dict[obj][6]) / debris_dict[obj][6])) \
                                            # debris_dict[obj][6] is the immersion ratio,
                                            # using string key causes type error
            # print('leeway to wind ratio: ', leeway_to_wind_ratio)
            wind_drift = self.leeway_drift(leeway_to_wind_ratio, wind_conditions)
            #print(wind_drift.head().to_string())
            # Combine the wind_DF with the ocean array as two new columns.
            drift_conditions = wind_drift.copy()
            ocean_conditions = self.ocean_current(len(drift_conditions))
            drift_conditions['ODIR'] = ocean_conditions[0]
            drift_conditions['OSPD'] = ocean_conditions[1]
            # Use wind direction to determine the wind current
            # Step 1: invert wind dirction to its direction of travel
            mask = (drift_conditions['WDIR'] <= 180)
            mask_verified = drift_conditions[mask]
            mask2 = (drift_conditions['WDIR'] > 180)
            mask2_verified = drift_conditions[mask2]
            drift_conditions.loc[mask, 'WTRAV'] = mask_verified['WDIR'] + 180
            drift_conditions.loc[mask2, 'WTRAV'] = mask2_verified['WDIR'] - 180
            #print(drift_conditions.head().to_string())
            # Step 2: WDIR +- 30 degrees, via left_or_right function
            # Determine counter for each hour, that allows 10% application of the left_or_right function
            the_drift = self.left_or_right(drift_conditions)
            #print(drift_conditions.head().to_string())
            wind_ocean_lee = the_drift.drop(columns=['WTRAV'])
            i += 1

    
        return wind_ocean_lee 

class CombineVectors:
    '''
       Takes the wind, ocean, and leeway forces—in bearing/speed format in a dictionary, and converts them to vectors.
       Returns dictionary containing dataframes.
    '''        
    def __init__(self):
        print("CombineVectors is defined")

    def vector_math(self, data_df):
        U_Wnd = -data_df['WSPD'] * np.sin(np.deg2rad(data_df['WDIR']))
        V_Wnd = -data_df['WSPD'] * np.cos(np.deg2rad(data_df['WDIR']))
        U_Lee = data_df['LSPD'] * np.sin(np.deg2rad(data_df['LDIR']))
        V_Lee = data_df['LSPD'] * np.cos(np.deg2rad(data_df['LDIR']))
        U_Ocn = data_df['OSPD'] * np.sin(np.deg2rad(data_df['ODIR']))
        V_Ocn = data_df['OSPD'] * np.cos(np.deg2rad(data_df['ODIR']))
        wind_df = pd.concat([U_Wnd, V_Wnd, U_Lee, V_Lee, U_Ocn, V_Ocn], axis=1)
        wind_df.rename(index=str, columns={0:'Wnd_U1', 1:'Wnd_V1', 2:'Lee_U', 3:'Lee_V', 4:'Oc_U', 5:'Oc_V'}, inplace=True)
        return wind_df

#%%

class RunProcess:
    '''
        For now, debris and wind are the result of running Debris_Generator and DataframeDict_Generator, and stored as variables.
    '''
    
    def foo(self, debris, wind_dict):
        wol = CompileWindOceanLee()    
        #data_out = pd.DataFrame()
        for i in range(1, len(wind_dict) + 1):
            temp_df = wol.load_drift_conditions(debris, wind_dict[i])
            wind_dict[i] = temp_df
            wind_dict[i] = wind_dict[i][['WDIR', 'WSPD', 'WCUR', 'LSPD', 'ODIR', 'OSPD']]
            wind_dict[i].rename(index=str, columns={'WCUR': 'LDIR'}, inplace=True)   
        return wind_dict
    
    

#%%

'''
In order for this to work, debris and wind are already in memory,
the result of Debris_Generator and DataframeDict_Generator.

'''
x = RunProcess()
y = x.foo(debris, winds)
#z = x.foo(debris, storm)

vectors = CombineVectors()

v = {}
v2 = {}



for i in range(1, len(y) + 1):
    v[i] = vectors.vector_math(y[i])
    #v[i] = vectors.vector_math(z[i])
    v[i]['U_Sum'] = v[i].iloc[:, 0::2].sum(axis=1)
    v[i]['V_Sum'] = v[i].iloc[:, 1::2].sum(axis=1)
    summed_vectors = v[i].copy()
    summed_vectors.drop(columns=['Wnd_U1','Wnd_V1',
                                 'Lee_U','Lee_V',
                                 'Oc_U','Oc_V'], inplace=True)
    obj_bearing = np.rad2deg(np.arctan2(-summed_vectors['V_Sum'], -summed_vectors['U_Sum'])) 
    obj_bearing.where(obj_bearing >= 0, obj_bearing + 360, inplace=True)
    obj_speed = np.sqrt((summed_vectors['U_Sum']**2) + (summed_vectors['V_Sum']**2))
    v2[i] = pd.DataFrame()
    v2[i]['Bearing'] = obj_bearing.copy()
    v2[i]['Speed'] = obj_speed.copy()
