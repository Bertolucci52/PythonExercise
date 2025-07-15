import pandas as pd
from scipy.stats import entropy
import numpy as np


def calcola_entropia(valori):
    if len(valori) == 0 or valori.sum() == 0:
        return None
    if len(set(valori)) == 1:
        return 0.0
    probabilità = valori / valori.sum()
    return entropy(probabilità, base=2)


def verifica_condizioni(df, categoria, dettaglio, condizioni):
    risultati = []
    df_filtro = df[
        (df["CashFlow - Categoria"] == categoria) &
        (df["CashFlow - Dettaglio"] == dettaglio)
    ].copy()
    df_filtro["Anno"] = df_filtro["Data Movimento"].dt.year
    df_filtro["Mese"] = df_filtro["Data Movimento"].dt.to_period("M")

    if "numero_movimenti_mensili_max" in condizioni:
        mov_mese = df_filtro[df_filtro["Importo"] < 0].groupby("Mese").size()
        violazioni = mov_mese[mov_mese > condizioni["numero_movimenti_mensili_max"]]
        if not violazioni.empty:
            risultati.append(f"❌ Troppe uscite mensili: {violazioni.to_dict()}")

    if "numero_movimenti_mensili_entrate_max" in condizioni:
        mov_mese = df_filtro[(df_filtro["Importo"] > 0) & (df_filtro["Passaggio Fondi"] == "Si")].groupby("Mese").size()
        violazioni = mov_mese[mov_mese > condizioni["numero_movimenti_mensili_entrate_max"]]
        if not violazioni.empty:
            risultati.append(f"❌ Troppe entrate mensili PF: {violazioni.to_dict()}")

    if "totale_uscite_attese" in condizioni:
        uscite_mese = df_filtro[df_filtro["Importo"] < 0].groupby("Mese")["Importo"].sum()
        violazioni = uscite_mese[round(uscite_mese, 2) != condizioni["totale_uscite_attese"]]
        if not violazioni.empty:
            risultati.append(f"❌ Uscite mensili anomale: {violazioni.to_dict()}")

    if "totale_entrate_annue_pf" in condizioni:
        entrate_anno = df_filtro[(df_filtro["Importo"] > 0) & (df_filtro["Passaggio Fondi"] == "Si")].groupby("Anno")["Importo"].sum()
        violazioni = entrate_anno[round(entrate_anno, 2) != condizioni["totale_entrate_annue_pf"]]
        if not violazioni.empty:
            risultati.append(f"❌ Entrate annuali PF anomale: {violazioni.to_dict()} - Gli stipendi hanno richiesto movimentazioni di risorse straordinarie")

    if "movimenti_annui_entrate_max" in condizioni:
        entrate_anno = df_filtro[df_filtro["Importo"] > 0].groupby("Anno").size()
        violazioni = entrate_anno[entrate_anno > condizioni["movimenti_annui_entrate_max"]]
        if not violazioni.empty:
            risultati.append(f"❌ Troppe entrate annue: {violazioni.to_dict()} - Sono stati richiesti conferimenti di capitale straordinario")

    if "soglia_massima_mensile" in condizioni:
        uscite_mese = df_filtro[df_filtro["Importo"] < 0].groupby("Mese")["Importo"].sum()
        violazioni = uscite_mese[uscite_mese < condizioni["soglia_massima_mensile"]]
        if not violazioni.empty:
            risultati.append(f"❌ Superata soglia mensile: {violazioni.to_dict()}")

    return risultati


df = pd.read_csv("../1/registro_cassa.csv", sep=";", encoding="ISO-8859-1")
df["Importo"] = df["Importo"].str.replace(",", ".").astype(float).round(2)
df["Data Movimento"] = pd.to_datetime(df["Data Movimento"], format="%d/%m/%Y")
df["Mese"] = df["Data Movimento"].dt.to_period("M")

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
    entropia_val = calcola_entropia(valori)
    if entropia_val is not None:
        risultati_saldi_dettagli.append({
            "Categoria": categoria,
            "Dettaglio": dettaglio,
            "Entropia Saldo": round(entropia_val, 4)
        })

df_entropie_saldo_dettagli = pd.DataFrame(risultati_saldi_dettagli).sort_values(
    by=["Categoria", "Entropia Saldo"], ascending=[True, False]
)

print("\nEntropia del saldo per ciascun dettaglio:")
print(df_entropie_saldo_dettagli.head(10))

# Entrate pure
df_entrate_pure = df[(df["Importo"] > 0) & (df["Passaggio Fondi"] == "No")]

# Entrate da trasferimenti interni
df_entrate_trasf = df[(df["Importo"] > 0) &
                      (df["Passaggio Fondi"] == "Si") &
                      (df["CashFlow - Categoria"] != "Finanziamenti")]

# Uscite
df_uscite = df[(df["Importo"] < 0) & (df["Passaggio Fondi"] == "No")]

# Risultati
risultati_entrate_uscite = []

