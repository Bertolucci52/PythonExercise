"""
Il programma stampa i 150 fiori nel piano (SepalLengthCm,PetalLengthCm)
colorando i fiori in modo diverso a seconda della specie.

https://trinket.io/embed/python3/a5bd54189b   (per usare python online con matplotlib)
"""
import pandas as pd
import matplotlib.pyplot as plt
import sys

#Questo codice usa la libreria csv per leggere il file
"""
import csv
s = set()
iCounter = 0;
with open('./iris.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        #print(row[5])
        if(iCounter!=0):
            s.add(row[5])
        iCounter=1
print(s)
s = list(s)
print(s[0])
"""



##axis=1 significa che il taglio e per colonna
df = pd.read_csv('./iris.csv')
df = df.drop(['Id'],axis=1)

target = df['Species']
#print(target)

#Uso la struttura dati 'insieme' perchè mi elimina le ridondanze
#In target ho 150 elementi, in s ho solo 3 elementi
s = set()
for val in target:
    s.add(val)  
#print(s)
#sys.exit(0)

s = list(s)
#print(s)
#print(s[0])
#print(len(s))

#df_singola_specie = df[df.Species==s[0]]
#print(df_singola_specie)


plt.figure(figsize=(8,6))

marker_vect = ['+','_','*']
color_vect = ['green','red', 'blue']
for numero in range(len(s)):
    print(numero)
    df_singola_specie = df[df.Species==s[numero]]
    x = df_singola_specie['SepalWidthCm']	#prendi tutte le x di una specie (numero)
    y = df_singola_specie['PetalWidthCm']  #prendi tutte le y di una specie (numero)
    plt.scatter(x,y,marker=marker_vect[numero],color=color_vect[numero])
		
plt.show()

