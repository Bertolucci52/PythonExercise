import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("risultati_isolation_forest.csv", sep=",", encoding="utf-8-sig")

# Conteggio per Categoria
conteggio_categoria = df["Categoria"].value_counts().sort_values(ascending=False)

plt.figure(figsize=(10, 5))
conteggio_categoria.plot(kind="bar")
plt.title("Numero di anomalie rilevate per Categoria")
plt.ylabel("Conteggio")
plt.xlabel("Categoria")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Conteggio per Mese (opzionale)
df["Mese"] = pd.to_datetime(df["Mese"])
conteggio_mese = df["Mese"].dt.to_period("M").value_counts().sort_index()

plt.figure(figsize=(12, 4))
conteggio_mese.plot(kind="bar")
plt.title("Anomalie nel tempo (per Mese)")
plt.ylabel("Numero anomalie")
plt.xlabel("Mese")
plt.tight_layout()
plt.show()
