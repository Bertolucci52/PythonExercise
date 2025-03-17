print("--------------------------------------------------------")
print("Nome: Roberto - Cognome: Barbato - Matricola: IN32000164")
print("--------------------------------------------------------")
print("Python - E-Tivity 2")
print("--------------------------------------------------------")

import pandas as pd                                 # lo utilizzerò per caricare e manipolare i dati del file csv
from scipy.stats import chi2_contingency            # permette di calcolare automaticamente i valori attesi, il chi-quadro,p-value e gradi di libertà


# 1. Importo il file csv e così come fatto su excel vado a creare un'unica tabella contenente i dati dei singoli giocatori: "dataFrameAnalisi"

dataFrameOriginale = pd.read_csv('AusOpen-men-2013.csv')

"""
print(dataFrameOriginale.head())           # Prime 5 righe
print(dataFrameOriginale.info())           # Info generali sulle colonne
dataFrameOriginale.columns                 # Lista di tutte le colonne
print(dataFrameOriginale.describe())       # Statistiche numeriche
"""

dataFrameGiocatoreUno = pd.DataFrame({
    'Giocatore': dataFrameOriginale['Player1'],
    # Player 1: vince se Result == 1
    'Vittoria': dataFrameOriginale['Result'].apply(lambda x: 1 if x == 1 else 0),
    'Aces':dataFrameOriginale['ACE.1'],
    'BreakPointCreated': dataFrameOriginale['BPC.1'],
    'BreakPointVinti': dataFrameOriginale['BPW.1']
    
})

dataFrameGiocatoreDue = pd.DataFrame({
    'Giocatore': dataFrameOriginale['Player2'],
    # Player 2: vince se Result == 0
    'Vittoria': dataFrameOriginale['Result'].apply(lambda x: 1 if x == 0 else 0),
    'Aces':dataFrameOriginale['ACE.2'],
    'BreakPointCreated': dataFrameOriginale['BPC.2'],
    'BreakPointVinti': dataFrameOriginale['BPW.2']
    
})

dataFrameAnalisi = pd.concat([dataFrameGiocatoreUno, dataFrameGiocatoreDue], ignore_index=True)
dataFrameAnalisi['Vittoria'] = dataFrameAnalisi['Vittoria'].map({
    1: 'Si',
    0: 'No'
})

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

print("Relazione Significativa: Aces -> Vittoria è un arco valido")

# 4. Seconda ip: "Chi riesce a creare un maggior numero di Break Point ha maggiore probabilità di vittoria?" BreakPointCreati --> Vittoria

# 4.1 Tabella Osservata - BreakPointCreati - Vittorie

print("_____________________________________________________")
print("Tabella Osservazione BreakPointCreati - Vittoria ")
tabella_breakPointCreati_vittoria = pd.crosstab(dataFrameAnalisi['BPC_Range'], dataFrameAnalisi['Vittoria'])
tabella_breakPointCreati_vittoria.columns = ['Vittoria = No', 'Vittoria = Si']
tabella_breakPointCreati_vittoria.index = ['Basso [0–3]', 'Medio [4–7]', 'Alto [8–11]']
print(tabella_breakPointCreati_vittoria)
print("_____________________________________________________")

# 4.2 Tabella Test Valori Attesi - Modello Teorico Neutro

chi2, p, dof, expected = chi2_contingency(tabella_breakPointCreati_vittoria)
expected_BreakPointCreati_Vittoria = pd.DataFrame(expected, index=tabella_breakPointCreati_vittoria.index, columns=tabella_breakPointCreati_vittoria.columns)

print(expected_BreakPointCreati_Vittoria)
print("_____________________________________________________")
print("Gradi di libertà: ", dof)
print("Chi-Quadro: ",chi2)

print("Relazione Significativa: BreakPointCreati -> Vittoria è un arco valido")

# 5. Terza ip: "Ma chi crea più BreakPoint, riesce a vincerli? o meglio, chi crea + breakpoint ha maggior probabilità di vincerli? per la serie, vincere ti abitua a vincere"

# 5.1 Tabella Osservata - BreakPointCreati - BreakPointVinti
print("_____________________________________________________")
print("Tabella Osservazione BreakPointCreati - BreakPointVinti ")
tabella_breakPointCreati_breakPointVinti = pd.crosstab(dataFrameAnalisi['BPC_Range'], dataFrameAnalisi['BPW_Range'])
tabella_breakPointCreati_breakPointVinti.columns = ['Basso [0–9]', 'Medio [10–17]', 'Alto [18–28]']
tabella_breakPointCreati_breakPointVinti.index = ['Basso [0–3]', 'Medio [4–7]', 'Alto [8–11]']
print(tabella_breakPointCreati_breakPointVinti)
print("_____________________________________________________")

# 5.2 Tabella Test Valori Attesi - Modello Teorico Neutro

chi2, p, dof, expected = chi2_contingency(tabella_breakPointCreati_breakPointVinti)
expected_BreakPointCreati_BreakPointVinti = pd.DataFrame(expected, index=tabella_breakPointCreati_breakPointVinti.index, columns=tabella_breakPointCreati_breakPointVinti.columns)

