#!/usr/bin/python3

import numpy as np
import csv
from matplotlib import pyplot as plt
#import matplotlib.patches as mpatches
#import matplotlib.lines as mlines
from scipy.stats import linregress


#filename = 'output.csv'
#filename = 'des_0/des_0_rand_f5t20.csv'
#filename = 'IF70_lowSR/IF70_lowSR.csv'
filename = 'IF50/IF50.csv'

with open(filename) as f:
    reader = csv.reader(f)
    next(reader)

    #IF=[]
    SR=[]
    #XI=[]
    FR=[]

    for row in reader:
        #IF.append(float(row[0]))
        SR.append(float(row[0]))
        #XI.append(float(row[1]))
        FR.append(float(row[3]))

f.close()

res = linregress(SR, FR)
a = res.slope
#a=round(a,4)
b = res.intercept
#b = round(b,4)

a_err = res.stderr
#a_err = round(a_err,4)
b_err = res.intercept_stderr
#b_err = round(b_err,4)

x = np.linspace(min(SR),max(SR),1000)
y = a*x + b

plt.plot(SR, FR, 'o', color = 'violet', label = 'Dados Amostrais')
#plt.plot(x, y, '--k', label=f'Reta Ajustada: freq(SRLoad) = {a:.4f}SRLoad + {b:.4f}')
#plt.plot(x, y, '--k', label=f'Reta Ajustada: freq(SRLoad) = {a:}SRLoad + {b:}')
plt.plot(x, y, '--k', label=f'Reta Ajustada: y = ax + b\n a = {a:.4f} $\pm$ {a_err:.4f}\n b = {b:.4f} $\pm$ {b_err:.4f}')
plt.xlabel("$SR_{Load}$")
#plt.xlabel("$\\xi$")
plt.ylabel("Freq($SR_{Load}$)")
#plt.ylabel("Freq($\\xi$)")
plt.title('Relação entre frequência e ruído')
#plt.title('Relação entre frequência e taxa de amortecimento')
plt.legend()
plt.savefig('Graphics/freqSRForIF50.png')
#plt.show()




#colors=[]
#shapes=[]

#size = len(IF)

#for i in range(0,size):
    #if (IF[i] == 0):
        #colors.append('red')
    #elif (IF[i] == 10):
        #colors.append('green')
    #elif (IF[i] == 30):
        #colors.append('blue')
    #elif (IF[i] == 50):
        #colors.append('purple')
    #elif (IF[i] == 70):
        #colors.append('violet')

#for j in range(0,size):
    #if (SR[j] == 5):
        #shapes.append('^')
    #elif (SR[j] == 15):
        #shapes.append('s')
    #elif (SR[j] == 20):
        #shapes.append('o')

# Criando o gráfico
#fig, ax = plt.subplots()

# Plotando os pontos com diferentes símbolos
#for i in range(size):
    #ax.scatter(XI[i], FR[i], marker=shapes[i], color=colors[i])

# Adicionando rótulos e título
#ax.set_xlabel('Taxa de amortecimento (%)')
#ax.set_ylabel('Frequência (Hz)')
#ax.set_title('Relação entre frequência e taxa de amortecimento')

#red_patch = mpatches.Patch(color='red', label='IF(%) = 0')
#green_patch = mpatches.Patch(color='green', label='IF(%) = 10')
#blue_patch = mpatches.Patch(color='blue', label='IF(%) = 30')
#purple_patch = mpatches.Patch(color='purple', label='IF(%) = 50')
#violet_patch = mpatches.Patch(color='violet', label='IF(%) = 70')


#tri_line = mlines.Line2D([], [], color='black', marker='^', label = 'SR(%) = 5')
#squ_line = mlines.Line2D([], [], color='black', marker='s', label = 'SR(%) = 15')
#cir_line = mlines.Line2D([], [], color='black', marker='o', label = 'SR(%) = 20')

#tri_patch = mpatches.Patch(marker='^', label='SR(%) = 5')

#ax.legend(handles=[red_patch, green_patch, blue_patch, purple_patch, violet_patch, tri_line, squ_line, cir_line],loc='upper left')

# Salvando gŕafico
#plt.savefig('Graphics/freqDumpForBanlaced.png')
# Mostrando o gráfico
#plt.show()



