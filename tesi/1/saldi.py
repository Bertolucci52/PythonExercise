import pandas as pd
from scipy.stats import entropy
import numpy as np

df = pd.read_csv("../dataset/registro_cassa.csv", sep=";", encoding="ISO-8859-1")
df["Importo"] = df["Importo"].str.replace(",", ".").astype(float).round(2)
df["Data Movimento"] = pd.to_datetime(df["Data Movimento"], format="%d/%m/%Y")
df["Mese"] = df["Data Movimento"].dt.to_period("M")

riepilogo_saldo = df.groupby(["Mese", "CashFlow - Categoria"])["Importo"].sum().reset_index()

# print("\nSaldo mensile per categoria:")
# print(riepilogo_saldo.head(10))

categorie = riepilogo_saldo["CashFlow - Categoria"].unique()
risultati_saldi = []

for categoria in categorie:
    dati_cat = riepilogo_saldo[riepilogo_saldo["CashFlow - Categoria"] == categoria]
    valori = dati_cat["Importo"].abs().values

    if len(valori) == 0 or valori.sum() == 0:
        continue

    if len(set(valori)) == 1:
        entropia_val = 0.0
    else:
        probabilità = valori / valori.sum()
        entropia_val = entropy(probabilità, base=2)

    risultati_saldi.append({
        "Categoria": categoria,
        "Entropia Saldo": round(entropia_val, 4)
    })

df_entropie_saldi = pd.DataFrame(risultati_saldi).sort_values(by="Entropia Saldo", ascending=False)


print("\nEntropia del saldo per categoria:")
print(df_entropie_saldi.head(10))


riepilogo_saldo_dettagli = df.groupby(["Mese", "CashFlow - Categoria", "CashFlow - Dettaglio"])["Importo"].sum().reset_index()
dettagli_saldi = riepilogo_saldo_dettagli[["CashFlow - Categoria", "CashFlow - Dettaglio"]].drop_duplicates()

risultati_saldi_dettagli = []

for _, riga in dettagli_saldi.iterrows():
    categoria = riga["CashFlow - Categoria"]
    dettaglio = riga["CashFlow - Dettaglio"]

    subset = riepilogo_saldo_dettagli[
        (riepilogo_saldo_dettagli["CashFlow - Categoria"] == categoria) &
        (riepilogo_saldo_dettagli["CashFlow - Dettaglio"] == dettaglio)
    ]

    valori = subset["Importo"].abs().values

    if len(valori) == 0 or valori.sum() == 0:
        continue

    if len(set(valori)) == 1:
        entropia_val = 0.0
    else:
        probabilità = valori / valori.sum()
        entropia_val = entropy(probabilità, base=2)

    risultati_saldi_dettagli.append({
        "Categoria": categoria,
        "Dettaglio": dettaglio,
        "Entropia Saldo": round(entropia_val, 4)
    })


df_entropie_saldo_dettagli = pd.DataFrame(risultati_saldi_dettagli).sort_values(by=["Categoria", "Entropia Saldo"], ascending=[True, False])

print("\nEntropia del saldo per ciascun dettaglio:")
print(df_entropie_saldo_dettagli.head(10))