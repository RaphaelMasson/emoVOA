#!/usr/bin/python3

import csv
import numpy as np

    

def Read_Filename20(filename):
    with open(filename) as f:
        reader = csv.reader(f)
        #next(reader)
        #next(reader)
        #next(reader)
        x=[]
        for row in reader:
            x.append(float(row[0]))

    f.close()

        #Os seguintes comandos tem como objetivo encontrar o primeiro pico
        #e calibrá-lo como o ponto zero

    ipico=x.index(max(x))
    l=len(x)
    x=x[ipico:l]
    N=len(x)
    t=np.linspace(0,(N-1)/10000,N) # Este comando gera um vetor temporal com intervalos de 1 ms.
    t=20*t # O intervalo entre as amostragens dos arquivos csv correspondem à 20 ms.
        
    return x, t

def Read_Filename20i(filename,i):
    with open(filename) as f:
        reader = csv.reader(f)
        #next(reader)
        #next(reader)
        #next(reader)
        x=[]
        for row in reader:
            x.append(float(row[i]))

    f.close()

        #Os seguintes comandos tem como objetivo encontrar o primeiro pico
        #e calibrá-lo como o ponto zero

    ipico=x.index(max(x))
    l=len(x)
    x=x[ipico:l]
    N=len(x)
    t=np.linspace(0,(N-1)/10000,N) # Este comando gera um vetor temporal com intervalos de 1 ms.
    t=20*t # O intervalo entre as amostragens dos arquivos csv correspondem à 20 ms.
        
    return x, t

def Read_Filenamei(filename,i):
    with open(filename) as f:
        reader = csv.reader(f)
        #next(reader)
        #next(reader)
        #next(reader)
        x=[]
        for row in reader:
            x.append(float(row[i]))

    f.close()

        #Os seguintes comandos tem como objetivo encontrar o primeiro pico
        #e calibrá-lo como o ponto zero

    ipico=x.index(max(x))
    l=len(x)
    x=x[ipico:l]
    N=len(x)
    t=np.linspace(0,(N-1)/10000,N) # Este comando gera um vetor temporal com intervalos de 1 ms.

    return x, t    

def Prony(p, x, t):
    T = t[1]-t[0]
    N = len(x)
    MSE = 1
    #p=30
    #p=120
    #p=300
    #Resolução do sistema linear (Ax=b) com as amostras para se obter os
    #coeficientes a[m], m=0,..,p-1
    #Obs: No python, o primeiro índice do vetor é 0.

    #Montando a matriz A e o vetor b:
    
    b=[None]*(N-p)
    A=np.zeros((N-p,p))
    for j in range(0,N-p):
        b[j]=-x[j+p]
        for i in range(p+j-1,-1+j,-1):
            A[j,p+j-1-i]=x[i]

    #Resolvendo o sistema Ax=b e encontramos os coeficientes a[n],
    # n=0,...,p-1
    a=np.dot(np.linalg.pinv(A),b)
    del b,A
    a=a.tolist()

    #Resolvendo o polinômio característico e encontrando as suas raízes
    #z[0],...,z[p-1]
    a.insert(0,1)
    zk=np.roots(a)
    zk=zk.astype(complex)
    #Com o vetor z, obtém-se os valores de amortecimentos e frequências:
    sigma=np.log(abs(zk))/T
    freq=(1/(2*np.pi*T))*np.arctan(zk.imag/zk.real)

    #Resolvendo o sistema Ax=b para encontrar h[0],...h[p-1]
    #Montando a matriz A:
    A=np.zeros((N,p))
    A=A.astype(complex)

    for j in range(0,N):
        for i in range(0,p):
            A[j,i]=(np.conj(zk[i]))**j

    #Montando o vetor b:
    b=[None]*N

    for i in range(0,N):
        b[i]=x[i]
    b=np.asarray(b)

    h=np.dot(np.linalg.pinv(A),b)

    #Obtendo as amplitudes e as fases a partir do vetor h
    amp=abs(h)
    fase=np.arctan((h.imag)/(h.real))

    
    for i in range(0,p):
        amp[i] = 2*amp[i]
    
    
    sinal=[None]*p
    ERRO=[None]*p
    
    for i in range(0,p):
        sinal[i]=amp[i]*np.exp(sigma[i]*t)*np.cos(2*np.pi*freq[i]*t+fase[i])
        ERRO[i] = np.square(np.subtract(x,sinal[i])).mean()
        
    MSE_Prony = min(ERRO)
    
    
    
    
    k=ERRO.index(MSE_Prony)
    
    sigmaProny = sigma[k]
    ampProny = amp[k]
    freqProny = freq[k]
    faseProny = fase[k]
    
    if (freqProny<0):
        freqProny=abs(freqProny)
        faseProny = faseProny*(-1)
    
        
    del sigma, freq, amp, fase
    sigmaProny = round(sigmaProny,4)
    freqProny = round(freqProny,4)
    ampProny = round(ampProny,4)
    faseProny = round(faseProny,4)
    
    
    
    return sigmaProny, freqProny, ampProny, faseProny, MSE_Prony

