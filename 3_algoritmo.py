# algoritmo_v2.py
# ============================================================
# Rilevazione anomalie con entropia di Shannon
# Livello 0 riscritto con:
#  - vocabolario fisso per categoria (union delle classi storiche)
#  - NA in classe_importo_id ignorati nei calcoli, con logging
#  - nessuna rimozione di movimenti dal dataset originale
# ============================================================

import os
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
from math import log2

# ================= CONFIG =================
INPUT_CSV        = "./dataset/registro_cassa_classi.csv"
INPUT_CSV_RAW    = "./dataset/registro_cassa_clean.csv"   # servira' da Livello 2
SEP              = ";"

Y                = "classe_importo_id"
X                = "categoria_dettaglio"
COL_ANNO         = "anno"
COL_YM           = "anno_mese"

ALPHA            = 1.0      # Laplace smoothing
THRESH           = 0.01     # soglia su |ΔHn| per attivare il drill-down (Livello 1)

# Parametri Livello 2 (placeholder, non usati in questo step)
THRESH_N_BURST_RATIO   = 2.0
THRESH_AMT_SPIKE_RATIO = 2.0
MIN_N_MISSING_BASE     = 6

# Output
OUT_LIV_0   = "./dataset/entropia_liv_0_categoria_annuale.csv"
OUT_LIV_1   = "./dataset/entropia_liv_1_mese_anno.csv"      # verrà scritto quando implementiamo il Livello 1
OUT_LIV_2   = "./dataset/entropia_liv_2_anomalie.csv"       # verrà scritto quando implementiamo il Livello 2
# =========================================


# ============== UTILS ENTROPIA ==============

def _entropy_from_probs(p: np.ndarray) -> float:
    """Entropia di Shannon (base 2) da un array di probabilita' (p_i >= 0, somma=1)."""
    p = p[p > 0]
    if p.size == 0:
        return 0.0
    return float(-(p * np.log2(p)).sum())

def entropy_on_vocab(series: pd.Series, vocab: List[str], alpha: float = 1.0) -> float:
    """
    Entropia con Laplace smoothing calcolata su un vocabolario fisso.
    - I NA vengono ignorati (NON vengono rimossi dal DataFrame chiamante).
    - Il conteggio usa solo le etichette in `vocab`.
    """
    s = series.dropna().astype(str)
    vc = s.value_counts()
    counts = np.array([vc.get(c, 0.0) for c in vocab], dtype=float)
    k = len(vocab)
    probs = (counts + alpha) / (counts.sum() + alpha * k)
    return _entropy_from_probs(probs)

def normalized_on_vocab(series: pd.Series, vocab: List[str], alpha: float = 1.0) -> float:
    """Entropia normalizzata H/log2(k) su vocabolario fisso."""
    k = len(vocab)
    if k <= 1:
        return 0.0
    H = entropy_on_vocab(series, vocab, alpha=alpha)
    return H / log2(k)


# ============== LIVELLO 0 ==============

def build_vocab_per_category(df: pd.DataFrame, cat_col: str, y_col: str) -> Dict[str, List[str]]:
    """
    Per ogni categoria, costruisce il vocabolario (unione) delle classi osservate su tutta la storia.
    I NA in y_col NON entrano nel vocabolario.
    """
    vocab_map: Dict[str, List[str]] = {}
    for cat, sub in df.groupby(cat_col):
        vocab = sorted(sub[y_col].dropna().astype(str).unique().tolist())
        vocab_map[str(cat)] = vocab
    return vocab_map

