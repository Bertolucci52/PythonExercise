print("--------------------------------------------------------")
print("Nome: Roberto - Cognome: Barbato - Matricola: IN32000164")
print("--------------------------------------------------------")
print("Python - E-Tivity 3")
print("--------------------------------------------------------")

import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# Carica il dataset
df = pd.read_csv('./data/german.data', header=None, delim_whitespace=True)

# Verifica la struttura del dataframe (quante colonne ci sono)
print(df.head())  # Controlla le prime righe del dataframe
print(df.shape)  # Controlla il numero di colonne


# Aggiungi i nomi delle colonne corrispondenti al dataset
df.columns = [
    'CheckingAccountStatus', 'Duration', 'CreditHistory', 'Purpose', 'CreditAmount', 
    'SavingsAccountBonds', 'Employment', 'PersonalStatus', 'OtherParties', 'ResidenceSince',
    'PropertyMagnitude', 'Age', 'OtherPaymentPlans', 'Housing', 'ExistingCreditsAtThisBank',
    'Job', 'NumDependents', 'OwnsPhone', 'ForeignWorker', 'Class', 'Target'  # Assicurati che questa lista corrisponda al numero di colonne nel dataset
]


# Verifica la nuova struttura
print(df.head())  # Controlla di nuovo le prime righe con i nuovi nomi di colonna


# Codifica le variabili categoriche
label_encoders = {}
for column in df.select_dtypes(include=['object']).columns:
    le = LabelEncoder()
    df[column] = le.fit_transform(df[column])
    label_encoders[column] = le

# Normalizzazione delle variabili numeriche
scaler = StandardScaler()
df[['Duration', 'CreditAmount', 'Age']] = scaler.fit_transform(df[['Duration', 'CreditAmount', 'Age']])

# Separare le variabili indipendenti (X) e la variabile dipendente (y)
X = df.drop('Class', axis=1)
y = df['Class']

# Suddividere il dataset in train e test (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Creare il modello RandomForest
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Valutare il modello
y_pred = model.predict(X_test)
print(f"Accuracy: {model.score(X_test, y_test):.2f}")

# Funzione di previsione per nuovi dati
def predict_credit_risk(model, scaler, label_encoders):
    # Chiedi i dati all'utente
    checking_account_status = input(f"Status del conto corrente ({', '.join(label_encoders['CheckingAccountStatus'].classes_)}): ")
    
    # Verifica che l'input dell'utente sia valido per 'CheckingAccountStatus'
    while checking_account_status not in label_encoders['CheckingAccountStatus'].classes_:
        print(f"Errore: lo status del conto deve essere uno dei seguenti: {', '.join(label_encoders['CheckingAccountStatus'].classes_)}")
        checking_account_status = input(f"Riprova. Inserisci uno status del conto valido ({', '.join(label_encoders['CheckingAccountStatus'].classes_)}): ")

    duration = float(input("Inserisci la durata del prestito (in mesi): "))
    credit_amount = float(input("Inserisci l'ammontare del credito: "))
    age = int(input("Inserisci l'età del richiedente: "))
    
    credit_history = input("Storia del credito (A34, A32, A30, ...): ")
    
    # Verifica che l'input dell'utente per 'CreditHistory' sia valido
    while credit_history not in label_encoders['CreditHistory'].classes_:
        print(f"Errore: la storia del credito deve essere uno dei seguenti: {', '.join(label_encoders['CreditHistory'].classes_)}")
        credit_history = input(f"Riprova. Inserisci una storia del credito valida ({', '.join(label_encoders['CreditHistory'].classes_)}): ")

    employment = input("Tipo di impiego (A61, A62, A63, ...): ")
    
    # Verifica che l'input dell'utente per 'Employment' sia valido
    while employment not in label_encoders['Employment'].classes_:
        print(f"Errore: il tipo di impiego deve essere uno dei seguenti: {', '.join(label_encoders['Employment'].classes_)}")
        employment = input(f"Riprova. Inserisci un tipo di impiego valido ({', '.join(label_encoders['Employment'].classes_)}): ")

    # Pre-elaborazione dei dati inseriti
    data = pd.DataFrame([[checking_account_status, duration, credit_amount, age, credit_history, employment]], 
                        columns=['CheckingAccountStatus', 'Duration', 'CreditAmount', 'Age', 'CreditHistory', 'Employment'])
    
    # Codifica delle variabili categoriche
    data['CheckingAccountStatus'] = label_encoders['CheckingAccountStatus'].transform(data['CheckingAccountStatus'])
    data['CreditHistory'] = label_encoders['CreditHistory'].transform(data['CreditHistory'])
    data['Employment'] = label_encoders['Employment'].transform([employment])[0]
    
    # Normalizzazione dei dati
    data[['Duration', 'CreditAmount', 'Age']] = scaler.transform(data[['Duration', 'CreditAmount', 'Age']])
    
    # Aggiungi le colonne mancanti con valori predefiniti (o nulli)
    for column in df.columns:
        if column not in data.columns:
            data[column] = 0  # Aggiungi un valore predefinito per le colonne mancanti
    
    # Previsione con il modello addestrato
    prediction = model.predict(data)
    
    # Mostrare il risultato
    if prediction == 1:
        print("Il prestito è a rischio.")
    else:
        print("Il prestito è sicuro.")

# Chiamare la funzione per fare una previsione
predict_credit_risk(model, scaler, label_encoders)


# Chiamare la funzione per fare una previsione
predict_credit_risk(model, scaler, label_encoders)