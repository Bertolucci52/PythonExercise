import pandas as pd
from scipy.stats import entropy
import numpy as np

# definizione uscite per categorie

df = pd.read_csv("registro_cassa.csv", sep=";", encoding="ISO-8859-1")
df["Importo"] = df["Importo"].str.replace(",", ".").astype(float).round(2)
df["Data Movimento"] = pd.to_datetime(df["Data Movimento"], format="%d/%m/%Y")

df_uscite = df[(df["Importo"] < 0) & (df["Passaggio Fondi"] == "No")]
# print(df_uscite[["Data Movimento", "Importo", "Passaggio Fondi"]].head())
df_uscite["Mese"] = df_uscite["Data Movimento"].dt.to_period("M")
riepilogo = df_uscite.groupby(["Mese", "CashFlow - Categoria"])["Importo"].sum().reset_index()

# print(riepilogo.head(10))

# print("--------------------------------------------------------------")

# Lista di tutte le categorie presenti
categorie = riepilogo["CashFlow - Categoria"].unique()


risultati = []

for categoria in categorie:
    dati_cat = riepilogo[riepilogo["CashFlow - Categoria"] == categoria]
    valori = dati_cat["Importo"].abs().values
    
    # Salta categorie senza dati utili
    if len(valori) == 0 or valori.sum() == 0:
        continue

    probabilità = valori / valori.sum()
    entropia = entropy(probabilità, base=2)
    
    risultati.append({
        "Categoria": categoria,
        "Entropia": round(entropia, 4)
    })

df_entropie = pd.DataFrame(risultati).sort_values(by="Entropia", ascending=False)

print(df_entropie.head(10))
print("--------------------------------------------------------------")

##
## Calcolo dell'entropia di Shannon per ogni categoria del Cash Flow
##
## In questa sezione si misura la variabilità delle uscite mensili per ogni macro-categoria contabile.
## L'obiettivo è identificare quali categorie mostrano un comportamento regolare e prevedibile nel tempo
## (entropia bassa), e quali invece risultano fortemente variabili o caotiche (entropia alta).
## L'entropia viene calcolata sulla distribuzione mensile degli importi (valori assoluti), 
## e il risultato è espresso in bit (log base 2), secondo la definizione classica di Shannon.
## Le categorie con entropia elevata sono potenzialmente soggette ad anomalie, 
## ma è necessario proseguire l'analisi verificando se tale variabilità può essere spiegata 
## da variabili secondarie (es. dettagli). 
## In caso contrario, si considerano candidati anomalie effettive.
##
## Risultati ottenuti:
## - Amministrazione: entropia 6.9261 bit → comportamento altamente variabile
## - Reparti Operativi: entropia 6.9594 bit → comportamento altamente variabile
## - Finanziamenti: entropia 6.2770 bit → variabilità significativa
## - Logistica: entropia 1.5621 bit → comportamento stabile con lieve variabilità
## Si verificherà ora se la loro variabilità è giustificata da altre informazioni disponibili,
## come le sotto-categorie (CashFlow - Dettaglio), così da “spiegare” l'entropia o confermare la presenza di anomalie.
##

# ----------------------------------------------------------------------------------

risultati_dettagli = []


for categoria in categorie:
    df_cat = df_uscite[df_uscite["CashFlow - Categoria"] == categoria].copy()
    df_cat["Mese"] = df_cat["Data Movimento"].dt.to_period("M")
    
    riepilogo_dett = df_cat.groupby(["Mese", "CashFlow - Dettaglio"])["Importo"].sum().reset_index()
    
    # Trova tutti i dettagli unici per questa categoria
    dettagli = riepilogo_dett["CashFlow - Dettaglio"].unique()

    for dettaglio in dettagli:
        subset = riepilogo_dett[riepilogo_dett["CashFlow - Dettaglio"] == dettaglio]
        valori = subset["Importo"].abs().values

        if len(valori) == 0 or valori.sum() == 0:
            continue

        # Se tutti i valori sono uguali, l'entropia è 0
        if len(set(valori)) == 1:
            entropia_val = 0.0
        else:
            probabilità = valori / valori.sum()
            entropia_val = entropy(probabilità, base=2)

        risultati_dettagli.append({
            "Categoria": categoria,
            "Dettaglio": dettaglio,
            "Entropia": round(entropia_val, 4)
        })


df_entropie_dettagli = pd.DataFrame(risultati_dettagli).sort_values(by=["Categoria", "Entropia"], ascending=[True, False])

# Mostra i primi risultati
print("\nEntropia per ogni dettaglio, per categoria:")
print(df_entropie_dettagli.head(10))