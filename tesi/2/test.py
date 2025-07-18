import pandas as pd
from scipy.stats import entropy
import numpy as np

df = pd.read_csv("../dataset/registro_cassa.csv", sep=";", encoding="ISO-8859-1")
df["Importo"] = df["Importo"].str.replace(",", ".").astype(float).round(2)
df["Data Movimento"] = pd.to_datetime(df["Data Movimento"], format="%d/%m/%Y")

df_uscite = df[(df["Importo"] < 0) & (df["Passaggio Fondi"] == "No")]
# print(df_uscite[["Data Movimento", "Importo", "Passaggio Fondi"]].head())
df_uscite["Mese"] = df_uscite["Data Movimento"].dt.to_period("M")
riepilogo = df_uscite.groupby(["Mese", "CashFlow - Categoria"])["Importo"].sum().reset_index()

# Analisi specifica per il dettaglio "Stipendi" della categoria Amministrazione

df_stipendi = df_uscite[
    (df_uscite["CashFlow - Categoria"] == "Amministrazione") &
    (df_uscite["CashFlow - Dettaglio"] == "Stipendi")
].copy()


riepilogo_stipendi = df_stipendi.groupby("Mese").agg(
    Numero_Movimenti=("Importo", "count"),
    Totale_Uscite=("Importo", "sum")
).reset_index()

tutti_i_mesi = pd.DataFrame({
    "Mese": pd.period_range(df["Data Movimento"].min(), df["Data Movimento"].max(), freq="M")
})


riepilogo_stipendi = tutti_i_mesi.merge(riepilogo_stipendi, on="Mese", how="left")
riepilogo_stipendi["Numero_Movimenti"] = riepilogo_stipendi["Numero_Movimenti"].fillna(0).astype(int)
riepilogo_stipendi["Totale_Uscite"] = riepilogo_stipendi["Totale_Uscite"].fillna(0.0).round(2)


# Regole di classificazione
def classifica_riga(row):
    if row["Numero_Movimenti"] == 0:
        return "Buco"
    elif row["Numero_Movimenti"] == 1 and round(row["Totale_Uscite"], 2) == -8200.00:
        return "Normale"
    elif row["Numero_Movimenti"] > 1:
        return "Anomalia: Multi-movimento"
    elif round(row["Totale_Uscite"], 2) != -8200.00:
        return "Anomalia: Importo anomalo"
    else:
        return "?"

riepilogo_stipendi["Classificazione"] = riepilogo_stipendi.apply(classifica_riga, axis=1)
print("Riepilogo stipendi per mese con classificazione:")
print(riepilogo_stipendi)

anomalie_stipendi = riepilogo_stipendi[riepilogo_stipendi["Classificazione"] != "Normale"]

print("Mesi con comportamento anomalo nei movimenti 'Stipendi':")
print(anomalie_stipendi)

print("\nTotale mesi analizzati:", len(riepilogo_stipendi))
print("Mesi normali:", (riepilogo_stipendi["Classificazione"] == "Normale").sum())
print("Mesi con anomalie:", len(anomalie_stipendi))

