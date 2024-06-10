#!/usr/bin/python3

import numpy as np
import csv
import statistics as st
from matplotlib import pyplot as plt
import filenames
import functions

#filenames = filenames.filenames
#size = len(filenames)
filename = 'des0_rand5.csv'
sr = 5
    
x, t = functions.Read_Filename20(filename)
sigma, freq, amp, fase, xi, MSE = functions.PronyPlusVOA(x, t)
freq = round(freq,4)
xi = round(xi,4)
print("Frequência sem filtro: ",freq)
print("Taxa de amortecimento sem filtro: ", xi)
print("\n")
a = -0.0015
b = 2.5501
freq, xi = functions.FilterSR(a, b, sr, freq)
freq = round(freq,4)
xi = round(xi,4)
print("Frequência com filtro: ",freq)
print("Taxa de amortecimento com filtro: ", xi)
#print("\n")



        
    
    
