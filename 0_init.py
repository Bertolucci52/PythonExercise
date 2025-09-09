import pandas as pd
import numpy as np

# ======== CONFIG RAPIDA ========
INPUT_CSV  = "./dataset/registro_cassa.csv"
OUTPUT_CSV = "./dataset/registro_cassa_clean.csv"
# ===============================

# Mappatura colonne originali -> standard
RENAME_MAP = {
    "risorsa": "risorsa",
    "tipologia_risorsa": "tipologia_risorsa",
    "tipologia_movimento": "tipologia_movimento",
    "importo_movimento": "importo",
    "data_movimento": "data",
    "passaggio_fondi": "passaggio_fondi",
    "categoria": "categoria",
    "categoria_dettaglio": "categoria_dettaglio"
}

MIN_YEAR = 2015

def main():
    # Leggi CSV in formato europeo
    df = pd.read_csv(INPUT_CSV, sep=";", decimal=",", dtype=str)
    total_in = len(df)

    # Rinomina le colonne in snake_case (o standard)
    df = df.rename(columns={old: new for old, new in RENAME_MAP.items() if old in df.columns})

    # Normalizza importo
    if "importo" in df.columns:
        df["importo"] = (
            df["importo"]
            .str.replace(" ", "", regex=False)   # rimuove spazi
            .str.replace(".", "", regex=False)   # rimuove eventuali punti residui
            .str.replace(",", ".", regex=False)  # converte virgola in punto
        )
        df["importo"] = pd.to_numeric(df["importo"], errors="coerce")

    # Normalizza data e filtra per anno minimo
    removed_by_year = 0
    if "data" in df.columns:
        df["data"] = pd.to_datetime(df["data"], errors="coerce", dayfirst=True)

        before_filter = len(df)
        df = df[df["data"].dt.year >= MIN_YEAR].copy()  # tiene solo dal 2015 in poi
        removed_by_year = before_filter - len(df)

        # Torna a stringa (ISO format)
        df["data"] = df["data"].dt.strftime("%Y-%m-%d")

    # === FILTRO RICHIESTO: tieni solo passaggio_fondi == 0 ===
    kept_pf0 = len(df)
    if "passaggio_fondi" in df.columns:
        # prova a convertire a numerico (NaN se non interpretabile)
        pf = pd.to_numeric(df["passaggio_fondi"], errors="coerce")
        df = df[pf == 0].copy()
    kept_pf0 = len(df)

    # Elimina righe completamente vuote (ma NON i duplicati)
    df = df.dropna(how="all")

    # Salva CSV pulito
    df.to_csv(OUTPUT_CSV, sep=";", decimal=",", index=False)

    print(f"[INIT] File pulito salvato in: {OUTPUT_CSV}")
    print(f"[INIT] Righe input: {total_in}")
    print(f"[INIT] Escluse perché antecedenti al {MIN_YEAR} (o data non interpretabile): {removed_by_year}")
    print(f"[INIT] Righe output (solo passaggio_fondi == 0): {len(df)} | Colonne: {len(df.columns)}")
    print("[NOTE] Nessuna rimozione di duplicati eseguita.")

if __name__ == "__main__":
    main()
