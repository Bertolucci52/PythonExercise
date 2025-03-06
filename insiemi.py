print("Python - Creazione e gestione degli insiemi")
a = {'Cane','Gatto','Topo'} #l'ho definita come variabile insieme {}
print("Insieme A: ",a)
b = set()
b.add('Leone')
b.add('Gatto')
b.add('Tigre')
print("Insieme B: ",b)
print("__________EFFETTUO OPERAZIONI TRA INSIEMI__________")
print("Operazione di Unione: ", a | b) #unione univoca degli elementi(esclude le ridondanze)
print("Operazione di Intersezione: ", a & b) #riporta solo l'elemento in comune tra i due insiemi
print("Operazione di Differenza: ", a - b)
print("Operazione di Differenza Simmetrica: ", a ^ b)