def VOA(sigma, freq, amp, fase, x, t):
    #O algoritmo genético foi inspirado na replicação viral.
    #Um vírus não precisa de outro para se reproduzir,
    #cada indivíduo gera vários
    #e com uma altíssima ocorrência de mutações.

    #Os parâmetros de amplitude, coeficiente de amortecimento, frequência e fase
    #são análogos a genes.
    
    # Probabilidades de mutação
    pm1=0.1
    pm2=0.8    
    
    # O Erro Quadrático Médio é a função fitness    
    sinal=amp*np.exp(sigma*t)*np.cos(2*np.pi*freq*t+fase)
    MSEgfitness = np.square(np.subtract(x,sinal)).mean()
    
    npop=1000

    sinais=[None]*npop
    MSE=[None]*npop
    Vfreq=[freq]*npop
    Vsigma=[sigma]*npop
    Vamp=[amp]*npop
    Vfase=[fase]*npop
    Vxi=[None]*npop

    REL=1
    #g=0
    k=0

    from random import uniform
    from random import choice

    while (REL>0):

        for i in range(npop):

            if (uniform(0,1)<pm1):
                var1=round(uniform(-0.005,0.005),4)
            elif (uniform(0,1)<pm2):
                var1=choice([-0.0001,0.0001])
            else:
                var1=0

            if (uniform(0,1)<pm1):
                var2=round(uniform(-0.005,0.005),4)
            elif (uniform(0,1)<pm2):
                var2=choice([-0.0001,0.0001])
            else:
                var2=0

            if (uniform(0,1)<pm1):
                var3=round(uniform(-0.005,0.005),4)
            elif (uniform(0,1)<pm2):
                var3=choice([-0.0001,0.0001])
            else:
                var3=0

            if (uniform(0,1)<pm1):
                var4=round(uniform(-0.005,0.005),4)
            elif (uniform(0,1)<pm2):
                var4=choice([-0.0001,0.0001])
            else:
                var4=0

            Vfreq[i]=freq+var1
            Vsigma[i]=sigma+var2
            Vamp[i]=amp+var3
            Vfase[i]=fase+var4

            sinais[i]=Vamp[i]*np.exp(Vsigma[i]*t)*np.cos(2*np.pi*Vfreq[i]*t+Vfase[i])
            MSE[i] = np.square(np.subtract(x,sinais[i])).mean()

        MSElfitness=min(MSE) # Menor erro quadrático médio.
        ibest=MSE.index(min(MSE)) # Índice do menor erro quadrático médio.

        REL=abs(MSEgfitness-MSElfitness)/MSEgfitness

        if(MSElfitness<MSEgfitness):
            MSEgfitness=MSElfitness
            sinal=sinais[ibest]
            freq=Vfreq[ibest]
            sigma=Vsigma[ibest]
            amp=Vamp[ibest]
            fase=Vfase[ibest]
            k=0

        elif(round(MSElfitness,15)==round(MSEgfitness,15)):
            k=k+1
            if (k==10):
                break

        #Amortecimento
        #w=2*np.pi*freq
        #sw=(sigma**2+w**2)**0.5
        #xi=-sigma/sw
        #xi=xi*100
        xi = FromSigma2Xi(freq, sigma)

        #g=g+1
        
        #print("Geração:",g)
        #print("Erro Quadrático Médio:",MSEgfitness)
        #print("Amplitude:",round(amp,4))
        #print("Fase:",round(fase,4))
        #print("Frequência:",round(freq,4))
        #print("Decaimento:",round(sigma,4))
        #print("Amortecimento:",round(xi,4))
        #print("\n")
        
    sigma = round(sigma,4)
    freq = round(freq,4)
    amp = round(amp,4)
    fase = round(fase,4)
    xi = round(xi,4)
        
    return sigma, freq, amp, fase, xi, MSEgfitness

