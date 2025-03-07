print("Esercitazione Python - Programma 4 Tris")
a=int(input("Inserisci un numero: "))
b=int(input("Inserisci un secondo numero: "))
operatore=input("Definisci un operatore (+ - * /): ")

opAmmessi={'+','-','*','/'}

if operatore not in opAmmessi:
    print("Errore: operatore non valido.")
    exit()
    
if operatore == '+':
    c = a + b
elif operatore == '-':
    c = a - b
elif operatore == '*':
    c = a * b
elif operatore == '/':
    if b!= 0:
        c = a/b
    else:
        print("Non si può dividere per zero.")
        c = None
else:
    print("Operatore non valido")
    

risultato="{0} {1} {2} = {3}".format(a,operatore,b,c)

print(risultato)