#!/usr/bin/python3

import numpy as np
import csv
#import statistics as st
#from matplotlib import pyplot as plt
#import des_0_filenames
import functions

filename = 'TestandoRuidos/' + 'des_70_rand_5.csv'
x, t = functions.ReadFilename(filename)
p=300
sigma, freq, amp, fase, xi, MSE = functions.PronyPlusVOA(p, x, t)
functions.PrintValues(filename, amp, freq, fase, sigma, xi, MSE)
#print(sigma)
#print(freq)
#print(amp)
#print(fase)
#print(MSE)
