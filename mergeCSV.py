#!/usr/bin/python3

import filenames
import functions
import csv
import numpy as np

filenames = filenames.filenames

X = [None]*10
for i in range(0,10):
    filename = filenames[i]
    x = functions.ReadFileX(filename)
    X[i] = x
    
M = functions.FromArray2DtoMatrix(X)
    
#output = filenames.output
myFile=open('IF50/des_50_rand_10.csv','w')
with myFile:
    writer=csv.writer(myFile)
    writer.writerows(M)