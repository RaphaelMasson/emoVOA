#!/usr/bin/python3

import numpy as np
import csv
import statistics as st
from matplotlib import pyplot as plt
import filenames
import functions

filenames = filenames.filenames
#size = len(filenames)

#Dados para a planilha
s=[]
#s.append(['IF(%)','S_Rload(%)','Amortecimento (%)','Std.Dev','Freq. (HZ)','Std.Dev'])
s.append(['S_Rload(%)','Amortecimento (%)','Std.Dev','Freq. (HZ)','Std.Dev'])
#s.append(['S_Rload(%)','Amortecimento (%)','Freq. (HZ)'])
#IF=['0','0','0','10','10','10','30','30','30','50','50','50','70','70','70']
#S_Rload=['5','15','20','5','15','20','5','15','20','5','15','20','5','15','20']
S_Rload = np.linspace(1,10,10)
#S_Rload = np.linspace(0.5,10,20)
S_Rload = S_Rload.tolist()
p = 300

functions.Caution()

#for j in range(0,size):
for j in range(0,10):
    #Vfreq = [None]*50
    Vfreq = [None]*10
    #Vfreq = [None]*20
    #Vxi = [None]*50
    Vxi = [None]*10
    #Vxi = [None]*20
    #for i in range(0,50):
    for i in range(0,10):
        x, t = functions.Read_Filenamei(filenames[j],i)
        sigma, freq, amp, fase, xi, MSE = functions.PronyPlusVOA(p, x, t)
        Vxi[i] = xi
        Vfreq[i] = freq         
        
            
        functions.PrintValuesi(filenames[j], amp, freq, fase, sigma, xi, MSE, i) 
               
        
    medfreq = st.mean(Vfreq)
    medfreq = round(medfreq,4)
    desfreq = st.stdev(Vfreq)
    desfreq = round(desfreq,4)
    
    medxi = st.mean(Vxi)
    medxi = round(medxi,4)
    desxi = st.stdev(Vxi)
    desxi = round(desxi,4)
    
    #s.append([str(IF[j]),str(S_Rload[j]),str(medxi),str(desxi),str(medfreq),str(desfreq)])
    s.append([str(S_Rload[j]),str(medxi),str(desxi),str(medfreq),str(desfreq)])
    
myFile=open('IF50/IF50.csv','w')
with myFile:
    writer=csv.writer(myFile)
    writer.writerows(s)
    
    