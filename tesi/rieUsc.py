import pandas as pd
from scipy.stats import entropy
import numpy as np

# Import + normalizzazione dei dati

# ----------------------------------------------------------------------------------

df = pd.read_csv("registro_cassa.csv", sep=";", encoding="ISO-8859-1")
df["Importo"] = df["Importo"].str.replace(",", ".").astype(float).round(2)
df["Data Movimento"] = pd.to_datetime(df["Data Movimento"], format="%d/%m/%Y")

# ----------------------------------------------------------------------------------

# Definizione delle uscite, eslusione dei passaggi fondo, e riepilogo per aaaa-mm

df_uscite = df[(df["Importo"] < 0) & (df["Passaggio Fondi"] == "No")]
print(df_uscite[["Data Movimento", "Importo", "Passaggio Fondi"]].head())
df_uscite["Mese"] = df_uscite["Data Movimento"].dt.to_period("M")
riepilogo = df_uscite.groupby(["Mese", "CashFlow - Categoria"])["Importo"].sum().reset_index()

print(riepilogo.head(10))
print("--------------------------------------------------------------")

# Entropia di Shannon

# ----------------------------------------------------------------------------------

# categoria_target = "Reparti Operativi"
# Filtra solo le righe della categoria scelta
# dati_categoria = riepilogo[riepilogo["CashFlow - Categoria"] == categoria_target]
# Prendi gli importi (valori assoluti) e normalizzali in una distribuzione di probabilità
# valori = dati_categoria["Importo"].abs().values
# probabilità = valori / valori.sum()
# Calcola l'entropia di Shannon (base 2)
# entropia = entropy(probabilità, base=2)
# print(f"Entropia per la categoria '{categoria_target}': {entropia:.4f} bit")

# ----------------------------------------------------------------------------------

# Lista di tutte le categorie presenti
categorie = riepilogo["CashFlow - Categoria"].unique()

# Lista per salvare i risultati
risultati = []

# Ciclo su ogni categoria
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

# Creiamo un DataFrame dei risultati ordinato
df_entropie = pd.DataFrame(risultati).sort_values(by="Entropia", ascending=False)

# Mostra le prime righe
print(df_entropie.head(10))
print("--------------------------------------------------------------")

##
## Calcolo dell'entropia di Shannon per ogni categoria del Cash Flow
##
## In questa sezione si misura la variabilità delle uscite mensili per ogni macro-categoria contabile.
## L'obiettivo è identificare quali categorie mostrano un comportamento regolare e prevedibile nel tempo
## (entropia bassa), e quali invece risultano fortemente variabili o caotiche (entropia alta).
##
## L'entropia viene calcolata sulla distribuzione mensile degli importi (valori assoluti), 
## e il risultato è espresso in bit (log base 2), secondo la definizione classica di Shannon.
##
## Le categorie con entropia elevata sono potenzialmente soggette ad anomalie, 
## ma è necessario proseguire l'analisi verificando se tale variabilità può essere spiegata 
## da variabili secondarie (es. dettagli, risorse, annotazioni). 
## In caso contrario, si considerano candidati anomalie effettive.
##
## Risultati ottenuti:
## - Amministrazione: entropia 6.9640 bit → comportamento altamente variabile
## - Reparti Operativi: entropia 6.9594 bit → comportamento altamente variabile
## - Finanziamenti: entropia 6.2770 bit → variabilità significativa
## - Logistica: entropia 0.0000 bit → comportamento perfettamente stabile
##
## Le prime tre categorie sono quindi buone candidate per un'analisi approfondita.
## In particolare, si verificherà se la loro variabilità è giustificata da altre informazioni disponibili,
## come le sotto-categorie (CashFlow - Dettaglio), così da “spiegare” l'entropia o confermare la presenza di anomalie.
##


# ----------------------------------------------------------------------------------

categoria_target = "Amministrazione"

# Filtra il riepilogo per la categoria Amministrazione
dati_categoria = df_uscite[df_uscite["CashFlow - Categoria"] == categoria_target].copy()

# Aggiungiamo la colonna "Mese" se non già presente
dati_categoria["Mese"] = dati_categoria["Data Movimento"].dt.to_period("M")

# Raggruppa per Mese e Dettaglio, somma gli importi
riepilogo_dettagli = dati_categoria.groupby(["Mese", "CashFlow - Dettaglio"])["Importo"].sum().reset_index()

dettagli = riepilogo_dettagli["CashFlow - Dettaglio"].unique()
risultati_dettaglio = []

for dettaglio in dettagli:
    subset = riepilogo_dettagli[riepilogo_dettagli["CashFlow - Dettaglio"] == dettaglio]
    valori = subset["Importo"].abs().values
    
    if len(valori) == 0 or valori.sum() == 0:
        continue

    probabilità = valori / valori.sum()
    entropia_val = entropy(probabilità, base=2)
    
    risultati_dettaglio.append({
        "Dettaglio": dettaglio,
        "Entropia": round(entropia_val, 4)
    })

df_entropie_dettagli = pd.DataFrame(risultati_dettaglio).sort_values(by="Entropia", ascending=False)

print(df_entropie_dettagli)

print("--------------------------------------------------------------")
print("--------------------------------------------------------------")
print("--------------------------------------------------------------")

# ----------------------------------------------------------------------------------

# 🔍 Analisi puntuale: valori mensili per il dettaglio "Stipendi"
stipendi = riepilogo_dettagli[riepilogo_dettagli["CashFlow - Dettaglio"] == "Stipendi"]
print(stipendi.sort_values(by="Mese"))
