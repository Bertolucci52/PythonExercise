import pandas as pd                                 # lo utilizzerò per caricare e manipolare i dati del file csv
from scipy.stats import chi2_contingency            # permette di calcolare automaticamente i valori attesi, il chi-quadro,p-value e gradi di libertà


# 1. Importo il file csv e così come fatto su excel vado a creare un'unica tabella contenente i dati dei singoli giocatori: "dataFrameAnalisi"

dataFrameOriginale = pd.read_csv('AusOpen-men-2013.csv')

print(dataFrameOriginale.head())           # Prime 5 righe
print(dataFrameOriginale.info())           # Info generali sulle colonne
dataFrameOriginale.columns                 # Lista di tutte le colonne
print(dataFrameOriginale.describe())       # Statistiche numeriche

dataFrameGiocatoreUno = pd.DataFrame({
    'Giocatore': dataFrameOriginale['Player1'],
    'Vittoria': dataFrameOriginale['Result'].apply(lambda x: 1 if x == 1 else 0),
    'Aces':dataFrameOriginale['ACE.1'],
    'BreakPointCreated': dataFrameOriginale['BPC.1'],
    'BreakPointVinti': dataFrameOriginale['BPW.1']
    
})

dataFrameGiocatoreDue = pd.DataFrame({
    'Giocatore': dataFrameOriginale['Player2'],
    'Vittoria': dataFrameOriginale['Result'].apply(lambda x: 1 if x == 2 else 0),
    'Aces':dataFrameOriginale['ACE.2'],
    'BreakPointCreated': dataFrameOriginale['BPC.2'],
    'BreakPointVinti': dataFrameOriginale['BPW.2']
    
})

dataFrameAnalisi = pd.concat([dataFrameGiocatoreUno, dataFrameGiocatoreDue], ignore_index=True)

print(dataFrameAnalisi.head())

# 2. vado a creare i range per le 3 variabili scelte (Aces - BreakPointCreati - BreakPointVinti)

print(dataFrameAnalisi['Aces'].min(), dataFrameAnalisi['Aces'].max(), dataFrameAnalisi['Aces'].mean())
print(dataFrameAnalisi['BreakPointCreated'].min(), dataFrameAnalisi['BreakPointCreated'].max(), dataFrameAnalisi['BreakPointCreated'].mean())
print(dataFrameAnalisi['BreakPointVinti'].min(), dataFrameAnalisi['BreakPointVinti'].max(), dataFrameAnalisi['BreakPointVinti'].mean())

dataFrameAnalisi['Aces_Range'] = pd.cut(
    dataFrameAnalisi['Aces'],
    bins=[-1, 14, 25, 41],                  
    labels=['Basso', 'Medio', 'Alto']
)
print(dataFrameAnalisi['Aces_Range'].value_counts())

dataFrameAnalisi['BPC_Range'] = pd.cut(
    dataFrameAnalisi['BreakPointCreated'],
    bins=[-1, 3, 7, 11],
    labels=['Basso', 'Medio', 'Alto']
)

print(dataFrameAnalisi['BPC_Range'].value_counts())

dataFrameAnalisi['BPW_Range'] = pd.cut(
    dataFrameAnalisi['BreakPointVinti'],
    bins=[-1, 8, 14, 28],
    labels=['Basso', 'Medio', 'Alto']
)

print(dataFrameAnalisi['BPW_Range'].value_counts())

# 3. inizio con la prima ip: "Chi fa più aces ha maggiore probabilità di vittoria?" Aces --> Vittoria

# 3.1 Tabella Osservata - Aces
print("_____________________________________________________")
print("Tabella Osservazione Aces - Vittoria ")
tabella_aces_vittoria = pd.crosstab(dataFrameAnalisi['Aces_Range'], dataFrameAnalisi['Vittoria'])           # ho dovuto rimuovere margins=true (che mi restituiva i totali altrimenti "scipy" mi riportava gradi di libertà errati)
tabella_aces_vittoria.columns = ['Vittoria = NO', 'Vittoria = SI']
tabella_aces_vittoria.index = ['Basso [0–14]', 'Medio [15–25]', 'Alto [26–41]']
print(tabella_aces_vittoria)
print("_____________________________________________________")

# 3.2 Tabella Test Valori Attesi - Modello Teorico Neutro
print("_____________________________________________________")
print("Tabella Valori Attesi Aces - Vittoria ")

"""
# Ho trovato in rete una libreria che calcola automaticamente la tabella dei valori attesi, i gradi di liberta il chi-quadro ecc

totale_generale = tabella_aces_vittoria.values.sum()
riga_tot = tabella_aces_vittoria.sum(axis=1)
colonna_tot = tabella_aces_vittoria.sum(axis=0)
n_righe = tabella_aces_vittoria.shape[0]
n_colonne = tabella_aces_vittoria.shape[1]

gradi = (n_righe - 1) * (n_colonne - 1)
print("Gradi di libertà:", gradi)


expected_df = pd.DataFrame(index=tabella_aces_vittoria.index, columns=tabella_aces_vittoria.columns)

for i in tabella_aces_vittoria.index:
    for j in tabella_aces_vittoria.columns:
        expected_df.loc[i, j] = (riga_tot[i] * colonna_tot[j]) / totale_generale

print(expected_df)

chi_quadro = 0

for i in tabella_aces_vittoria.index:
    for j in tabella_aces_vittoria.columns:
        osservato = tabella_aces_vittoria.loc[i, j]
        atteso = expected_df.loc[i, j]
        contributo = (osservato - atteso) ** 2 / atteso
        chi_quadro += contributo

print("Chi-quadro:", chi_quadro)


"""

chi2, p, dof, expected = chi2_contingency(tabella_aces_vittoria)
expected_Aces_Vittoria = pd.DataFrame(expected, index=tabella_aces_vittoria.index, columns=tabella_aces_vittoria.columns)

print(expected_Aces_Vittoria)
print("_____________________________________________________")
print("Gradi di libertà: ", dof)
print("Chi-Quadro: ",chi2)
print("p-value (se < 0.05 c'è una relazione statisticamente significativa | > 0.05 nessuna evidenza di relazione (non posso rifiutare Ho)): ",p)

print("Relazione Significativa: Aces -> Vittoria è un arco valido")
