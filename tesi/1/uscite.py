import pandas as pd
from scipy.stats import entropy
import numpy as np

df = pd.read_csv("../dataset/registro_cassa.csv", sep=";", encoding="ISO-8859-1")
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

risultati_dettagli = []


for categoria in categorie:
    df_cat = df_uscite[df_uscite["CashFlow - Categoria"] == categoria].copy()
    df_cat["Mese"] = df_cat["Data Movimento"].dt.to_period("M")
    
    riepilogo_dett = df_cat.groupby(["Mese", "CashFlow - Dettaglio"])["Importo"].sum().reset_index()
    
    # Trova tutti i dettagli unici per categoria
    dettagli = riepilogo_dett["CashFlow - Dettaglio"].unique()

    for dettaglio in dettagli:
        subset = riepilogo_dett[riepilogo_dett["CashFlow - Dettaglio"] == dettaglio]
        valori = subset["Importo"].abs().values

        if len(valori) == 0 or valori.sum() == 0:
            continue

        # Se tutti i valori sono uguali (stipendi costanti nei mesi), l'entropia è 0
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

print("\nEntropia per ogni dettaglio, per categoria:")
print(df_entropie_dettagli.head(10))