def livello0_compute(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Calcola:
      - baseline per categoria (H_base, Hn_base)
      - serie annuale per (categoria, anno) e ΔHn vs baseline
    Restituisce (base_df, merged_year).
    """
    # Logging NA in Y (informativo; NON rimuoviamo righe dal df)
    total_na_y = int(df[Y].isna().sum()) if Y in df.columns else 0
    print(f"[Liv0] NA in {Y} (ignorati nei calcoli entropici, dati NON rimossi): {total_na_y}")

    # Vocabolario fisso per categoria
    vocab_map = build_vocab_per_category(df, X, Y)

    # Baseline per categoria
    baselines = []
    for cat, sub in df.groupby(X):
        vocab = vocab_map[str(cat)]
        Hn = normalized_on_vocab(sub[Y], vocab, alpha=ALPHA)
        H  = entropy_on_vocab(sub[Y], vocab, alpha=ALPHA)
        baselines.append((cat, len(vocab), H, Hn, len(sub)))
    base_df = pd.DataFrame(baselines, columns=[X, "k_vocab", "H_base", "Hn_base", "N_tot"])

    # Serie annuale
    yearly = []
    for (cat, yr), sub in df.groupby([X, COL_ANNO]):
        vocab = vocab_map[str(cat)]
        Hn = normalized_on_vocab(sub[Y], vocab, alpha=ALPHA)
        H  = entropy_on_vocab(sub[Y], vocab, alpha=ALPHA)
        yearly.append((cat, yr, len(vocab), H, Hn, len(sub), int(sub[Y].isna().sum())))
    yearly_df = pd.DataFrame(yearly, columns=[X, COL_ANNO, "k_vocab", "H", "Hn", "N", "N_na_ignored"])

    # ΔHn vs baseline
    merged_year = yearly_df.merge(base_df[[X, "H_base", "Hn_base"]], on=X, how="left")
    merged_year["delta_Hn"] = merged_year["Hn"] - merged_year["Hn_base"]

    return base_df, merged_year

def livello0_save_outputs(base_df: pd.DataFrame, merged_year: pd.DataFrame) -> pd.DataFrame:
    """Salva OUT_LIV_0 e ritorna il subset che supera la soglia per il drill-down."""
    os.makedirs(os.path.dirname(OUT_LIV_0) or ".", exist_ok=True)
    merged_year.to_csv(OUT_LIV_0, sep=SEP, index=False)
    print(f"[Liv0] Salvato livello annuale: {OUT_LIV_0} (righe: {len(merged_year)})")

    # Selezione coppie per il Livello 1
    to_drill = merged_year.loc[merged_year["delta_Hn"].abs() > THRESH].copy()
    print(f"[Liv0] Coppie (categoria,anno) che superano soglia |ΔHn|>{THRESH}: {len(to_drill)}")
    return to_drill


# ============== LIVELLO 1 (STUB) ==============

def livello1_drilldown_mensile(
    df: pd.DataFrame,
    base_df: pd.DataFrame,
    to_drill: pd.DataFrame,
    merged_year: pd.DataFrame,
) -> pd.DataFrame:
    """
    Drill-down mensile per le sole coppie (categoria, anno) selezionate da Livello 0,
    usando lo stesso vocabolario fisso per categoria del Livello 0.
    - Ignora NA in Y nei calcoli (non rimuove righe dal df)
    - Calcola entrambe le differenze:
        * delta_Hn_month_vs_base = Hn_mese - Hn_base (storico categoria)
        * delta_Hn_month_vs_year = Hn_mese - Hn_anno (contestuale all'anno)
    - Riporta anche delta_Hn_year (dal Livello 0) per contesto.
    """
    # Schema di output
    out_cols = [
        X, COL_ANNO, COL_YM, "N",
        "H", "Hn",
        "H_base", "Hn_base",
        "Hn_year",
        "delta_Hn_month_vs_base",
        "delta_Hn_month_vs_year",
        "delta_Hn_year",
    ]

    if to_drill.empty:
        pd.DataFrame(columns=out_cols).to_csv(OUT_LIV_1, sep=SEP, index=False)
        print(f"[Liv1] Nessuna coppia da analizzare. Creato file vuoto: {OUT_LIV_1}")
        return pd.DataFrame(columns=out_cols)

    # Vocabolario fisso per categoria (come Livello 0)
    vocab_map = build_vocab_per_category(df, X, Y)

    # Mappe di supporto
    base_map = base_df.set_index(X)[["H_base", "Hn_base"]].to_dict("index")
    year_Hn_map = merged_year.set_index([X, COL_ANNO])["Hn"].to_dict()
    year_delta_map = merged_year.set_index([X, COL_ANNO])["delta_Hn"].to_dict()

    # Tipi coerenti per join robusti
    df[X] = df[X].astype(str)
    df[COL_ANNO] = df[COL_ANNO].astype(str)
    df[COL_YM] = df[COL_YM].astype(str)
    to_drill[X] = to_drill[X].astype(str)
    to_drill[COL_ANNO] = to_drill[COL_ANNO].astype(str)

    rows = []
    # Loop sulle coppie (categoria, anno) oltre soglia
    for cat, yr in to_drill[[X, COL_ANNO]].drop_duplicates().itertuples(index=False, name=None):
        sub_year = df[(df[X] == cat) & (df[COL_ANNO] == yr)]
        vocab = vocab_map.get(cat, [])

        # Recupero baseline e anno
        Hb  = base_map.get(cat, {}).get("H_base", np.nan)
        Hnb = base_map.get(cat, {}).get("Hn_base", np.nan)
        Hn_year = year_Hn_map.get((cat, yr), np.nan)
        dHn_year = year_delta_map.get((cat, yr), np.nan)

        # Per ogni mese dell'anno selezionato
        for ym, sub_month in sub_year.groupby(COL_YM):
            # Entropia su vocabolario fisso, NA ignorati
            H  = entropy_on_vocab(sub_month[Y], vocab, alpha=ALPHA)
            Hn = normalized_on_vocab(sub_month[Y], vocab, alpha=ALPHA)

            dHn_vs_base = Hn - Hnb if pd.notna(Hn) and pd.notna(Hnb) else np.nan
            dHn_vs_year = Hn - Hn_year if pd.notna(Hn) and pd.notna(Hn_year) else np.nan

            rows.append((
                cat, yr, ym, len(sub_month),
                H, Hn,
                Hb, Hnb,
                Hn_year,
                dHn_vs_base,
                dHn_vs_year,
                dHn_year,
            ))

    out_df = (
        pd.DataFrame(rows, columns=out_cols)
          .sort_values([X, COL_ANNO, COL_YM])
          .reset_index(drop=True)
    )

    os.makedirs(os.path.dirname(OUT_LIV_1) or ".", exist_ok=True)
    out_df.to_csv(OUT_LIV_1, sep=SEP, index=False)
    print(f"[Liv1] Salvato drill-down mensile con doppi confronti: {OUT_LIV_1} (righe: {len(out_df)})")
    return out_df

# ============== LIVELLO 2 (STUB) ==============

# ============== LIVELLO 2 — regole realistiche (coerente con questo file) ==============

def livello2_regole_realistiche(
    to_drill: pd.DataFrame,
    l1_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Livello 2: incrocia mesi sospetti (Livello 0/1) con volumi/importi e "cadenza"
    per classificare le vere anomalie e declassare i comportamenti regolari.
    - Usa il RAW (INPUT_CSV_RAW) per aggregazioni mensili (N_month, sum_abs_month, PF...).
    - Costruisce baseline storiche per categoria e caratterizza la cadenza.
    - Crea una griglia completa (12 mesi) per ogni (categoria, anno) sospetto: così segnala anche mesi mancanti (N=0).
    - Unisce i delta entropici del Livello 1 (vs base e vs anno) se presenti.
    - Applica regole P0–P4 e produce label_liv2, severity, reasons_liv2.
    - Salva OUT_LIV_2 e ritorna il DataFrame finale.
    """

    # ----------------------- Config locali Livello 2 -----------------------
    P_ACTIVE_HIGH = 0.70   # atteso in mese "di stagione"
    P_ACTIVE_LOW  = 0.10   # fuori stagione
    REACTIVATION_GAP = 6   # mesi di inattività per parlare di riattivazione
    ENTROPY_BONUS = 0.30   # soglia per "entropy_shift_support" che aumenta severità
    # banda robusta per importi: tau = max(3*MAD, 0.2*mediana)
    MAD_MULT = 3.0
    REL_BAND = 0.20

    # ----------------------- Helper interni (solo L2) -----------------------
    def _coerce_amount(s: pd.Series) -> pd.Series:
        s = s.astype(str).str.replace(" ", "", regex=False)
        s = s.str.replace(".", "", regex=False).str.replace(",", ".", regex=False)
        return pd.to_numeric(s, errors="coerce")

    def _parse_date(s: pd.Series) -> pd.Series:
        d = pd.to_datetime(s, errors="coerce", format="%Y-%m-%d")
        if d.isna().all():
            d = pd.to_datetime(s, errors="coerce", dayfirst=True)
        return d

    def _to_bool01(x):
        if x is None or (isinstance(x, float) and np.isnan(x)):
            return pd.NA
        s = str(x).strip().lower()
        if s in {"1", "true", "vero", "si", "sì", "y", "yes"}:
            return 1
        if s in {"0", "false", "falso", "no", "n", ""}:
            return 0
        try:
            f = float(s.replace(",", "."))
            if f == 1.0: return 1
            if f == 0.0: return 0
        except:
            pass
        return pd.NA

    def _agg_monthly_raw(raw: pd.DataFrame) -> pd.DataFrame:
        # colonne tempo
        if "anno" not in raw.columns or "anno_mese" not in raw.columns:
            date_col = None
            for c in ["data_movimento", "data", "Data Movimento"]:
                if c in raw.columns:
                    date_col = c
                    break
            if date_col is None:
                raise ValueError("Nel RAW mancano 'anno'/'anno_mese' e non trovo una colonna data.")
            d = _parse_date(raw[date_col])
            raw = raw.copy()
            raw["anno"] = d.dt.year.astype("Int64").astype(str)
            raw["anno_mese"] = d.dt.to_period("M").astype(str)

        # importi
        if "importo_movimento" in raw.columns:
            raw["_importo_num"] = _coerce_amount(raw["importo_movimento"])
        elif "importo" in raw.columns:
            raw["_importo_num"] = _coerce_amount(raw["importo"])
        else:
            raw["_importo_num"] = pd.NA

        # passaggio_fondi
        if "passaggio_fondi" in raw.columns:
            raw["_pf01"] = raw["passaggio_fondi"].apply(_to_bool01).astype("Int64")
        else:
            raw["_pf01"] = pd.NA

        required = ["categoria_dettaglio", "anno", "anno_mese"]
        for c in required:
            if c not in raw.columns:
                raise ValueError(f"Colonna mancante nel RAW per aggregazione: {c}")

        def _pf1_sum(x):
            s = pd.Series(x)
            return int(np.nansum(s.fillna(0).astype(int).to_numpy()))
        def _pf_na_sum(x):
            s = pd.Series(x)
            return int(s.isna().sum())

        g = raw.groupby(required, dropna=False)
        out = g.agg(
            N_month=("anno_mese", "size"),
            sum_abs_month=("_importo_num", lambda x: float(np.nansum(np.abs(x)))),
            pf1_count=("_pf01", _pf1_sum),
            pf_na_count=("_pf01", _pf_na_sum),
        ).reset_index()
        out["pf0_count"] = out["N_month"] - out["pf1_count"] - out["pf_na_count"]
        out["pf1_share"] = np.where(out["N_month"] > 0, out["pf1_count"] / out["N_month"], np.nan)
        return out

    def _mad(x: pd.Series) -> float:
        arr = np.asarray(x, dtype=float)
        if arr.size == 0: return 0.0
        med = np.median(arr)
        return float(np.median(np.abs(arr - med)))

    def _build_category_baselines_month(raw_month: pd.DataFrame) -> pd.DataFrame:
        # baseline sui mesi ATTIVI
        active = raw_month[raw_month["N_month"] > 0].copy()
        base = active.groupby(X).agg(
            med_N_month_base=("N_month", "median"),
            med_sum_abs_base=("sum_abs_month", "median"),
            mad_sum_abs_base=("sum_abs_month", _mad),
        ).reset_index()

        # cadenza: mesi attivi/anno
        months_per_year = raw_month.assign(active=(raw_month["N_month"] > 0).astype(int)) \
                                   .groupby([X, COL_ANNO])["active"].sum() \
                                   .reset_index(name="active_months")
        cadence = months_per_year.groupby(X)["active_months"].mean().reset_index(name="mean_active_months_per_year")

        return base.merge(cadence, on=X, how="left")

    def _month_of_year(ym: str) -> int:
        try:
            return int(ym.split("-")[1])
        except:
            return pd.NA

    def _compute_p_active_moy(monthly_all: pd.DataFrame) -> pd.DataFrame:
        """p_active_moy: per (categoria, mese-dell'anno) = freq storica di mesi attivi in quel mese."""
        tmp = monthly_all.copy()
        tmp["moy"] = tmp[COL_YM].apply(_month_of_year)
        tmp["active"] = (tmp["N_month"] > 0).astype(int)
        # anni osservati per categoria
        years_per_cat = tmp.groupby(X)[COL_ANNO].nunique().rename("n_years").reset_index()
        # volte attivo per mese dell'anno
        act = tmp.groupby([X, "moy"])["active"].sum().rename("n_active").reset_index()
        out = act.merge(years_per_cat, on=X, how="left")
        out["p_active_moy"] = np.where(out["n_years"] > 0, out["n_active"] / out["n_years"], np.nan)
        return out  # colonne: [X, moy, p_active_moy]

    def _cadence_type(row) -> str:
        mean_months = float(row.get("mean_active_months_per_year", np.nan))
        medN = float(row.get("med_N_month_base", np.nan))
        mad_amt = float(row.get("mad_sum_abs_base", np.nan))
        med_amt = float(row.get("med_sum_abs_base", np.nan))
        stable_amt = (mad_amt <= REL_BAND * med_amt) if med_amt > 0 else False
        if mean_months >= 10 and (0.75 <= medN <= 1.25) and stable_amt:
            return "fixed"
        if 3 <= mean_months < 10:
            return "seasonal"
        return "sporadic"

    def _build_full_grid_for_to_drill(to_drill_pairs: pd.DataFrame) -> pd.DataFrame:
        """Griglia completa 12 mesi per ogni (categoria, anno) sospetto."""
        rows = []
        for cat, yr in to_drill_pairs[[X, COL_ANNO]].astype(str).drop_duplicates().itertuples(index=False, name=None):
            for m in range(1, 13):
                ym = f"{yr}-{m:02d}"
                rows.append((cat, yr, ym))
        return pd.DataFrame(rows, columns=[X, COL_ANNO, COL_YM])

    # ----------------------- Caricamento RAW e preproc -----------------------
    raw = pd.read_csv(INPUT_CSV_RAW, sep=SEP, dtype=str, low_memory=False)
    # normalizza tipi
    for c in [X, COL_ANNO]:
        if c in raw.columns:
            raw[c] = raw[c].astype(str)

    # Considero solo le categorie sospette (riduce il perimetro)
    cats_set = set(to_drill[X].astype(str))
    raw_subset = raw[raw[X].astype(str).isin(cats_set)].copy()

    # Aggregazione mensile dal RAW
    monthly_raw = _agg_monthly_raw(raw_subset)

    # Baseline storiche per categoria (mesi attivi)
    base_month = _build_category_baselines_month(monthly_raw)

    # Probabilità storica di attività per mese dell'anno
    p_active = _compute_p_active_moy(monthly_raw)

    # Griglia completa mesi per le coppie (cat, anno) sospette
    grid = _build_full_grid_for_to_drill(to_drill)

    # Unisco l'aggregato mensile alla griglia: i mesi "mancanti" diventano N=0
    monthly_full = grid.merge(monthly_raw, on=[X, COL_ANNO, COL_YM], how="left")
    for col, fill in [("N_month", 0), ("sum_abs_month", 0.0), ("pf1_count", 0), ("pf0_count", 0), ("pf_na_count", 0), ("pf1_share", np.nan)]:
        monthly_full[col] = monthly_full[col].fillna(fill)

    # Join con baseline e p_active_moy
    monthly_enriched = monthly_full.merge(base_month, on=X, how="left")
    monthly_enriched["moy"] = monthly_enriched[COL_YM].apply(_month_of_year)
    monthly_enriched = monthly_enriched.merge(p_active[[X, "moy", "p_active_moy"]], on=[X, "moy"], how="left")

    # Calcolo banda importi robusta per categoria (mediana ± tau)
    monthly_enriched["tau_amt"] = np.maximum(
        MAD_MULT * monthly_enriched["mad_sum_abs_base"].fillna(0.0),
        REL_BAND * monthly_enriched["med_sum_abs_base"].fillna(0.0),
    )
    monthly_enriched["amount_band_low"]  = (monthly_enriched["med_sum_abs_base"] - monthly_enriched["tau_amt"]).clip(lower=0.0)
    monthly_enriched["amount_band_high"] = monthly_enriched["med_sum_abs_base"] + monthly_enriched["tau_amt"]

    # Tipo di cadenza per categoria
    monthly_enriched["cadence_type"] = monthly_enriched.apply(_cadence_type, axis=1)

    # Numero mesi attivi nell'anno (per categoria, anno)
    act_in_year = monthly_enriched.assign(active=(monthly_enriched["N_month"] > 0).astype(int)) \
                                  .groupby([X, COL_ANNO])["active"].sum().rename("active_months_in_year").reset_index()
    monthly_enriched = monthly_enriched.merge(act_in_year, on=[X, COL_ANNO], how="left")

    # Join con Livello 1 (delta entropici, se esistono su quel mese)
    l1_short = l1_df[[X, COL_ANNO, COL_YM, "delta_Hn_month_vs_base", "delta_Hn_month_vs_year", "delta_Hn_year"]].copy()
    monthly_enriched = monthly_enriched.merge(l1_short, on=[X, COL_ANNO, COL_YM], how="left")

    # ----------------------- Regole P0–P4 e classificazione -----------------------
    labels, severities, reasons = [], [], []

    for r in monthly_enriched.itertuples(index=False):
        label = ""
        sev = 0
        rs = []

        cat = getattr(r, X)
        yr  = getattr(r, COL_ANNO)
        ym  = getattr(r, COL_YM)

        N_m     = int(r.N_month or 0)
        sum_abs = float(r.sum_abs_month or 0.0)
        medN    = float(r.med_N_month_base or 0.0)
        medAmt  = float(r.med_sum_abs_base or 0.0)
        tau     = float(r.tau_amt or 0.0)
        cadence = float(r.mean_active_months_per_year or 0.0)
        act_in_yr = int(r.active_months_in_year or 0)
        band_low  = float(r.amount_band_low or 0.0)
        band_high = float(r.amount_band_high or 0.0)
        p_moy     = float(r.p_active_moy) if pd.notna(r.p_active_moy) else np.nan
        cad_type  = str(r.cadence_type)

        dHn_mb = float(r.delta_Hn_month_vs_base) if pd.notna(r.delta_Hn_month_vs_base) else np.nan
        dHn_my = float(r.delta_Hn_month_vs_year) if pd.notna(r.delta_Hn_month_vs_year) else np.nan

        # ----- P0: Declassamenti (NON anomalie) -----
        if cad_type == "fixed" and N_m == 1 and (sum_abs >= band_low and sum_abs <= band_high):
            label, sev = "expected_fixed", 0
            rs.append(f"fixed_one_payment_in_band [{band_low:.2f},{band_high:.2f}]")
        elif cad_type == "seasonal" and N_m > 0 and pd.notna(p_moy) and p_moy >= P_ACTIVE_HIGH:
            label, sev = "expected_seasonal", 0
            rs.append(f"seasonal_active_prob={p_moy:.2f}>= {P_ACTIVE_HIGH}")

        # Se non già classificato come atteso, valuto anomalie
        if not label:
            # ----- P1: Cadenza -----
            if cad_type == "fixed" and cadence >= MIN_N_MISSING_BASE and N_m == 0 and act_in_yr < max(10, cadence - 2):
                label, sev = "cadence_gap", 3
                rs.append(f"missing_month fixed: active_year={act_in_yr}<<cadence≈{cadence:.1f}")

            elif cad_type == "fixed" and N_m >= 2:
                label, sev = "unexpected_duplicate", 2
                rs.append(f"duplicate_in_fixed N={N_m}")

            elif cad_type == "seasonal" and N_m > 0 and pd.notna(p_moy) and p_moy <= P_ACTIVE_LOW:
                label, sev = "off-season_appearance", 2
                rs.append(f"offseason_active_prob={p_moy:.2f}<= {P_ACTIVE_LOW}")

            # ----- P2: Volumi / Importi -----
            if medN > 0 and N_m >= max(2, THRESH_N_BURST_RATIO * medN):
                # mantieni priorità se già cadenza; altrimenti assegna
                if not label or sev < 2:
                    label, sev = "burst_count", 2
                rs.append(f"N_month={N_m}>= {THRESH_N_BURST_RATIO}x medN={medN:.1f}")

            if medAmt > 0 and sum_abs >= max(band_high, THRESH_AMT_SPIKE_RATIO * medAmt):
                if not label or sev < 3:
                    label, sev = "amount_spike", 3
                rs.append(f"sum_abs={sum_abs:.2f}>=max(band_high={band_high:.2f}, {THRESH_AMT_SPIKE_RATIO}x{medAmt:.2f})")

            if medAmt > 0 and N_m > 0 and sum_abs <= min(band_low, medAmt / THRESH_AMT_SPIKE_RATIO):
                if not label or sev < 2:
                    label, sev = "amount_drop", 2
                rs.append(f"sum_abs={sum_abs:.2f}<=min(band_low={band_low:.2f}, {medAmt:.2f}/{THRESH_AMT_SPIKE_RATIO})")

            # ----- P3: Novità / Riattivazioni (soft, senza run-length globale) -----
            # Stima "first_ever" e "reactivation_spike" a livello anno con active_months_in_year molto basso
            # (versione semplice e robusta senza ricostruire tutta la timeline storica qui)
            if act_in_yr == 1 and N_m > 0:
                # se unico mese attivo dell'anno
                if not label or sev < 2:
                    label, sev = "first_ever_or_rare_year", 2
                rs.append("solo mese attivo nell'anno")
                if medAmt > 0 and sum_abs >= max(band_high, THRESH_AMT_SPIKE_RATIO * medAmt):
                    sev = 3
                    rs.append("spike_on_first_ever_or_rare_year")

        # ----- P4: Bonus entropico (mai da solo) -----
        bonus = 0
        if pd.notna(dHn_mb) and abs(dHn_mb) >= ENTROPY_BONUS:
            bonus += 1
            rs.append(f"entropy_shift_vs_base={dHn_mb:+.3f}")
        if pd.notna(dHn_my) and abs(dHn_my) >= ENTROPY_BONUS:
            bonus += 1
            rs.append(f"entropy_shift_vs_year={dHn_my:+.3f}")

        sev = min(3, sev + (1 if bonus and sev > 0 else 0))  # aumenta di 1 se già anomalia

        labels.append(label)
        severities.append(sev)
        reasons.append("|".join(rs))

    out_cols = [
        X, COL_ANNO, COL_YM,
        "N_month", "sum_abs_month",
        "pf1_count", "pf0_count", "pf_na_count", "pf1_share",
        "med_N_month_base", "med_sum_abs_base", "mad_sum_abs_base", "mean_active_months_per_year",
        "cadence_type", "amount_band_low", "amount_band_high", "p_active_moy",
        "active_months_in_year",
        "delta_Hn_month_vs_base", "delta_Hn_month_vs_year", "delta_Hn_year",
        "label_liv2", "severity", "reasons_liv2"
    ]

    liv2_df = monthly_enriched.copy()
    liv2_df["label_liv2"] = labels
    liv2_df["severity"] = severities
    liv2_df["reasons_liv2"] = reasons
    liv2_df = liv2_df[out_cols].sort_values([X, COL_ANNO, COL_YM]).reset_index(drop=True)

    # Salvataggio
    os.makedirs(os.path.dirname(OUT_LIV_2) or ".", exist_ok=True)
    liv2_df.to_csv(OUT_LIV_2, sep=SEP, index=False)
    print(f"[Liv2] Salvato classificazione anomalie: {OUT_LIV_2} (righe: {len(liv2_df)})")

    return liv2_df

# ============== MAIN ==============

def main():
    # Caricamento dati principali (classe/importi categorizzati)
    df = pd.read_csv(INPUT_CSV, sep=SEP, dtype=str, low_memory=False)
    for col in [Y, X, COL_ANNO, COL_YM]:
        if col not in df.columns:
            raise ValueError(f"Colonna mancante nel dataset: '{col}'")

    print("\n=== Livello 0: baseline e serie annuale con vocabolario fisso, NA ignorati ===")
    print(f"Input: {INPUT_CSV} | Righe: {len(df)} | Soglia |ΔHn|: {THRESH}\n")

    base_df, merged_year = livello0_compute(df)
    to_drill = livello0_save_outputs(base_df, merged_year)

    l1_df = livello1_drilldown_mensile(df, base_df, to_drill, merged_year)

    # Livello 2: classificazione finale anomalie
    _ = livello2_regole_realistiche(to_drill, l1_df)

    print("\n[OK] Livelli 0/1/2 completati.\n")



if __name__ == "__main__":
    main()
