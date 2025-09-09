import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ============== CONFIG ==============
INPUT_CSV      = "./dataset/registro_cassa_clean.csv"
OUT_DIR_TABLES = "./eda_out"
OUT_DIR_PLOTS  = "./eda_plots"
SEP            = ";"   
# ====================================

def ensure_dirs():
    os.makedirs(OUT_DIR_TABLES, exist_ok=True)
    os.makedirs(OUT_DIR_PLOTS, exist_ok=True)

def read_data(path):
    # Legge tutto come stringa per sicurezza, poi converte
    df = pd.read_csv(path, sep=SEP, dtype=str)
    # Colonne attese (se mancano, verranno semplicemente ignorate nei calcoli specifici)
    expected = [
        "risorsa","tipologia_risorsa","tipologia_movimento","importo","data",
        "passaggio_fondi","categoria","categoria_dettaglio"
    ]
    # Normalizza nomi (minuscolo)
    df.columns = [c.strip().lower() for c in df.columns]

    # Importo -> float (punto decimale atteso)
    if "importo" in df.columns:
        df["importo"] = (
            df["importo"]
            .str.replace(" ", "", regex=False)
            .str.replace(",", ".", regex=False)  # safety: se per caso è rimasta la virgola
        )
        df["importo"] = pd.to_numeric(df["importo"], errors="coerce")

    # Data -> datetime (YYYY-MM-DD atteso, ma tollera dayfirst)
    if "data" in df.columns:
        df["data"] = pd.to_datetime(df["data"], errors="coerce", dayfirst=True)
        
    # Distribuzione valori di tipologia_movimento (se esiste)
    if "tipologia_movimento" in df.columns:
        movimento_counts = df["tipologia_movimento"].value_counts(dropna=False)
        movimento_counts.to_csv(os.path.join(OUT_DIR_TABLES, "tipologia_movimento_counts.csv"))

    return df

def tables_summary(df):
    # Dimensione & dtypes
    shape_info = {"rows": int(df.shape[0]), "cols": int(df.shape[1])}
    dtypes = df.dtypes.astype(str).to_dict()

    # Missing per colonna
    missing = df.isna().sum().sort_values(ascending=False).rename("missing")

    # Statistiche numeriche su importo (se esiste)
    num_stats = pd.DataFrame()
    if "importo" in df.columns:
        desc = df["importo"].describe(percentiles=[0.01,0.05,0.25,0.5,0.75,0.95,0.99]).to_frame("importo")
        num_stats = desc

    # Cardinalità (valori unici) per categoriche principali
    cat_cols = [c for c in ["risorsa","tipologia_risorsa","tipologia_movimento","passaggio_fondi","categoria","categoria_dettaglio"] if c in df.columns]
    cardinality = pd.Series({c: int(df[c].nunique(dropna=True)) for c in cat_cols}, name="unique_values").sort_values(ascending=False)

    # Salvataggi
    pd.DataFrame([shape_info]).to_csv(os.path.join(OUT_DIR_TABLES, "shape.csv"), index=False)
    pd.Series(dtypes, name="dtype").to_csv(os.path.join(OUT_DIR_TABLES, "dtypes.csv"))
    missing.to_csv(os.path.join(OUT_DIR_TABLES, "missing_per_column.csv"))
    if not num_stats.empty:
        num_stats.to_csv(os.path.join(OUT_DIR_TABLES, "numeric_stats_importo.csv"))
    cardinality.to_csv(os.path.join(OUT_DIR_TABLES, "categorical_cardinality.csv"))

    # Anche un JSON riassuntivo
    summary_json = {
        "shape": shape_info,
        "dtypes": dtypes,
        "top_missing_columns": missing.head(10).to_dict(),
        "categorical_cardinality": cardinality.to_dict()
    }
    with open(os.path.join(OUT_DIR_TABLES, "summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary_json, f, ensure_ascii=False, indent=2)

def plot_save(fig, name):
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR_PLOTS, name), dpi=120)
    plt.close(fig)