print(expected_BreakPointCreati_BreakPointVinti)
print("_____________________________________________________")
print("Gradi di libertà: ", dof)
print("Chi-Quadro: ",chi2)

print("Relazione Significativa: BreakPointCreati -> BreakPointVinti è un arco valido")

# 6. Quarta ip: "Assodato che c'è un forte correlazione tra chi crea break point e break point vinti, ossia, un giocatore abituato a creare tanti breakpoint li trasforma in vittoria, mettiamo in relazione BreakPointVinti con Vittoria finale della partita"

# 6.1 Tabella Osservata - BreakPointVinti - Vittorie

print("_____________________________________________________")
print("Tabella Osservazione BreakPointVinti - Vittoria ")
tabella_BreakPointVinti_vittoria = pd.crosstab(dataFrameAnalisi['BPW_Range'], dataFrameAnalisi['Vittoria'])
tabella_BreakPointVinti_vittoria.columns = ['Vittoria = No', 'Vittoria = Si']
tabella_BreakPointVinti_vittoria.index = ['Basso [0–9]', 'Medio [10–17]', 'Alto [18–28]']
print(tabella_BreakPointVinti_vittoria)
print("_____________________________________________________")

# 6.2 Tabella Test Valori Attesi - Modello Teorico Neutro

chi2, p, dof, expected = chi2_contingency(tabella_BreakPointVinti_vittoria)
expected_BreakPointVinti_Vittoria = pd.DataFrame(expected, index=tabella_BreakPointVinti_vittoria.index, columns=tabella_BreakPointVinti_vittoria.columns)

print(expected_BreakPointVinti_Vittoria)
print("_____________________________________________________")
print("Gradi di libertà: ", dof)
print("Chi-Quadro: ",chi2)

print("Relazione Significativa: BreakPointVinti -> Vittoria è un arco valido")
print("_____________________________________________________")
print("_____________________________________________________")

from pgmpy.models import BayesianNetwork                                    # libreria per la creazione della rete bayesiana (nodi e archi)
from pgmpy.estimators import MaximumLikelihoodEstimator                     # stima le probabilità dei dati reali (CPT)
from pgmpy.inference import VariableElimination                             # calcola l'inferenza probabilistica

# 1. Definisco la struttura della rete così come elaborata in precedenza (4 nodi: Aces, Vittoria, BPC e BPW di cui 3 diretti)
model = BayesianNetwork([
    ('Aces_Range', 'Vittoria'),                 # 1° relazione diretta Aces -> Vittoria (il numero di ace influenza la probabilità di vincere la partita)
    ('BPW_Range', 'Vittoria'),                  # 2° relazione diretta BPW  -> Vittoria (i brekpoint che vinco influenzano il risultato finale)
    ('BPC_Range', 'BPW_Range')                  # 3° relazione diretta BPC  -> BPW (vincere aiuta a vincere, + break creo maggiore è la probabilità di vincerli)
])

# 2. Creazione del modello
model.fit(dataFrameAnalisi, estimator=MaximumLikelihoodEstimator)           # definisco le CPT (probabilità condizionata dai geniori + probabilità marginale dei genitori) e maximus...."probabilità più plausibili"

# 3. Creazione inferenza per la distribuzione delle probabilità in funzione della domanda
infer = VariableElimination(model)

print("Che probabilità hai di vincere una partita di tennis in funzione del tuo servizio, dei Break Point Creati/Vinti?")
aces = input("In una partita, quanti aces pensi di riuscire a fare? In che range pensi di essere? (Basso [0–14], Medio [15–25], Alto [26–41]): ").capitalize()
bpc = input("Invece, quanti Break Point riesci a creare? In che range pensi di essere? (Basso [0–3], Medio [4–7], Alto [8–11]): ").capitalize()
bpw = input("E di questi, quanti ne riesci a vincere? (Basso [meno della metà], Medio [circa la metà], Alto [più della metà]): ").capitalize()

rangeAmmesse={'Basso','Medio','Alto'}

if aces not in rangeAmmesse or bpc not in rangeAmmesse or bpw not in rangeAmmesse:
    print("Errore: range non valido. Ammessi Basso - Medio - Alto")
    exit()
    
sDomanda="Che probabilità di vincere una partita ho se rientro nei seguenti valori: Aces: {0} - BreakPointCreati: {1} - BreakPointVinti: {2} ?".format(aces,bpc,bpw)
print("_____________________________________________________")
print(sDomanda)
print("_____________________________________________________")

def calcola_prob_vittoria(aces, bpc, bpw):
    risultato = infer.query(
        variables=['Vittoria'],
        evidence={
            'Aces_Range': aces,
            'BPC_Range': bpc,
            'BPW_Range': bpw
        }
    )
    return risultato

print("\nRisultato:")
print(calcola_prob_vittoria(aces, bpc, bpw))
risultato = calcola_prob_vittoria(aces, bpc, bpw)

for val, prob in zip(risultato.state_names['Vittoria'], risultato.values):
    print(f"{val}: {prob*100:.1f}%")