for _, riga in dettagli_saldi.iterrows():
    categoria = riga["CashFlow - Categoria"]
    dettaglio = riga["CashFlow - Dettaglio"]

    # Entrate pure
    subset_pure = df_entrate_pure[
        (df_entrate_pure["CashFlow - Categoria"] == categoria) &
        (df_entrate_pure["CashFlow - Dettaglio"] == dettaglio)
    ]
    valori_pure = subset_pure.groupby("Mese")["Importo"].sum().abs().values
    entropia_pure = calcola_entropia(valori_pure)
    if entropia_pure is not None:
        risultati_entrate_uscite.append({
            "Categoria": categoria,
            "Dettaglio": dettaglio,
            "Tipo": "Entrata (No PF)",
            "Entropia": round(entropia_pure, 4)
        })

    # Entrate trasferimenti
    subset_trasf = df_entrate_trasf[
        (df_entrate_trasf["CashFlow - Categoria"] == categoria) &
        (df_entrate_trasf["CashFlow - Dettaglio"] == dettaglio)
    ]
    valori_trasf = subset_trasf.groupby("Mese")["Importo"].sum().abs().values
    entropia_trasf = calcola_entropia(valori_trasf)
    if entropia_trasf is not None:
        risultati_entrate_uscite.append({
            "Categoria": categoria,
            "Dettaglio": dettaglio,
            "Tipo": "Entrata (PF)",
            "Entropia": round(entropia_trasf, 4)
        })

    # Uscite
    subset_uscite = df_uscite[
        (df_uscite["CashFlow - Categoria"] == categoria) &
        (df_uscite["CashFlow - Dettaglio"] == dettaglio)
    ]
    valori_uscite = subset_uscite.groupby("Mese")["Importo"].sum().abs().values
    entropia_uscita = calcola_entropia(valori_uscite)
    if entropia_uscita is not None:
        risultati_entrate_uscite.append({
            "Categoria": categoria,
            "Dettaglio": dettaglio,
            "Tipo": "Uscita",
            "Entropia": round(entropia_uscita, 4)
        })

# Ordina e salva il DataFrame
df_entropie_entrate_uscite = pd.DataFrame(risultati_entrate_uscite).sort_values(
    by=["Categoria", "Dettaglio", "Tipo"]
)

print("--------------------------------------------------------------------------")
print(df_entropie_entrate_uscite.head(50))

# Filtra solo risultati con entropia superiore alla soglia
soglia_entropia = 2.3
df_entropie_filtrate = df_entropie_entrate_uscite[df_entropie_entrate_uscite["Entropia"] > soglia_entropia]

# Visualizza
print("--------------------------------------------------------------------------")
print("\n\U0001f4a1 Dettagli con entropia significativa (> 2.3):")
print(df_entropie_filtrate)

condizioni_where = {    
    ("Finanziamenti", "Conferimento quota capitale"): {
        "movimenti_annui_entrate_max": 2
    },
    ("Finanziamenti", "Prestito bancario"): {
        "movimenti_annui_entrate_max": 1,
        "numero_movimenti_mensili_max": 1
    },
    ("Amministrazione", "Stipendi"): {
        "numero_movimenti_mensili_max": 1,
        "totale_uscite_attese": -8200.00,
        "numero_movimenti_mensili_entrate_max": 2,
        "totale_entrate_annue_pf": 100000.00
    },
    ("Reparti Operativi",): {
        "condizione_custom": "variabilità attesa → nessuna where (anomalia plausibile)"
    },
    ("Logistica", "Auto Aziendali"): {
        "soglia_massima_mensile": -1000.00
    }
}

# Iterazione
print("--------------------------------------------------------------------------")
print("\nAnalisi condizioni where per ogni dettaglio con entropia alta:")
for _, riga in df_entropie_filtrate.iterrows():
    categoria = riga["Categoria"]
    dettaglio = riga["Dettaglio"]

    chiave_completa = (categoria, dettaglio)
    chiave_categoria = (categoria,)
    condizioni = condizioni_where.get(chiave_completa) or condizioni_where.get(chiave_categoria)

    if condizioni:
        print(f"\n\U0001F50D {categoria} → {dettaglio}")
        for k, v in condizioni.items():
            print(f" - {k}: {v}")

        violazioni = verifica_condizioni(df, categoria, dettaglio, condizioni)
        if violazioni:
            for v in violazioni:
                print(v)
        else:
            print(" ✅ Tutte le condizioni rispettate")
    else:
        print(f"\n{categoria} → {dettaglio} → Nessuna condizione definita")

# Inizializza lista per raccogliere tutte le violazioni
violazioni_complessive = []

# Iterazione sulle entropie significative
print("--------------------------------------------------------------------------")
print("\nAnalisi condizioni where per ogni dettaglio con entropia alta:")
for _, riga in df_entropie_filtrate.iterrows():
    categoria = riga["Categoria"]
    dettaglio = riga["Dettaglio"]
    tipo = riga["Tipo"]
    entropia = riga["Entropia"]

    chiave_completa = (categoria, dettaglio)
    chiave_categoria = (categoria,)
    condizioni = condizioni_where.get(chiave_completa) or condizioni_where.get(chiave_categoria)

    if condizioni:
        print(f"\n🔍 {categoria} → {dettaglio} ({tipo})")
        for k, v in condizioni.items():
            print(f" - {k}: {v}")

        violazioni = verifica_condizioni(df, categoria, dettaglio, condizioni)

        if violazioni:
            for v in violazioni:
                violazioni_complessive.append({
                    "Categoria": categoria,
                    "Dettaglio": dettaglio,
                    "Tipo": tipo,
                    "Entropia": entropia,
                    "Esito": "Anomalia",
                    "Violazione": v
                })
                print(v)
        else:
            violazioni_complessive.append({
                "Categoria": categoria,
                "Dettaglio": dettaglio,
                "Tipo": tipo,
                "Entropia": entropia,
                "Esito": "Ok",
                "Violazione": "-"
            })
            print("✅ Tutte le condizioni rispettate")
    else:
        print(f"\n{categoria} → {dettaglio} ({tipo}) → Nessuna condizione definita")


# Salva il riepilogo delle anomalie in un file CSV
df_violazioni = pd.DataFrame(violazioni_complessive)
df_violazioni.to_csv("violazioni_anomalie.csv", index=False)

print("\n📁 File 'violazioni_anomalie.csv' salvato con successo!")
print(df_violazioni.head())