print("--------------------------------------------------------")
print("Nome: Roberto - Cognome: Barbato - Matricola: IN32000164")
print("--------------------------------------------------------")
print("Python - E-Tivity 3")
print("--------------------------------------------------------")

import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
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

# Addestramento del modello KNN sui dati X e Y ----> TEST 1.1 (segue riga 181) --> ho ridotto a 3 i vicini per evitare la "normalizzazione" dei cattivi creditori
knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X_train, y_train)

y_pred = knn.predict(X_test)

# Valutazione
print("--------------------------------------------------------")
print("Valutazione del modello KNN (k=3)")
print("--------------------------------------------------------")
print("Confusion Matrix:")                                                                          # quanti sono stati etichettati "buoni/cattivi" correttamente --> 120 buoni veri e 21 falsi negativi + 31 falsi positivi e 28 veri cattivi
print(confusion_matrix(y_test, y_pred))
print("--------------------------------------------------------")
print("Classification Report:")
print(classification_report(y_test, y_pred, target_names=["Buon creditore", "Cattivo creditore"]))  #rapporto buoni/cattivi creditori su 100 unità di veri buoni/cattivi creditori --> accuracy (accuratezza del test) 74% + performante sui buoni creditori che sui cattivi

# Test 5 - german.data-numeric riporta un range di importi richiesti che non avevo discriminato in precedenza

def codifica_importo(importo):
    if importo <= 5000:
        return 1
    elif importo <= 10000:
        return 2
    elif importo <= 20000:
        return 3
    else:
        return 4


def predici_credito_utente():
    print("\n Inserisci i dati del cliente per valutare la richiesta di prestito [0-20.000]:\n")

    # Mappature testuali
    checking_account_map = {
        1: "Conto Corrente Inattivo",
        2: "Giacenza media: 0 <= ... < 2.000 € senza Accredito dello Stipendio",
        3: "Giacenza media: >= 2.000 € con Accredito dello Stipendio Attivo",
        4: "Nessun c/c associato"
    }

    credit_history_map = {
        0: "Nessun Debito Vivo - Situazione debitoria pulita",
        1: "Debiti Vivi contratti con il nostro Istituto di Credito - Pagamenti Regolari",
        2: "Debiti Vivi contratti con altro Istituto di Credito - Pagamenti Regolari",
        3: "Debiti Vivi - Pagamenti Irregolari",
        4: "Debiti Vivi - Conto Corrente Critico - Debiti Vivi accumulati"
    }

    employment_map = {
        0: "Disoccupato",
        1: "< 1 anno",
        2: "1–4 anni",
        3: "4–7 anni",
        4: ">= 7 anni"
    }

    job_map = {
        0: "Disoccupato",
        1: "Lavoratore a Tempo Determinato - Autonomo",
        2: "Lavoratore a Tempo Indeterminato - Pubblico Impiego",
        3: "Lavoratore altamente qualificato - Manager"
    }

    
    def chiedi_opzione(mappa, testo):
        while True:
            print(testo)
            for k, v in mappa.items():
                print(f"  {k}: {v}")
            try:
                scelta = int(input("   → Inserisci il numero corrispondente: "))
                if scelta in mappa:
                    return scelta
                else:
                    print("Valore non valido. Riprova.")
            except ValueError:
                print("Inserisci un numero valido.")

    conto = chiedi_opzione(checking_account_map, "Stato Conto Corrente:")
    storico = chiedi_opzione(credit_history_map, "Situazione Debitoria:")
    lavoro = chiedi_opzione(job_map, "Impiego:")
    if lavoro !=0:
        anni_impiego = chiedi_opzione(employment_map, "Da quanti anni:")
    else:
        anni_impiego = 0
        print("Hai indicato 'disoccupato', quindi gli anni di impiego sono stati impostati a 0.")    

    # INPUT 
    while True:
        try:
            importo = int(input("Importo richiesto (€): "))
            if importo <= 0:
                print("Inserisci un importo maggiore di zero.")
            elif importo > 20000:
                print("È possibile richiedere un finanziamento massimo di € 20.000.")
            else:  
                print(f"Importo accettato: € {importo}")              
                break                
        except ValueError:
            print("Inserisci un numero valido.")
    
    importo_codificato = codifica_importo(importo)
    print("Range di appartenza dell'importo richiesto:", importo_codificato)
    
    while True:
        try:
            durata = int(input("Durata del prestito (in mesi): "))
            if durata > 0:
                break
            else:
                print("Inserisci un numero maggiore di zero.")
        except ValueError:
            print("Inserisci un numero valido.")

    while True:
        try:
            eta = int(input("Età del cliente: "))
            if eta > 0:
                break
            else:
                print("Inserisci un'età valida.")
        except ValueError:
            print("Inserisci un numero valido.")
    
    # Test 6 --> Visto che il dataset non mi riporta un alto numero di cattivi creditori (così da istruire correttamente la macchina), ho forzato questa condizione "estrema" per far uscire un cattivo creditore
    
    if importo > 20000 or (conto == 1 and storico == 4 and lavoro == 0):   
        print("\n Profilo ad Alto Rischio.")
        print("Prestito sconsigliato. Il sistema ha bloccato la richiesta a prescindere dal modello.")
        return

    input_utente = [[conto, durata, storico, importo_codificato, anni_impiego, eta, lavoro]]
    input_df = pd.DataFrame(input_utente, columns=X.columns)
    input_scalato = scaler.transform(input_df)

    prediction = knn.predict(input_scalato)[0]
    proba = knn.predict_proba(input_scalato)[0]