def PronyPlusVOA(p, x, t):
    
    sigma, freq, amp, fase, MSE_Prony = Prony(p, x, t)
    PrintProny(freq, sigma, MSE_Prony)
    sigma, freq, amp, fase, xi, MSE = VOA(sigma, freq, amp, fase, x, t)
    
    sigma = round(sigma,4)
    freq = round(freq,4)
    amp = round(amp,4)
    fase = round(fase,4)
    xi = round(xi,4)
       
    return sigma, freq, amp, fase, xi, MSE

def PrintValues(filename, amp, freq, fase, sigma, xi, MSEgfitness):
    print("Arquivo: ",filename)
    print("\n")
    print("Amplitude:",round(amp,4))
    print("Fase:",round(fase,4))
    print("Frequência:",round(freq,4))
    print("Decaimento:",round(sigma,4))
    print("Amortecimento:",round(xi,4))
    print("Erro Quadrático Médio: ", MSEgfitness)
    print("\n")    

def PrintValuesi(filename, amp, freq, fase, sigma, xi, MSEgfitness, i):
    print("Arquivo: ",filename)
    print("Amostra: ", i+1)
    print("\n")
    print("Amplitude:",round(amp,4))
    print("Fase:",round(fase,4))
    print("Frequência:",round(freq,4))
    print("Decaimento:",round(sigma,4))
    print("Amortecimento:",round(xi,4))
    print("Erro Quadrático Médio: ", MSEgfitness)
    print("\n")    
    
    
def FilterSR(sr, freq):
    filename = 'DadosFreqSRFit.txt'
    f = open(filename, "r")
    g = f.readlines()
    g = g[0].rstrip().split(" ")
    a = float(g[2])
    f.close()
    freq = -a*sr+freq
    
    filename = 'DadosFreqXiFit.txt'
    f = open(filename, "r")
    g = f.readlines()
    a = g[0].rstrip().split(" ")
    a = float(a[2])
    b = g[1].rstrip().split(" ")
    b = float(b[2])
    
    xi = (freq - b)/a
    
    return freq, xi

def ReadFilename(filename):
    with open(filename) as f:
        reader = csv.reader(f)
        #Os 3 comandos seguintes repetidos foram usados para ignorar as 3
        #primeiras linhas do arquivo csv impressas pelo software ATPDraw
        next(reader)
        next(reader)
        next(reader)
    
        t=[]
        x=[]
        for row in reader:
            t.append(float(row[0]))
            x.append(float(row[1]))
    f.close()
    
    #Os seguintes comandos tem como objetivo encontrar o primeiro pico
    #e calibrá-lo como o ponto zero
    
    i=x.index(max(x))
    l=len(x)
    x=x[i:l]
    t=t[i:l]
    t=np.asarray(t)
    t = t-t[0]
    
    return x,t

def ReadFileX(filename):
    with open(filename) as f:
        reader = csv.reader(f)
        #Os 3 comandos seguintes repetidos foram usados para ignorar as 3
        #primeiras linhas do arquivo csv impressas pelo software ATPDraw
        next(reader)
        next(reader)
        next(reader)
        
        x=[]
        for row in reader:
            x.append(float(row[1]))
    f.close()
    return x
    
def FromArray2DtoMatrix(A):
    columns = len(A)
    arrows = len(A[0])
    
    M = np.zeros((arrows, columns))
    
    for i in range(0, columns):
        B = np.asarray(A[i])
        B = np.transpose(B)
        M[:,i] = B
        
    return M

def FromSigma2Xi(freq, sigma):
    w=2*np.pi*freq
    sw=(sigma**2+w**2)**0.5
    xi=-sigma/sw
    xi=xi*100
    return xi
    
def PrintProny(freq, sigma, MSE_Prony):
    xi = FromSigma2Xi(freq, sigma)
    print('Frequência: ', freq)
    print('Taxa de Amortecimento: ', xi)
    print('Erro Quadrático Médio: ', MSE_Prony)
    
    
def Caution():
    print('Observação:')
    print('Caso perceba que os valores dos parâmetros divergiram muito')
    print(' do esperado e que o Erro Quadrático Médio foi alto, então')
    print(' aborte imediatamente a compilação e atribua um valor mais')
    print(' elevado para a ordem o sistema p.')    









