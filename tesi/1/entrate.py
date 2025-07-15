##
## Calcolo dell'entropia di Shannon per le entrate del Cash Flow
##
## In questa sezione si analizza la variabilità delle entrate mensili, distinguendo tra:
## - Entrate "pure": movimenti positivi con Passaggio Fondi = No (es. finanziamenti, contributi, incassi esterni)
## - Entrate "interne": trasferimenti tra conti, ovvero movimenti positivi con Passaggio Fondi = Sì
## L'obiettivo è misurare, per ogni categoria e dettaglio, la stabilità dei flussi in ingresso nel tempo.
##
## Risultati principali (entrate pure):
## - Reparti Operativi → entropia 6.9627 bit → comportamento altamente variabile - forte isntabilità anche sul lato delle entrate
## - Finanziamenti → entropia 4.6558 bit → comportamento moderatamente variabile - più regolari ma non del tutto prevedibili
##
## Risultati (entrate da trasferimenti interni):
## - Viene calcolata l'entropia solo per le categorie ≠ "Finanziamenti", che ricevono fondi tramite Passaggio Fondi = Sì
## - Questo consente di osservare il comportamento delle strutture nel richiedere/gestire fondi interni
## Questo doppio livello di analisi permette di distinguere tra instabilità reale (entrate esterne) e instabilità interna,
## evidenziando potenziali squilibri o anomalie nella gestione delle risorse.


import pandas as pd
from scipy.stats import entropy
import numpy as np

# definizione entrate per categorie

df = pd.read_csv("registro_cassa.csv", sep=";", encoding="ISO-8859-1")
df["Importo"] = df["Importo"].str.replace(",", ".").astype(float).round(2)
df["Data Movimento"] = pd.to_datetime(df["Data Movimento"], format="%d/%m/%Y")

df_entrate = df[(df["Importo"] > 0) & (df["Passaggio Fondi"] == "No")]
# print(df_entrate[["Data Movimento", "Importo", "Passaggio Fondi"]].head())
df_entrate["Mese"] = df_entrate["Data Movimento"].dt.to_period("M")
riepilogo = df_entrate.groupby(["Mese", "CashFlow - Categoria"])["Importo"].sum().reset_index()

# Calcolo entropia di Shannon per le entrate vere (per categoria)
categorie = riepilogo["CashFlow - Categoria"].unique()
risultati_entrate = []

for categoria in categorie:
    dati_cat = riepilogo[riepilogo["CashFlow - Categoria"] == categoria]
    valori = dati_cat["Importo"].abs().values

    if len(valori) == 0 or valori.sum() == 0:
        continue

    if len(set(valori)) == 1:
        entropia_val = 0.0
    else:
        probabilità = valori / valori.sum()
        entropia_val = entropy(probabilità, base=2)

    risultati_entrate.append({
        "Categoria": categoria,
        "Entropia": round(entropia_val, 4)
    })

df_entropie_entrate = pd.DataFrame(risultati_entrate).sort_values(by="Entropia", ascending=False)

print("\nEntropia delle entrate vere per categoria:")
print(df_entropie_entrate.head(10))

##
## Entropia delle entrate pure per ciascun dettaglio
##
## Si analizzano le entrate reali (Importo > 0 e Passaggio Fondi = No)
## calcolando l'entropia mensile per ciascun dettaglio (CashFlow - Dettaglio),
## nel rispetto della gerarchia 1:N rispetto alla categoria principale.
##

risultati_dettagli_entrate = []

