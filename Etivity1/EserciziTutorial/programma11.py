import fnmatch
import os
import shutil  # Per spostare i file

# Cartella di destinazione
destinazione = "C:\\Users\\Utente\\Immagini_Trovate"
os.makedirs(destinazione, exist_ok=True)  # Crea la cartella se non esiste

# Tipi di immagini da cercare
images = ['*.jpg', '*.jpeg', '*.png', '*.tif', '*.tiff']
matches = []

# Scansiona il disco C:\
for root, dirnames, filenames in os.walk("C:\\Users\\Utente\\Pictures"):  
    for extensions in images:
        for filename in fnmatch.filter(filenames, extensions):
            file_path = os.path.join(root, filename)
            matches.append(file_path)  # Salva il percorso dell'immagine trovata
            
            # Sposta il file nella cartella di destinazione
            shutil.move(file_path, os.path.join(destinazione, filename))

print(f"Operazione completata! {len(matches)} immagini trovate e spostate.")
