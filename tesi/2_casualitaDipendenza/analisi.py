import pandas as pd
from scipy.stats import entropy
import numpy as np

df = pd.read_csv("../1_entropiaShannon/registro_cassa.csv", sep=";", encoding="ISO-8859-1")
df["Importo"] = df["Importo"].str.replace(",", ".").astype(float).round(2)
df["Data Movimento"] = pd.to_datetime(df["Data Movimento"], format="%d/%m/%Y")

df_uscite = df[(df["Importo"] < 0) & (df["Passaggio Fondi"] == "No")]
# print(df_uscite[["Data Movimento", "Importo", "Passaggio Fondi"]].head())
df_uscite["Mese"] = df_uscite["Data Movimento"].dt.to_period("M")
riepilogo = df_uscite.groupby(["Mese", "CashFlow - Categoria"])["Importo"].sum().reset_index()