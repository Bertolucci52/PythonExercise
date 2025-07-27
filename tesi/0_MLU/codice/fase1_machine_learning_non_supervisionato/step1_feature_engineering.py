import pandas as pd
import numpy as np
from scipy.stats import entropy

# Caricamento del dataset
df = pd.read_csv("../dataset/registro_cassa.csv", sep=";", encoding="ISO-8859-1")

# Pulizia e formattazione
df["Importo"] = df["Importo"].str.replace(",", ".").astype(float).round(2)
df["Data Movimento"] = pd.to_datetime(df["Data Movimento"], format="%d/%m/%Y")
df["Mese"] = df["Data Movimento"].dt.to_period("M")

# Gruppo su base Categoria + Dettaglio + Mese
gruppi = df.groupby(["Mese", "CashFlow - Categoria", "CashFlow - Dettaglio"])

# Costruzione del dataset di feature mensili
records = []

for (mese, categoria, dettaglio), gruppo in gruppi:
    importi = gruppo["Importo"].values
    abs_importi = np.abs(importi)

    if abs_importi.sum() > 0:
        probabilità = abs_importi / abs_importi.sum()
        entropia_val = entropy(probabilità, base=2)
    else:
        entropia_val = 0.0

    records.append({
        "Mese": str(mese),
        "Categoria": categoria,
        "Dettaglio": dettaglio,
        "Numero Movimenti": len(importi),
        "Importo Medio": np.mean(importi),
        "Importo Totale": np.sum(importi),
        "Varianza": np.var(importi),
        "Entropia": round(entropia_val, 4)
    })

df_features = pd.DataFrame(records)
print(df_features.head())

df_features.to_csv("features_ml_mensili.csv", index=False)

## RIEPILOGO 

# partendo dal db grezzo "registro_cassa.csv" ho creato una struttura di feature statistiche mensili per ogni combo possibile:
# Mese x Categoria x Dettaglio
# andando a calcolare il numero di movimenti che ci sono stati nel mese, l'importo totale movimentato, l'importo medio
# la varianza (ossia, quanto sono variabili i valori - dispersione -) e l'entropia (quanto è distribuita l'intensità dei movimenti)

# Entropia Alta ---> distribuzione diffusa (molti valori diversi) ; Bassa ---> comportamento ripetitivo
# Varianza Alta ---> importi molto diversi tra loro ; Bassa ---> tutti simili
# nMovimenti Molti ---> attività intensa ; Pochi ---> enveti isolati o inattività
# impTotale Positivo ---> entrata netta ; Negativo ---> uscita netta ; Zero ---> compensazione o inattività

# Entropia = 0 (vds stipendi, nella maggior parte dei casi) ---> tutti i valori del mese sono uguali
# Entropia Alta ma Varianza Bassa (vds attività reparti operativi) ---> tanti piccoli importi ma distribuiti uniformemente 
# Varianza Alta e nMovimenti pochi (vds bonus lavoratori) ---> eventi fuori scala
