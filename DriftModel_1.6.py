#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 10:43:45 2018

@author: sccx
"""
# 1
import numpy as np
import pandas as pd
#import pprint
from matplotlib import pyplot as plt
from windrose import plot_windrose
import matplotlib.cm as cm


# 2
def point_cloud_generator(number_of_runs):

# 3
    def getEndpoint(lat1,lon1,bearings,float_distance):
        R = 6371 # Radius of Earth, roughly
        distance = float_distance             
        brng = np.deg2rad(bearings) 
        lat1 = np.deg2rad(lat1)    
        lon1 = np.deg2rad(lon1)    
        lat2 = np.arcsin(np.sin(lat1)*np.cos(distance/R) + np.cos(lat1)*np.sin(distance/R)*np.cos(brng))
        lon2 = lon1 + np.arctan2(np.sin(brng)*np.sin(distance/R)*np.cos(lat1),np.cos(distance/R)-np.sin(lat1)*np.sin(lat2))
        lat2 = np.rad2deg(lat2)
        lon2 = np.rad2deg(lon2)
        return lat2,lon2
    
    #%%
    
    # Generate Wind and current vectors (directions and speeds), according to weighted probabilities
    # Meteorological convention for wind, oceanographic convention for current    

    n1 = range(338, 361, 1)
    n2 = range(1, 23, 1)
    ne = range(23, 68, 1)
    e = range(68, 113, 1)
    se = range(113, 158, 1)
    s = range(158, 203, 1)
    sw = range(203, 248, 1)
    w = range(248, 293, 1)
    nw = range(293, 338, 1)  

# Find the probabilities with non_random.py

    n1_prob1 = 2
    n2_prob1 = 2
    ne_prob1 = 2
    e_prob1 = 4
    se_prob1 = 80
    s_prob1 = 4
    sw_prob1 = 2
    w_prob1 = 2
    nw_prob1 = 2

    n1_prob2 = 2
    n2_prob2 = 2
    ne_prob2 = 2
    e_prob2 = 40
    se_prob2 = 40
    s_prob2 = 4
    sw_prob2 = 2
    w_prob2 = 2
    nw_prob2 = 2

# 4

    # Each range of integers appears in the list a weighted number of times.

    weighted_wd1 = (n1 * n1_prob1) + (n2 * n2_prob1) + (ne * ne_prob1) + (e * e_prob1) + (se * se_prob1) + (s * s_prob1) + (sw * sw_prob1) + (w * w_prob1) + (nw * nw_prob1)
    weighted_wd2 = (n1 * n1_prob2) + (n2 * n2_prob2) + (ne * ne_prob2) + (e * e_prob2) + (se * se_prob2) + (s * s_prob2) + (sw * sw_prob2) + (w * w_prob2) + (nw * nw_prob2)
    #weighted_wd = range(1, 82, 1) * 50 + range(82, 119, 1) * 25 + range(119, 193, 1) * 15 + range(193, 361, 1) * 10 # Meteorological convention
    weighted_ws1 = range(0, 801, 1) * 65 + range(801, 1501, 1) * 20 + range(1501, 2001, 1) * 12 + range(2001, 10000, 1) * 3  # cm/second
    weighted_ws2 = range(0, 801, 1) * 65 + range(801, 1501, 1) * 20 + range(1501, 2001, 1) * 12 + range(2001, 10000, 1) * 3  # cm/second

    weighted_cd = range(0, 46, 1) * 35 + range(46, 91, 1) * 35 + range(340, 360, 1) * 30 # Oceanographic convention
    weighted_cs = range(60, 101, 1) # cm/second

# 5
    # Randomly select from weighted variables according to number of total_steps
    total_steps = 432  # Each step is 10 minutes (600 seconds)

    # Wind data (two wind vectors, one each from the SMKF1 and MLRF1 buoys)
    random_wd1 = np.random.choice(weighted_wd1, total_steps)
    random_ws1 = np.random.choice(weighted_ws1, total_steps)
    final_ws1 = (random_ws1 + 0.) / 100 # Speeds now in meters/sec

    plot_df1 = pd.DataFrame({'speed': final_ws1, 'direction': random_wd1})
    plot_windrose(plot_df1, kind='box', bins=np.arange(0.01,20,1), cmap=cm.GnBu_r, lw=5) # can use kind='pdf' for probability density function

    random_wd2 = np.random.choice(weighted_wd2, total_steps)
    random_ws2 = np.random.choice(weighted_ws2, total_steps)
    final_ws2 = (random_ws2 + 0.) / 100 # Speeds now in meters/sec

    plot_df2 = pd.DataFrame({'speed': final_ws2, 'direction': random_wd2})
    plot_windrose(plot_df2, kind='box', bins=np.arange(0.01,20,1), cmap=cm.GnBu_r, lw=5) # can use kind='pdf' for probability density function

    # Ocean current data
    random_cd = np.random.choice(weighted_cd, total_steps)
    random_cs = np.random.choice(weighted_cs, total_steps)
    final_cs = (random_cs + 0.) / 100 # Speeds now in meters/sec

    # Build data array of all directions and speeds
    my_data = np.stack((random_wd1, final_ws1, random_wd2, final_ws2, random_cd, final_cs), axis=1)
    #print("Random selection of 10 weighted variables for wind and current direction and speed, in array (my_data): ")
    #pprint.pprint(my_data)

    # Backup data
    data_copy = my_data.copy()


    phi1 = -data_copy[:,0] - 90 # DO I SUBTRACT 90?
    u_wd1 = data_copy[:,1] * np.cos(np.deg2rad(phi1))
    v_wd1 = data_copy[:,1] * np.sin(np.deg2rad(phi1))

    phi2 = -data_copy[:,2] - 90 # DO I SUBTRACT 90?
    u_wd2 = data_copy[:,3] * np.cos(np.deg2rad(phi2))
    v_wd2 = data_copy[:,3] * np.sin(np.deg2rad(phi2))


    # Ocean u/v vector components, with bearing degrees converted to radians
    theta = 90 - data_copy[:,4]
    u_cur = data_copy[:,5] * np.cos(np.deg2rad(theta))
    v_cur = data_copy[:,5] * np.sin(np.deg2rad(theta))


    # Create array of wind and ocean U and V vectors
    uv_stack = np.stack((u_wd1, v_wd1, u_wd2, v_wd2, u_cur, v_cur), axis=1)

    #print("U/V wind and current vector array (uv_stack): ")
    #pprint.pprint(uv_stack)
# 7  
    # Calculate the final vectors
    U_vector = uv_stack[:,0] + uv_stack[:,2] + uv_stack[:,4]
    V_vector = uv_stack[:,1] + uv_stack[:,3] + uv_stack[:,5]
    vector_stack = np.stack((U_vector, V_vector), axis=1)

    #print("Summed U/V vector array (vector_stack): ")
    #pprint.pprint(vector_stack)

    bearings = (90 - np.arctan2(vector_stack[:,1], vector_stack[:,0]) * 180/np.pi) % 360 # Radians converted to degrees with 180/pi, returns bearing on unit circle
    speeds = np.sqrt(vector_stack[:,0] ** 2, vector_stack[:,1] ** 2)
    #route = np.stack((bearings, speeds), axis=1) # ADD 180 to the bearing, without exceeding 360..?
    #print("This is the route and the speed for each step in the series (route):")
    #pprint.pprint(route)
    # mean_bearing = np.mean(route, axis=0)
    # print "The mean direction and speed of the vector are (unit circle degrees, meters/sec): ", mean_bearing
    
    #%%
# 8 Almiranta,24.81055,-80.76553333
   
    (start_lat, start_lon) = 24.81055, -80.76553333
    
    lat1 = float(start_lat)
    lon1 = float(start_lon)
    # print "Starting latitude and longitude: ", lat1, lon1
    
# 9 Calculate the distance the object floats each step using the speed,time, and drag.
    density = 550 # kg/m**3, hypothetical object density. Use Archimedes principle: http://www.dummies.com/education/science/physics/understanding-buoyancy-using-archimedess-principle/
    refarea = 3.6 # approximate area of object (meters?)
    drag_coeff = 0.09 # drag coefficient
    drag = (((density * (speeds ** 2)) / 2) * drag_coeff * refarea)
    travel_time = 600 # seconds (10 minutes), or 0.166 hours
    float_distance = (speeds * travel_time) / (drag * travel_time)
    
    (newlat, newlon) = getEndpoint(lat1, lon1, bearings[0], float_distance)
    course = np.stack((newlat, newlon), axis = 1)
    date_rng = pd.date_range('1/1/1733', periods=total_steps, freq='10Min')
    course = np.insert(course, 2, date_rng, axis=1)
    
    # print "The object follows this course: "
    # print(course)   
    # Export results, then plot...
    # plt.scatter(newlat, newlon)
    return course

# 10  
number_of_runs = 5
data_list = []
for i in range(number_of_runs):
    data_list.append(point_cloud_generator(number_of_runs))
my_points = np.asarray(data_list)

pointcloud = np.vstack(my_points)
np.savetxt('pointcloud.txt', pointcloud, ('%5.8f'))

# Ways to format datetime/supress scientific notation (that aren't working):
# pd.options.display.float_format = '{:.2f}'.format
# pd.to_datetime(date_rng)


#To help validate the direction of drift

cloud = pointcloud
y = cloud[::1,0]
x = cloud[::1,1]
plt.scatter(x, y)




'''
NEXT STEPS
- Turn the ranges into variables that the user can input... maybe
- Store a list of the shipwrecks and iterate a point cloud for each
    each debris field. Then, output the results to a dedicated, comma
    separated text file: FIND: (\s\-) REPLACE: ,\1

You should make a column of absolute windspeed (sqrt(u_ms^2 + v_ms^2)) 
and take atan2(u_ms/wind_abs, v_ms/wind_abs). 
(also note that atan2 takes y component first - 
make sure that's what you want)

wind_abs = np.sqrt((u_wd[0]**2) + (v_wd[0]**2))
wind_dir_trig = np.atan2(u_wd/wind_abs, v_wd/wind_abs)
wind_dir_degrees = wind_dir_trig * 180/np.pi
'''
