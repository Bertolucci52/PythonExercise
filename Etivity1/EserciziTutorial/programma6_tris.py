# Creazione della lista con 10 elementi, inclusi duplicati
myList = ["Cane", "Gatto", "Leone", "Aquila", "Mucca", 
          "Toro", "Michele", "Cane", "Giovanni", "Cane"]

print("Elenco Iniziale:", myList)

# Creazione di un set per ottenere solo gli elementi distinti
listaDistinct = set()

# Aggiunta degli elementi alla variabile di tipo set (eliminerà automaticamente i duplicati)
for elemento in myList:
    listaDistinct.add(elemento)

print("Elenco Lista senza duplicati:", listaDistinct)
