#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 10 11:10:30 2018

@author: sccx
"""

import pandas as pd
import matplotlib.pyplot as plt

pd.options.display.float_format = '{:,.2f}'.format

path = '/Users/sccx/Dropbox/seancox/PrevailingWind_Project/WorkingData/'

# Buoys
mlrf = pd.read_table(path + 'MLRF1_CF_1992_2014.txt', delimiter='\t', names=['date', 'time', 'direction', 'speed'])
smkf = pd.read_table(path + 'SMKF1_CF_1992_2014.txt', delimiter='\t', names=['date', 'time', 'direction', 'speed'])

# Mean, standard deviation, 
mlrf_mean, smkf_mean = mlrf['direction'].mean(), smkf['direction'].mean()
print('The mean wind directions at MLRF1 and SMKF1 during the 1992-2014 period are: %.1f and %.1f, respectively.' % ( mlrf_mean, smkf_mean))
print('Other relevant data for MLRF1:' )
print(mlrf.describe())

print('Other relevant data for SMKF1:' )
print(smkf.describe())


mlrf['date'] = pd.to_datetime(mlrf['date']) 
smkf['date'] = pd.to_datetime(smkf['date']) 



mlrf_july = []
mlrf_daily_means = []
smkf_july = []
smkf_daily_means = []

for i in range(0, 31):
    mlrf_july.append(mlrf.loc[(mlrf['date'].dt.month==07) & (mlrf['date'].dt.day==i)])
    smkf_july.append(mlrf.loc[(mlrf['date'].dt.month==07) & (smkf['date'].dt.day==i)])   
    mlrf_daily_means.append(mlrf_july[i]['direction'].mean())
    smkf_daily_means.append(smkf_july[i]['direction'].mean())

print('Done')

plt.plot(mlrf_daily_means)
plt.plot(smkf_daily_means)