def plots(df):
    # 1) Distribuzione importi (hist)
    if "importo" in df.columns and df["importo"].notna().any():
        vals = df["importo"].dropna().values
        # Histogram (clip per robustezza a code molto lunghe)
        q99 = np.nanpercentile(vals, 99)
        vals_clip = np.clip(vals, np.nanmin(vals), q99)

        fig = plt.figure()
        plt.hist(vals_clip, bins=50)
        plt.title("Distribuzione Importi (clippata al 99° percentile)")
        plt.xlabel("importo")
        plt.ylabel("frequenza")
        plot_save(fig, "01_hist_importo.png")

        # Boxplot
        fig = plt.figure()
        plt.boxplot(vals, vert=True, showfliers=True)
        plt.title("Boxplot Importi")
        plt.ylabel("importo")
        plot_save(fig, "02_boxplot_importo.png")

    # 2) Serie temporale: somma importi per mese
    if "data" in df.columns and df["data"].notna().any() and "importo" in df.columns:
        tmp = df.dropna(subset=["data"]).copy()
        tmp["year_month"] = tmp["data"].dt.to_period("M").astype(str)
        monthly = tmp.groupby("year_month", as_index=False)["importo"].sum().sort_values("year_month")
        monthly.to_csv(os.path.join(OUT_DIR_TABLES, "monthly_totals.csv"), index=False)

        fig = plt.figure()
        plt.plot(monthly["year_month"], monthly["importo"], marker="o")
        plt.title("Importo totale per mese")
        plt.xlabel("mese")
        plt.ylabel("somma importi")
        plt.xticks(rotation=45, ha="right")
        plot_save(fig, "03_timeseries_importo_mensile.png")

    # 3) Top categorie
    if "categoria" in df.columns:
        top_cat = df["categoria"].value_counts(dropna=False).head(20)
        fig = plt.figure(figsize=(8,6))
        top_cat.sort_values().plot(kind="barh")
        plt.title("Top categorie (conteggi)")
        plt.xlabel("conteggio")
        plot_save(fig, "04_bar_top_categorie.png")

    if "categoria_dettaglio" in df.columns:
        top_det = df["categoria_dettaglio"].value_counts(dropna=False).head(20)
        fig = plt.figure(figsize=(8,6))
        top_det.sort_values().plot(kind="barh")
        plt.title("Top categorie dettaglio (conteggi)")
        plt.xlabel("conteggio")
        plot_save(fig, "05_bar_top_categorie_dettaglio.png")

    # 4) Top risorse / tipologia_risorsa
    if "risorsa" in df.columns:
        top_ris = df["risorsa"].value_counts(dropna=False).head(20)
        fig = plt.figure(figsize=(8,6))
        top_ris.sort_values().plot(kind="barh")
        plt.title("Top risorse (conteggi)")
        plt.xlabel("conteggio")
        plot_save(fig, "06_bar_top_risorse.png")

    if "tipologia_risorsa" in df.columns:
        top_tr = df["tipologia_risorsa"].value_counts(dropna=False).head(20)
        fig = plt.figure(figsize=(8,6))
        top_tr.sort_values().plot(kind="barh")
        plt.title("Top tipologie risorsa (conteggi)")
        plt.xlabel("conteggio")
        plot_save(fig, "07_bar_top_tipologia_risorsa.png")

    # 5) Importo per categoria (somma) - top 20
    if "categoria" in df.columns and "importo" in df.columns:
        grp = df.groupby("categoria", dropna=False)["importo"].sum().sort_values(ascending=False).head(20)
        fig = plt.figure(figsize=(8,6))
        grp.sort_values().plot(kind="barh")
        plt.title("Somma importi per categoria (top 20)")
        plt.xlabel("somma importi")
        plot_save(fig, "08_bar_importi_per_categoria.png")
        
    # 6) Top tipologia_movimento
    if "tipologia_movimento" in df.columns:
        top_tm = df["tipologia_movimento"].value_counts(dropna=False).head(20)
        fig = plt.figure(figsize=(8,6))
        top_tm.sort_values().plot(kind="barh")
        plt.title("Top tipologie movimento (conteggi)")
        plt.xlabel("conteggio")
        plot_save(fig, "09_bar_top_tipologia_movimento.png")


def main():
    ensure_dirs()
    df = read_data(INPUT_CSV)
    tables_summary(df)
    plots(df)
    print(f"[EDA] Completata.\n- Tabelle in: {OUT_DIR_TABLES}\n- Grafici in: {OUT_DIR_PLOTS}")

if __name__ == "__main__":
    main()
