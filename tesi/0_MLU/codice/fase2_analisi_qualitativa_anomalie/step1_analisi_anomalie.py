import pandas as pd

# Carica il dataset con anomalie e tutte le feature
df = pd.read_csv("../fase1_machine_learning_non_supervisionato/risultati_isolation_forest.csv", sep=",", encoding="utf-8-sig")
df["Mese"] = pd.to_datetime(df["Mese"]).dt.to_period("M")

# Isola le anomalie
anomalie = df[df["Anomaly Score"] == -1].copy()

# Lista dei risultati da salvare
risultati = []

for idx, riga in anomalie.iterrows():
    cat = riga["Categoria"]
    dett = riga["Dettaglio"]
    mese = riga["Mese"]

    # Dataset storico per stesso Categoria + Dettaglio, escluso il mese corrente
    storico = df[
        (df["Categoria"] == cat) &
        (df["Dettaglio"] == dett) &
        (df["Mese"] != mese)
    ]

    # Valori marginali (mese anomalo)
    marg_entropia = riga["Entropia"]
    marg_varianza = riga["Varianza"]
    marg_mov = riga["Numero Movimenti"]
    marg_totale = riga["Importo Totale"]

    # Funzione di confronto
    def confronta(feature, val_marginale):
        if storico.empty:
            return (None, None, None, None)
        media = storico[feature].mean()
        std = storico[feature].std()
        scarto = val_marginale - media
        rapporto = val_marginale / media if media != 0 else None
        return (round(media, 4), round(std, 4), round(scarto, 4), round(rapporto, 4) if rapporto is not None else None)

    media_ent, std_ent, scarto_ent, rapporto_ent = confronta("Entropia", marg_entropia)
    media_var, std_var, scarto_var, rapporto_var = confronta("Varianza", marg_varianza)
    media_mov, std_mov, scarto_mov, rapporto_mov = confronta("Numero Movimenti", marg_mov)
    media_tot, std_tot, scarto_tot, rapporto_tot = confronta("Importo Totale", marg_totale)

    risultati.append({
        "Mese": mese,
        "Categoria": cat,
        "Dettaglio": dett,
        "Entropia Marginale": marg_entropia,
        "Entropia Media Storica": media_ent,
        "Entropia Std": std_ent,
        "Entropia Scarto": scarto_ent,
        "Entropia Rapporto": rapporto_ent,
        "Varianza Marginale": marg_varianza,
        "Varianza Media Storica": media_var,
        "Varianza Std": std_var,
        "Varianza Scarto": scarto_var,
        "Varianza Rapporto": rapporto_var,
        "N. Movimenti Marginale": marg_mov,
        "N. Movimenti Storico": media_mov,
        "N. Movimenti Std": std_mov,
        "N. Movimenti Scarto": scarto_mov,
        "N. Movimenti Rapporto": rapporto_mov,
        "Importo Totale Marginale": marg_totale,
        "Importo Totale Storico": media_tot,
        "Importo Totale Std": std_tot,
        "Importo Totale Scarto": scarto_tot,
        "Importo Totale Rapporto": rapporto_tot,
    })

# Esporta il file completo
df_out = pd.DataFrame(risultati)
df_out.to_csv("analisi_completa_anomalie.csv", index=False)

print("✅ Analisi completa salvata in 'analisi_completa_anomalie.csv'")
input("Premi INVIO per chiudere...")
