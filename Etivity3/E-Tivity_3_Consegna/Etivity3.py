print("--------------------------------------------------------")
print("Nome: Roberto - Cognome: Barbato - Matricola: IN32000164")
print("--------------------------------------------------------")
print("Python - E-Tivity 3")
print("--------------------------------------------------------")

import pandas as pd                                 # lo utilizzerò per caricare e manipolare i dati del file csv

dataRace = pd.read_csv('./archivio/races.csv')
dataCostruttori = pd.read_csv('./archivio/constructors.csv')
dataRisultati = pd.read_csv('./archivio/results.csv')
dataPiloti = pd.read_csv('./archivio/drivers.csv')

"""
print(dataRace.head())
print(dataRace.info())           # Info generali sulle colonne
dataRace.columns                 # Lista di tutte le colonne
print(dataRace.describe())       # Statistiche numeriche
print("____________________________________")
print(dataCostruttori.head())
print(dataCostruttori.info())           # Info generali sulle colonne
dataCostruttori.columns                 # Lista di tutte le colonne
print(dataCostruttori.describe())       # Statistiche numeriche
print("____________________________________")
print(dataRisultati.head())
print(dataRisultati.info())           # Info generali sulle colonne
dataRisultati.columns                 # Lista di tutte le colonne
print(dataRisultati.describe())       # Statistiche numeriche
print("____________________________________")
print(dataPiloti.head())
print(dataPiloti.info())           # Info generali sulle colonne
dataPiloti.columns                 # Lista di tutte le colonne
print(dataPiloti.describe())       # Statistiche numeriche
"""

primoMerge = pd.merge(
    dataRisultati,
    dataCostruttori[['constructorId', 'name']],
    on='constructorId',
    how='left'
)
# print(primoMerge.head())

secondoMerge = pd.merge(
    primoMerge,
    dataPiloti[['driverId', 'surname','nationality']],
    on='driverId',
    how='left'    
)

secondoMerge = secondoMerge.drop(columns=['constructorId', 'driverId'])
secondoMerge = secondoMerge.rename(columns={'name': 'Scuderia', 'surname': 'Pilota','nationality':'Nazionalità'})

# print(secondoMerge.head())

dataAnalisi = pd.merge(
    secondoMerge,
    dataRace[['raceId','name','year']],
    on='raceId',
    how='left'
)

# print(dataAnalisi.head())
dataAnalisi = dataAnalisi.rename(columns={'name': 'Circuito', 'year': 'Anno','positionOrder':'Posizione Finale'})

print(dataAnalisi[['Circuito','Anno','Scuderia', 'Pilota','Nazionalità','Posizione Finale']].head(10))

#dataAnalisi[['Circuito', 'Anno', 'Scuderia', 'Pilota', 'Nazionalità', 'Posizione Finale']].to_csv('output_f1.csv', index=False)
