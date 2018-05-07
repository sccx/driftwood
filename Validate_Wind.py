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
    
smkf_july = []
for i in range(0, 31):
    smkf_july.append(mlrf.loc[(mlrf['date'].dt.month==07) & (smkf['date'].dt.day==i)])   
    
print('Done')

# Get the mean direction for each day of the month:
mlrf_daily_means = []
for i in range(0,31):
    mlrf_daily_means.append(mlrf_july[i]['direction'].mean())

smkf_daily_means = []
for i in range(0,31):
    smkf_daily_means.append(smkf_july[i]['direction'].mean())

plt.plot(mlrf_daily_means)
plt.plot(smkf_daily_means)

'''
import matplotlib.pyplot as plt
plt.plot([1,2,3,4])
plt.ylabel('some numbers')
plt.show()

ax = df[['V1','V2']].plot(kind='bar', title ="V comp", figsize=(15, 10), legend=True, fontsize=12)
ax.set_xlabel("Hour", fontsize=12)
ax.set_ylabel("V", fontsize=12)
plt.show()
'''

#plot_windrose(mlrf_july, kind='box', bins=np.arange(0.01,20,1), cmap=cm.GnBu_r, lw=5) # can use kind='pdf' for probability density function

'''
    mlrf_july_means[i] = mlrf_july[i]['direction'].mean()
'''















