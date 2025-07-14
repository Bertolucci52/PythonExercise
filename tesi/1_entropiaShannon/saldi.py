import pandas as pd
from scipy.stats import entropy
import numpy as np

# ----------------------------------------------------------------------------------
# Importazione e normalizzazione del dataset

df = pd.read_csv("registro_cassa.csv", sep=";", encoding="ISO-8859-1")
df["Importo"] = df["Importo"].str.replace(",", ".").astype(float).round(2)
df["Data Movimento"] = pd.to_datetime(df["Data Movimento"], format="%d/%m/%Y")
df["Mese"] = df["Data Movimento"].dt.to_period("M")

# ----------------------------------------------------------------------------------
# Calcolo saldo mensile (entrate + uscite) per ogni categoria

# Raggruppa per mese e categoria, somma gli importi
riepilogo_saldo = df.groupby(["Mese", "CashFlow - Categoria"])["Importo"].sum().reset_index()

# Visualizza i primi saldi
# print("\nSaldo mensile per categoria:")
# print(riepilogo_saldo.head(10))

##
## Calcolo dell'entropia di Shannon sul saldo mensile per categoria
##
## Questo blocco misura la stabilità finanziaria netta delle categorie.
## L'entropia viene calcolata sulla distribuzione dei saldi mensili
## (assoluti), indicando quanto siano prevedibili i flussi economici netti.
##

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

# Visualizza i risultati
print("\nEntropia del saldo per categoria:")
print(df_entropie_saldi.head(10))

##
## Calcolo dell'entropia sul saldo mensile per ciascun dettaglio (rispettando la relazione 1:N)
##
## Dopo aver analizzato il comportamento netto delle categorie principali,
## questa sezione si concentra sui sotto-dettagli contabili per comprendere
## quali elementi specifici siano effettivamente responsabili delle instabilità osservate.
##

# Raggruppa per mese e dettaglio, calcola il saldo
riepilogo_saldo_dettagli = df.groupby(["Mese", "CashFlow - Categoria", "CashFlow - Dettaglio"])["Importo"].sum().reset_index()

# Ricava l'elenco dei dettagli (categoria + dettaglio)
dettagli_saldi = riepilogo_saldo_dettagli[["CashFlow - Categoria", "CashFlow - Dettaglio"]].drop_duplicates()

# Lista risultati
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

# Ordina i risultati
df_entropie_saldo_dettagli = pd.DataFrame(risultati_saldi_dettagli).sort_values(by=["Categoria", "Entropia Saldo"], ascending=[True, False])

# Mostra i primi risultati
print("\nEntropia del saldo per ciascun dettaglio:")
print(df_entropie_saldo_dettagli.head(10))

##
## Calcolo dell'entropia di Shannon sul saldo netto per ciascun dettaglio
##
## In questa sezione si analizza il comportamento finanziario netto dei singoli dettagli
## contabili (CashFlow - Dettaglio), raggruppati per la rispettiva categoria di appartenenza.
## L'obiettivo è individuare quali elementi siano i veri responsabili della variabilità
## osservata nel saldo mensile delle macro-categorie.
##
## Risultati principali:
##
## - Reparti Operativi:
##   • Hardware → entropia 6.5387
##   • Software → entropia 6.6038
##   → Entrambi fortemente instabili → confermano il caos della categoria a livello micro
##
## - Amministrazione:
##   • Stipendi → entropia 6.2504
##   • Bonus Lavoratore → entropia 1.6790
##   → Gli stipendi, che ci si aspetterebbe costanti, sono invece molto variabili sul saldo netto
##
## - Finanziamenti:
##   • Conferimento capitale → 4.8878
##   • Prestito bancario → 2.8807
##   → Entrambi presentano un certo grado di instabilità, suggerendo gestione a blocchi irregolari
##
## - Logistica:
##   • Beni Immobili → entropia 0.5830
##   • Auto Aziendali → entropia 0.0000
##   → Categoria generalmente stabile, conferma quanto già emerso dalle analisi precedenti
##
## Conclusione:
## L'entropia sul saldo per dettaglio permette di individuare con precisione chirurgica
## le vere fonti di instabilità economica, confermando e approfondendo le anomalie già evidenziate
## a livello di categoria.
##