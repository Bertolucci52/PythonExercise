import os
import numpy as np
import pandas as pd

# ========= CONFIG RAPIDA =========
INPUT_CSV  = "./dataset/registro_cassa_clean.csv"
OUTPUT_CSV = "./dataset/registro_cassa_classi.csv"
SEP        = ";"          
BINS_K     = 6            
METHOD     = "quantile"   
AMOUNT_COL_CANDIDATES = ["importo_movimento", "importo"]
DATE_COL_CANDIDATES   = ["data_movimento", "data"]
# =================================

def find_col(cols, candidates):
    for c in candidates:
        if c in cols:
            return c
    return None

def coerce_amount(s: pd.Series) -> pd.Series:
    """Converte importi con possibili migliaia '.' e decimali ',' in float."""
    s = s.astype(str).str.replace(" ", "", regex=False)
    s = s.str.replace(".", "", regex=False)   # rimuovi separatore migliaia
    s = s.str.replace(",", ".", regex=False)  # virgola -> punto
    return pd.to_numeric(s, errors="coerce")

def parse_date(series: pd.Series) -> pd.Series:
    """Parsa le date provando ISO (YYYY-MM-DD) e poi day-first."""
    d = pd.to_datetime(series, errors="coerce", format="%Y-%m-%d")
    if d.isna().all():
        d = pd.to_datetime(series, errors="coerce", dayfirst=True)
    return d

def main():
    os.makedirs(os.path.dirname(OUTPUT_CSV) or ".", exist_ok=True)

    # ---- lettura ----
    df = pd.read_csv(INPUT_CSV, sep=SEP, dtype=str, low_memory=False)

    # ---- importo -> classi (sextili) ----
    amt_col = find_col(df.columns, AMOUNT_COL_CANDIDATES)
    if amt_col is not None:
        amt = coerce_amount(df[amt_col])
        mask = amt.notna()
        if mask.any():
            if METHOD == "quantile":
                # qcut con gestione duplicati e possibile riduzione K
                try:
                    cats, bins = pd.qcut(
                        amt[mask],
                        q=BINS_K,
                        labels=list(range(1, BINS_K+1)),
                        retbins=True,
                        duplicates="drop"
                    )
                except ValueError:
                    uniq = amt[mask].nunique()
                    k_adj = max(2, min(BINS_K, uniq))
                    cats, bins = pd.qcut(
                        amt[mask],
                        q=k_adj,
                        labels=list(range(1, k_adj+1)),
                        retbins=True,
                        duplicates="drop"
                    )
                df.loc[mask, "classe_importo_id"] = cats.astype("Int64")
                df.loc[mask, "classe_importo_interval"] = pd.cut(
                    amt[mask], bins=bins, include_lowest=True
                ).astype(str)

            elif METHOD == "uniform":
                vmin, vmax = float(amt[mask].min()), float(amt[mask].max())
                bins = np.linspace(vmin, vmax, BINS_K + 1)
                df.loc[mask, "classe_importo_id"] = pd.cut(
                    amt[mask], bins=bins, labels=list(range(1, BINS_K+1)), include_lowest=True
                ).astype("Int64")
                df.loc[mask, "classe_importo_interval"] = pd.cut(
                    amt[mask], bins=bins, include_lowest=True
                ).astype(str)
            else:
                raise ValueError("METHOD non valido. Usa 'quantile' o 'uniform'.")
        else:
            print("[WARN] Nessun importo valido: classi importo non create.")
    else:
        print(f"[WARN] Colonna importo non trovata (attese: {AMOUNT_COL_CANDIDATES}).")

    # ---- date -> anno, mese, anno_mese ----
    date_col = find_col(df.columns, DATE_COL_CANDIDATES)
    if date_col is not None:
        d = parse_date(df[date_col])
        df["anno"]      = d.dt.year.astype("Int64")
        df["mese"]      = d.dt.month.astype("Int64")
        # anno_mese come stringa YYYY-MM per entropia mensile
        df["anno_mese"] = d.dt.to_period("M").astype(str)
    else:
        print(f"[WARN] Colonna data non trovata (attese: {DATE_COL_CANDIDATES}).")
        
    # --- drop importo e data ---
    date_col = find_col(df.columns, DATE_COL_CANDIDATES)
    amt_col  = find_col(df.columns, AMOUNT_COL_CANDIDATES)

    to_drop = []
    if date_col: 
        to_drop.append(date_col)
    if amt_col: 
        to_drop.append(amt_col)

    if to_drop:
        df.drop(columns=to_drop, inplace=True, errors="ignore")
        print(f"[CLASSI] Colonne eliminate: {to_drop}")    

    # ---- salvataggio ----
    df.to_csv(OUTPUT_CSV, sep=SEP, index=False)

    # ---- log sintetico ----
    n_rows = len(df)
    n_binned = df["classe_importo_id"].notna().sum() if "classe_importo_id" in df.columns else 0
    print("[CLASSI] Completato.")
    print(f"  Input : {INPUT_CSV}")
    print(f"  Output: {OUTPUT_CSV}")
    print(f"  Righe : {n_rows}")
    if "classe_importo_id" in df.columns:
        print(f"  Classi importo ({METHOD}, K={BINS_K}) assegnate a {n_binned}/{n_rows} righe.")
    if "anno" in df.columns:
        print("  Campi temporali creati: anno, mese, anno_mese")

if __name__ == "__main__":
    main()