for categoria in categorie:
    df_cat = df_entrate[df_entrate["CashFlow - Categoria"] == categoria].copy()
    df_cat["Mese"] = df_cat["Data Movimento"].dt.to_period("M")

    riepilogo_dett = df_cat.groupby(["Mese", "CashFlow - Dettaglio"])["Importo"].sum().reset_index()
    dettagli = riepilogo_dett["CashFlow - Dettaglio"].unique()

    for dettaglio in dettagli:
        subset = riepilogo_dett[riepilogo_dett["CashFlow - Dettaglio"] == dettaglio]
        valori = subset["Importo"].abs().values

        if len(valori) == 0 or valori.sum() == 0:
            continue

        if len(set(valori)) == 1:
            entropia_val = 0.0
        else:
            probabilità = valori / valori.sum()
            entropia_val = entropy(probabilità, base=2)

        risultati_dettagli_entrate.append({
            "Categoria": categoria,
            "Dettaglio": dettaglio,
            "Entropia": round(entropia_val, 4)
        })

df_entropie_dettagli_entrate = pd.DataFrame(risultati_dettagli_entrate).sort_values(by=["Categoria", "Entropia"], ascending=[True, False])

print("\nEntropia per ogni dettaglio (entrate pure):")
print(df_entropie_dettagli_entrate.head(10))

df_trasferimenti = df[(df["Importo"] > 0) & (df["Passaggio Fondi"] == "Si") & (df["CashFlow - Categoria"] != "Finanziamenti")].copy()
df_trasferimenti["Mese"] = df_trasferimenti["Data Movimento"].dt.to_period("M")

riepilogo_trasf = df_trasferimenti.groupby(["Mese", "CashFlow - Categoria"])["Importo"].sum().reset_index()

categorie_trasf = riepilogo_trasf["CashFlow - Categoria"].unique()
risultati_trasf = []

for categoria in categorie_trasf:
    dati_cat = riepilogo_trasf[riepilogo_trasf["CashFlow - Categoria"] == categoria]
    valori = dati_cat["Importo"].abs().values

    if len(valori) == 0 or valori.sum() == 0:
        continue

    if len(set(valori)) == 1:
        entropia_val = 0.0
    else:
        probabilità = valori / valori.sum()
        entropia_val = entropy(probabilità, base=2)

    risultati_trasf.append({
        "Categoria": categoria,
        "Entropia": round(entropia_val, 4)
    })

if risultati_trasf:
    df_entropie_trasferimenti = pd.DataFrame(risultati_trasf).sort_values(by="Entropia", ascending=False)
    print("\nEntropia delle entrate da passaggi fondi (interne):")
    print(df_entropie_trasferimenti.head(10))
else:
    print("\n⚠️ Nessuna categoria ha ricevuto entrate da passaggi fondi (interne).")

riepilogo_dett_trasf = df_trasferimenti.groupby(
    ["Mese", "CashFlow - Categoria", "CashFlow - Dettaglio"]
)["Importo"].sum().reset_index()

dettagli_trasf = riepilogo_dett_trasf[["CashFlow - Categoria", "CashFlow - Dettaglio"]].drop_duplicates()

risultati_dett_trasf = []

for _, riga in dettagli_trasf.iterrows():
    categoria = riga["CashFlow - Categoria"]
    dettaglio = riga["CashFlow - Dettaglio"]

    subset = riepilogo_dett_trasf[
        (riepilogo_dett_trasf["CashFlow - Categoria"] == categoria) &
        (riepilogo_dett_trasf["CashFlow - Dettaglio"] == dettaglio)
    ]

    valori = subset["Importo"].abs().values

    if len(valori) == 0 or valori.sum() == 0:
        continue

    if np.allclose(valori, valori[0], atol=1e-2):
        entropia_val = 0.0
    else:
        probabilità = valori / valori.sum()
        entropia_val = entropy(probabilità, base=2)

    risultati_dett_trasf.append({
        "Categoria": categoria,
        "Dettaglio": dettaglio,
        "Entropia Trasferimenti": round(entropia_val, 4)
    })

df_entropie_dett_trasferimenti = pd.DataFrame(risultati_dett_trasf).sort_values(by=["Categoria", "Entropia Trasferimenti"], ascending=[True, False])

print("\nEntropia dei trasferimenti interni per dettaglio:")
print(df_entropie_dett_trasferimenti.head(10))