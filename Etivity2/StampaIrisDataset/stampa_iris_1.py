"""
Questo programma stampa SepalLengthCm e PetalLengthCm
per le due specie setosa e versicolor, 
gia sapendo che i primi 50 elementi sono setosa e i 50 successivi sono 
versicolor
"""
import matplotlib.pyplot as plt
import sys


"""
Leggo il csv usando la libreria pandas ma in alcuni da problemi di installazione
"""
"""
import pandas as pd

df = pd.read_csv('./iris.csv')
x = df['SepalLengthCm']
y = df['PetalLengthCm']

setosa_x = x[:50]
setosa_y = y[:50]

versicolor_x = x[50:100]
versicolor_y = y[50:100]
"""


"""
petalLen_x = []
petalWid_y = []

iFlag = 0
file = open("./iris.csv")
for line in file:
    #print(line)
    vect_line = line.split(",")
    if(iFlag!=0):
        if(len(vect_line)==6):
           print(vect_line) 
           petalLen_x.append(float(vect_line[1]))
           petalWid_y.append(float(vect_line[2]))
           
    iFlag = iFlag + 1
    


## Crea il grafico
plt.figure(figsize=(8,6))
plt.scatter(petalLen_x,petalWid_y,marker='+',color='green')
plt.show()
"""



## Crea grafico in cui colori in modo diverso la specie
"""
petalLen_Set = []
petalLen_Ver = []
petalLen_Vir = []

petalWid_Set = []
petalWid_Ver = []
petalWid_Vir = []

sepalLen_Set = []
sepalLen_Ver = []
sepalLen_Vir = []

sepalWid_Set = []
sepalWid_Ver = []
sepalWid_Vir = []

specie = []

iFlag = 0
file = open("./iris.csv")
for line in file:
    #print(line)
    vect_line = line.split(",")
    if(iFlag!=0):
        if(len(vect_line)==6):
            print(vect_line)
            if(vect_line[5]=='Iris-setosa\n'):        
                petalLen_Set.append(float(vect_line[1]))
                petalWid_Set.append(float(vect_line[2]))
            if(vect_line[5]=='Iris-versicolor\n'):        
                petalLen_Ver.append(float(vect_line[1]))
                petalWid_Ver.append(float(vect_line[2]))
            if(vect_line[5]=='Iris-virginica\n'):        
                petalLen_Vir.append(float(vect_line[1])) 
                petalWid_Vir.append(float(vect_line[2]))
    iFlag = iFlag + 1
    


## Crea il grafico
plt.figure(figsize=(8,6))
plt.scatter(petalLen_Set,petalWid_Set,marker='+',color='green')
plt.scatter(petalLen_Vir,petalWid_Vir,marker='x',color='red')
plt.scatter(petalLen_Ver,petalWid_Ver,marker='*',color='blue')
plt.show()
"""


"""