# Test 1 - Ho riscontrato che il mio dataset è composto maggiormente da buoni creditori e questo va ad influenzare il KNN per vicinanza anche per un evidente cattivo creditore. --> provo abbassando il k a 3 vicini
# Test 2 - Riducendo il k la risultante è più "coerente" con la realtà anche se variabili estreme non sempre portano ad un valore veritiero
# Test 3 - Il primo attributo (stato del conto corrente) influenza enormemente il risultato finale --> in particolar modo il valore 4 (nessun conto corrente) assume quasi un valore "neutro" portando di default a fidarsi.
# Test 3.1 - Anche la durata va ad influire tanto sul risultato finale
# Test 4 - Avendo scelto poche variabili dal dataset originale pure se metto dati "logicamente" negativi il test si affida ai vicini simili (che possono essere buoni) --> segue riga 215

    print(f"\nProbabilità → Buon creditore: {proba[0]:.2f} | Cattivo creditore: {proba[1]:.2f}")
    print("\nRisultato della valutazione:")
    if prediction == 1:
        print("Il cliente è un buon creditore.")
    else:
        print("Il cliente è un cattivo creditore.")
    
    # Test 4.1 --> verifica dei vicini
    print("___________________________________")
    distanze, indici = knn.kneighbors(input_scalato)
    vicini = df.iloc[indici[0]]
    vicini = vicini.copy()
    vicini["Distanza"] = distanze[0]
    print("\nValori vicini nel dataset:")
    print(vicini)
    print("___________________________________")        

primo_ciclo = True
while True:
    if not primo_ciclo:
        comando = input("\n Vuoi valutare un nuovo cliente? (Digita 'exit' per uscire - altrimenti premi 'invio' per continuare): ").strip().lower()
        if comando == "exit":
            print("Uscita dal programma!")
            break
    predici_credito_utente() 
    primo_ciclo = False  
    
    
### Considerazioni Finali:
# Ho constatato che il dataset scelto è sbilanciato sui buoni creditori e questo a fatto venir meno, almeno in parte, il modello Knn che si basa sui vicini.
# Per ovviare al problema ho impostato dei parametri bloccanti per "istruire" a monte il programma --> il modello di regressione logistica sarebbe stato più idoneo.
# Eseguendo testRegr.py si può effettivamente constatare come sia l'accuratezza che il risultato dei cattivi creditori migliori