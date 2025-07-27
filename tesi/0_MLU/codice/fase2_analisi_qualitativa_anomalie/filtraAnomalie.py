import pandas as pd

# Carica il dataset completo con le entropie e le segnalazioni
df = pd.read_csv("../fase1_machine_learning_non_supervisionato/risultati_isolation_forest.csv", sep=",", encoding="utf-8-sig")

# Conversione del campo Mese in oggetto periodo (per confronto)
df["Mese"] = pd.to_datetime(df["Mese"]).dt.to_period("M")

# Isola le anomalie
anomalie = df[df["Anomaly Score"] == -1].copy()

# Lista per salvare le analisi con entropia storica
risultati = []

for idx, riga in anomalie.iterrows():
    categoria = riga["Categoria"]
    dettaglio = riga["Dettaglio"]
    mese = riga["Mese"]
    entropia_marginale = riga["Entropia"]

    # Trova tutti gli altri mesi (escludi quello attuale)
    storico = df[
        (df["Categoria"] == categoria) &
        (df["Dettaglio"] == dettaglio) &
        (df["Mese"] != mese)
    ]

    if storico.empty:
        media_storica = None
        std_storica = None
        scarto_assoluto = None
        rapporto = None
    else:
        media_storica = storico["Entropia"].mean()
        std_storica = storico["Entropia"].std()
        scarto_assoluto = entropia_marginale - media_storica
        rapporto = entropia_marginale / media_storica if media_storica != 0 else None

    risultati.append({
        "Mese": mese,
        "Categoria": categoria,
        "Dettaglio": dettaglio,
        "Entropia Marginale": entropia_marginale,
        "Entropia Storica Media": round(media_storica, 4) if media_storica is not None else None,
        "Entropia Storica Std": round(std_storica, 4) if std_storica is not None else None,
        "Scarto Assoluto": round(scarto_assoluto, 4) if scarto_assoluto is not None else None,
        "Rapporto (Marginale/Storica)": round(rapporto, 4) if rapporto is not None else None
    })

# Salva su nuovo CSV
df_risultati = pd.DataFrame(risultati)
df_risultati.to_csv("analisi_entropia_anomalie.csv", index=False)

print("Analisi completata. File salvato come 'analisi_entropia_anomalie.csv'.")
input("Premi INVIO per chiudere...")
