import pandas as pd
import numpy as np
from math import log2

# ======== CONFIG ========
INPUT_CSV = "./dataset/registro_cassa_classi.csv"
SEP       = ";"
COLONNE   = [
    "risorsa",
    "tipologia_risorsa",
    "tipologia_movimento",
    "passaggio_fondi",
    "categoria_dettaglio",
    "classe_importo_id",
    "anno",
    "mese",
    "anno_mese",
]
SHOW_TOP_K = 10
# ========================

def shannon_entropy(series: pd.Series, base: float = 2.0) -> tuple[float, int]:    
    s = series.fillna("__NA__")
    counts = s.value_counts()
    N = counts.sum()
    if N == 0:
        return 0.0, 0
    p = counts / N
    H = -(p * np.log2(p)).sum()
    return float(H), len(counts)

def normalized_entropy(H: float, k: int) -> float:
    """Normalizza H in [0,1] rispetto all'entropia massima log2(k)."""
    if k <= 1:
        return 0.0
    Hmax = log2(k)
    return H / Hmax

def main():
    df = pd.read_csv(INPUT_CSV, sep=SEP, dtype=str, low_memory=False)

    print("\n================ ENTROPIE MARGINALI (Shannon, base 2) ================\n")
    print(f"File: {INPUT_CSV}")
    print(f"Righe totali: {len(df)}\n")
    
    riepilogo = []
    
    for col in COLONNE:
        if col not in df.columns:
            print(f"[SKIP] Colonna non trovata: {col}\n")
            continue
        H, k = shannon_entropy(df[col])
        Hn = normalized_entropy(H, k)
        print(f"- Colonna: {col}")
        print(f"  • Valori distinti (k): {k}")
        print(f"  • Entropia H: {H:.4f} bit")
        print(f"  • Entropia normalizzata: {Hn:.4f}")
        # top categorie
        vc = df[col].fillna("__NA__").value_counts()
        total = vc.sum()
        top = vc.head(SHOW_TOP_K)
        print(f"  • Top {min(SHOW_TOP_K, len(vc))} categorie:")
        for val, cnt in top.items():
            perc = 100.0 * cnt / total if total else 0
            print(f"     - {val}: {cnt} ({perc:.2f}%)")
        if len(vc) > SHOW_TOP_K:
            others = total - top.sum()
            print(f"     - (altre {len(vc)-SHOW_TOP_K}): {others} ({100.0*others/total:.2f}%)")
        print()
        
        riepilogo.append((col,H,Hn))

    print("======================================================================\n")
    print("Nota: entropia normalizzata vicina a 1 → distribuzione uniforme.")
    print("      entropia vicina a 0 → distribuzione concentrata.\n")
    
    # stampa riepilogo sintetico
    riepilogo_df = pd.DataFrame(riepilogo, columns=["colonna", "H", "Hn"])
    riepilogo_df = riepilogo_df.sort_values("Hn", ascending=False)

    print("=== RIEPILOGO ENTROPIE (ordinate per Hn) ===")
    for _, row in riepilogo_df.iterrows():
        print(f"{row['colonna']:25s} -> H = {row['H']:.4f} bit -> Hn = {row['Hn']:.4f}")

if __name__ == "__main__":
    main()
