print("--------------------------------------------------------")
print("Nome: Roberto - Cognome: Barbato - Matricola: IN32000164")
print("--------------------------------------------------------")
print("Python - E-Tivity 3")
print("--------------------------------------------------------")

import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix

# Caricamento del dataset numerico
dataNumeric = pd.read_csv('./data/german.data-numeric', header=None, sep='\s+')

"""
print("--------------------------------------------------------")
print(dataNumeric.head())  # Controlla le prime righe del dataframe
print(dataNumeric.shape)  # Controlla il numero di colonne
print("--------------------------------------------------------")
"""

# dal file word German.doc ho deciso di utilizzare le seguenti variabili: status of checking account, duration in months, credit history, credit amount, present employment since, age in year e job per discriminare il soggetto

# Definizione intestazione colonne --> per variabili scelte --> rinomina
colonne_descrittive = {
    0:  "Stato conto corrente",
    1:  "Durata (mesi)",
    2:  "Storico credito",
    4:  "Importo richiesto",
    6:  "Anni impiego attuale",
    9: "Età del Contraente",
    16: "Tipo di lavoro",
    24: "Target"
}

dataNumeric = dataNumeric.rename(columns=colonne_descrittive)
df = dataNumeric[list(colonne_descrittive.values())]

"""
print(df["Età del Contraente"].describe())
print(df["Importo richiesto"].describe())
"""

# Mappatura delle variabili

# Status of checking account --> questa variabile verifica l'esistenza o meno di un conto corrente presso il nostro circuito bancario ipotetico, verificandone la giacenza e/o l'accredito dello stipendio
checking_account_map = {
    1: "Conto Corrente Inattivo",
    2: "Giacenza media: 0 <= ... < 2.000 € senza Accredito dello Stipendio",
    3: "Giacenza media: >= 2.000 € con Accredito dello Stipendio Attivo",
    4: "Nessun c/c associato"
}

# Credit history --> situazione storica del contraente
credit_history_map = {
    0: "Nessun Debito Vivo - Situazione debitoria pulita",
    1: "Debiti Vivi contratti con il nostro Istituto di Credito - Pagamenti Regolari",
    2: "Debiti Vivi contratti con altro Istituto di Credito - Pagamenti Regolari",
    3: "Debiti Vivi - Pagamenti Irregolari",
    4: "Debiti Vivi - Conto Corrente Critico - Debiti Vivi accumulati"
}

# Present employment since --> situazione lavorativa del contraente
employment_map = {
    0: "Disoccupato",
    1: "< 1 anno",
    2: "1–4 anni",
    3: "4–7 anni",
    4: ">= 7 anni"
}

# Job --> impiego del contraente
job_map = {
    0: "Disoccupato",
    1: "Lavoratore a Tempo Determinato - Autonomo",
    2: "Lavoratore a Tempo Indeterminato - Pubblico Impiego",
    3: "Lavoratore altamente qualificato - Manager"
}

print(df)

# Separazione tra feature(quello che so) (X) e target (quello che voglio sapere) (y)
X = df.drop("Target", axis=1)
y = df["Target"]

# normalizzazione i dati per ogni colonna delle mie feature "X" --> porto i dati sulla stessa scala per prepararli all'addestramento
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Suddivisione del dataset (80% per addestrare il modello 20% per testarlo)
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

print("--------------------------------------------------------")
print("Valutazione del modello: Regressione Logistica (con class_weight)")
print("--------------------------------------------------------")

logreg = LogisticRegression(class_weight='balanced', max_iter=1000, random_state=42)
logreg.fit(X_train, y_train)

y_pred_log = logreg.predict(X_test)

# Valutazione
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred_log))
print("--------------------------------------------------------")
print("Classification Report:")
print(classification_report(y_test, y_pred_log, target_names=["Buon creditore", "Cattivo creditore"]))