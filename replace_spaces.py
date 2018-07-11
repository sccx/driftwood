#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed May 16 19:06:47 2018

@author: sccx
"""

'''
Use os.walk to open files in a directory and apply pattern
to find and replace unwanted spaces in NOAA data.

Taken from: https://stackoverflow.com/questions/4205854/python-way-to-recursively-find-and-replace-string-in-text-files
'''


import os, fnmatch
def findReplace(directory, find, replace, filePattern):
    for path, dirs, files in os.walk(os.path.abspath(directory)):
        for filename in fnmatch.filter(files, filePattern):
            filepath = os.path.join(path, filename)
            with open(filepath) as f:
                s = f.read()
            s = s.replace(find, replace)
            with open(filepath, "w") as f:
                f.write(s)

path = 'PATH HERE'
spaces = '  '
one_space = ' '

i = 0

# The NOAA data is delimited with various numbers of spaces. At this stage, the 
# quickest way to solve this was to simply run the space finder four times.
# This seems to fix the space issue, but another solution that simply checks until
# no more extraneous spaces exist in any files in the directory is preferable.

while i <= 4:
    findReplace(path, spaces, one_space, "*.txt")
    i += 1

print("Data processed.")