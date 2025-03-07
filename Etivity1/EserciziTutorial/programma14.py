import pandas as pd
import matplotlib.pyplot as plt
import sys

df = pd.read_csv(r"C:\Users\Utente\Desktop\Python\Etivity1\EserciziTutorial\iris.csv")  # Carica il dataset
df = df.drop(['Id'], axis=1)    # Rimuove la colonna "Id"

target = df['Species']

s = list(set(target))  # Convertiamo direttamente il set in una lista senza bisogno di un ciclo

print(s)

plt.figure(figsize=(8,6))  # Imposta la dimensione del grafico
marker_vect = ['+', '_', '*']  # Marker diversi per ogni specie
color_vect = ['green', 'red', 'blue']  # Colori diversi per ogni specie

#Creazione del ciclo for per plottare ogni specie

for numero in range(len(s)):  # Itera su ogni specie
    print(numero)
    df_singola_specie = df[df.Species == s[numero]]  # Filtra il dataset per la specie corrente
    x = df_singola_specie['SepalLengthCm']  # Asse X: lunghezza sepalo
    y = df_singola_specie['PetalLengthCm']  # Asse Y: lunghezza petalo
    plt.scatter(x, y, marker=marker_vect[numero], color=color_vect[numero])  # Plotta i dati

plt.show()
