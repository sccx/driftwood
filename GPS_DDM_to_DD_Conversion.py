#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat May  5 11:17:47 2018

@author: sccx
"""


import pandas as pd
import numpy

path = '/Users/sccx/Dropbox/seancox/PrevailingWind_Project/DataSources/'
filename = 'Shipwreck_Coordinates.txt'


data = pd.read_csv(path + filename, sep=",", header=None)
data.columns = ["Ship", "Degrees_Lat", "Decimal_Min_Lat", "Degrees_Long", "Decimal_Min_Long"]
ship_GPS = pd.DataFrame(data)

ship_GPS['Degrees_Lat'] = ship_GPS['Degrees_Lat'].astype(float)
ship_GPS['Decimal_Min_Lat'] = ship_GPS['Decimal_Min_Lat'].astype(float)
ship_GPS['Degrees_Long'] = ship_GPS['Degrees_Long'].astype(float)
ship_GPS['Decimal_Min_Long'] = ship_GPS['Decimal_Min_Long'].astype(float)

ship_lats = (ship_GPS['Degrees_Lat'] + (ship_GPS['Decimal_Min_Lat'] / 60))
ship_longs = (ship_GPS['Degrees_Long'] + (ship_GPS['Decimal_Min_Long'] / 60))
ship_names = ship_GPS['Ship']

ships = numpy.column_stack((ship_names, ship_lats, ship_longs))
fmt='%s, %.6e, %.6e'
numpy.savetxt('ship_coordinates.txt', ships, fmt=fmt, delimiter=' ')

#ship_coords = pd.DataFrame(data2)