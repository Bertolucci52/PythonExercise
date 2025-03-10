# Programma di ricerca parametro su più file (e nei singoli file) + copia degli stessi in una dir prestabilita
print("--------------------------------------------------------")
print("Nome: Roberto - Cognome: Barbato - Matricola: IN32000164")
print("--------------------------------------------------------")
print("Python - E-Tivity 1")
print("--------------------------------------------------------")

import PyPDF2                          # maneggiare i pdf
import docx                            # maneggiare i word
import pandas as pd                    # maneggiare excel e csv
import os
import re
import shutil                          # per spostare i file
import fnmatch                          # per confrontare i nomi dei file con il pattern

pattern=(input("Immetti la parola da cercare (PARAM1): "))
pattern = pattern.strip()

if len(pattern)<1:
    print("Errore - Inserire almeno un carattere per la ricerca")
    exit()

print("Parola: ", pattern)

dirStart=input("Immetti la directory di partenza della ricerca (PARAM2): ")
print("Start: ",dirStart)

base_path = os.path.join(os.path.expanduser("~"), "Desktop")                                # Percorso al Desktop ---> expanduser("~") mi ricavo la cartella principale dell'utente a cui aggiungo Desktop predefinito
cartella_utente = input("Immetti il nome della cartella di destinazione (PARAM3): ")
dirEnd = os.path.join(base_path, cartella_utente)                                           # Crea il percorso completo
os.makedirs(dirEnd, exist_ok=True)                                                          # Crea la cartella se non esiste
print(f"I file verranno salvati in: {dirEnd}")


fileType=['*.pdf','*.docx','*.xlsx','*.txt']



file_trovati = []                                                                           # Lista per salvare i percorsi trovati
text_trovate = []

for root, dirs, files in os.walk(dirStart):
    for ext in fileType:                                                                    # In precedenza ho passato al filtro l'intero Array fileType generando errrore                 
        for filename in fnmatch.filter(files, ext):                                         # esegue la ricerca per ogni parametro del ciclo for derivante da ext    
            file_path = os.path.join(root, filename)                                        # genero la path del file
            if pattern.lower() in filename.lower():                                         # senza .lower() ricercava una corrispondenza case-sansitive                                                                                            
                file_trovati.append(file_path)                                              # Aggiungi alla lista per successiva stampa sul terminale
                shutil.copy(file_path,dirEnd)                                               # copio il file nella dirEnd scelta
                
            if ext.endswith(".pdf"):
                print("Corrispondenze nel file PDF", file_path,":")
                object = PyPDF2.PdfReader(file_path)                     # accedo al PDF
                numPages = len(object.pages)                             # conto le pagine del pdf
                trovato_match=False
                for i in range(0, numPages):                                # analizzo per i =(0,numPages) ---> da 0 a n.pagine contante in precedenza
                    pageObj = object.pages[i]                               # accedo alla pagina i-esima
                    text = pageObj.extract_text()                           # estraggo (leggo) il testo della pagina   
                    for match in re.finditer(pattern, text):                # cerco il pattern nel testo della pagina i-esima che sto analizzando (il ciclo for si attiva solo in caso di corrispondenze)
                        print(f'Page no: {i} | Match: {match}')             # se lo trovo stampo la pagina i-esima e l'oggetto match
                        trovato_match=True
                
                if trovato_match:                    
                    text_trovate.append(file_path)
                    shutil.copy(file_path,dirEnd)
                    
            elif ext.endswith(".docx"):
                 print("Corrispondenze nel file Word ", file_path,":")
                 document = docx.Document(file_path)
                 text=""
                 trovato_match=False
                 for para in document.paragraphs:
                     text += para.text + "\n"
                 for match in re.finditer(pattern,text):
                    print(f"Match: {match}") 
                    trovato_match = True
                            
                 if trovato_match:
                    text_trovate.append(file_path)
                    shutil.copy(file_path,dirEnd)
                 
            elif ext.endswith(".xlsx"):
                print("Corrispondenze nel file Excel ", file_path,":")
                df = pd.read_excel(file_path)
                text = df.to_string()
                trovato_match=False
                for match in re.finditer(pattern,text):
                    print(f"Match: {match}") 
                    trovato_match = True
                            
                if trovato_match:
                    text_trovate.append(file_path)
                    shutil.copy(file_path,dirEnd)
                                
            elif ext.endswith(".txt"):
                print("Corrispondenze nel file .txt ", file_path,":")
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    text = f.read()
                    trovato_match=False
                    for match in re.finditer(pattern,text):
                        print(f"Match: {match}") 
                        trovato_match = True
                            
                if trovato_match:
                    text_trovate.append(file_path)
                    shutil.copy(file_path,dirEnd)

if text_trovate:
    print("\nDocumenti che hanno corrispondenza nella parola cercata e che sono stati copiati nella cartella di destinazione:")
    for parole in text_trovate:
        print(parole)
else:
    print("Nessuna corrispondenza trovata.")

if file_trovati:
    print("\nFile trovati con corrispondenze nel titolo e che sono stati copiati nella cartella di destinazione:")
    for file in file_trovati:
        print(file)
else:
    print("Nessuna corrispondenza trovata.")   

    
