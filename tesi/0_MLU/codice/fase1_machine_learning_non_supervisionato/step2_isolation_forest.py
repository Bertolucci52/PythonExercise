import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

try:
    # Carica il file delle feature
    df = pd.read_csv("features_ml_mensili.csv", sep=",")
      

    # Estrai le feature numeriche
    features = df[["Numero Movimenti", "Importo Medio", "Importo Totale", "Varianza", "Entropia"]].copy()

    # Normalizzazione
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(features)

    # Isolation Forest
    model = IsolationForest(n_estimators=100, contamination="auto", random_state=42)
    df["Anomaly Score"] = model.fit_predict(X_scaled)
    df["Anomalia"] = df["Anomaly Score"].apply(lambda x: "Sì" if x == -1 else "No")

    # Salvataggio
    df.to_csv("risultati_isolation_forest.csv", index=False)
    print("✅ Analisi completata. File salvato come 'risultati_isolation_forest.csv'.")
    print(df.head())

except Exception as e:
    print("❌ Errore durante l'esecuzione:", str(e))

input("Premi INVIO per chiudere...")