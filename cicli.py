print("Python - Gestione dei Cicli for")
a={'cane','gatto','topo'}
print("Nell'insieme A sono presenti i seguenti animali: ")
for animale in a: #la variabile animale CONTIENE gli elementi definiti nell'insieme a
    print(animale)

esami={'IN110':27,'AM110':30,'AL110':24} #variabile DIZIONARIO (CHIAVE-VALORE) ha una struttura chiave-valore chiave:'IN110' e il valore è dato da ":" + valore
print("Insieme Esami: ", esami)
print("Esami superati:", end=" ") #end=" " serve per lasciare spazio 
for corso in esami.keys(): #esami.keys è la lista delle chiavi presenti nel dizionario esami
    print(corso, end=" ")

print()
print("Valutazione Esami: ")
for corso in esami.keys():
    print("Corso:", corso, "- Votazione: ", esami[corso], "/30") #[mi fa accedere al valore associato alla chiave del dizionario]