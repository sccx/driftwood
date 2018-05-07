#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat May  5 11:17:47 2018

@author: sccx
"""
'''
Developed for converting coordinates from decimal degree minutes
into decimal degrees. The output from the numpy.savetext function
is in scientific notation, so I just copied the 'ships' array and 
used regexes in Textwrangler to clean it up. Sometimes, it's possible
to take a five-minute problem and turn it into a four-hour adventure.
'''

import pandas as pd
import numpy

path = 'path'
filename = 'filename'


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

