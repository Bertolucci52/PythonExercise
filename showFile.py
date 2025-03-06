import fnmatch                          # libreria che permette di confrontare i nomi dei file con un pattern
import os                               # libreria che contiene funzioni per lavorare con i file system

rootpath='./'                           # punto di inizio della ricerca
pattern='*.pdf'                         # definisce il criterio di ricerca: "*" -> tutti i file che terminano con ".pdf" 

#  os.walk(rootpath) --> scansiona la cartella definita in rootpath e restituisce i valori per ogni cartella trovata: root (cartella attuale), dirs(sottocartelle in root), files (lista dei file presenti in root)
# funzione fnmatch.filter(files, pattern) --> filtra solo i file che corrispondono al pattern definito (.pdf)
# funzione os.path.join(root, filename) --> crea il percorso completo del file combinando la cartella attuale (root) con il nome del file (filename)

for root, dirs, files in os.walk(rootpath):
    for filename in fnmatch.filter(files, pattern):
        print(os.path.join(root,filename))