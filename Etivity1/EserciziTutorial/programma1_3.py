nextEx="---------------------------------------------------------------------------"
print("Esercitazione Python - Programma 1")
a=15
b=3
c=a*b
s="Il prodotto di {0} x {1} = {2}".format(a,b,c)
print(s)

print(nextEx)

print("Esercitazione Python - Programma 2")
testo_1=input("Inserisci il tuo nome: ")
testo_2=input("Inserisci il tuo cognome: ")
testo_3=input("Inserisci città natale: ")

testo_elaborato=("L'utente {0} {1} è originario di {2}").format(testo_1,testo_2,testo_3)
print(testo_elaborato)

print(nextEx)

print("Esercitazione Python - Programma 3")
num_1=int(input("Inserisci un numero: "))
num_2=int(input("Inserisci un altro numero: "))

if(num_1>num_2):
    numeroMaggiore=("Tra {0} e {1}, il numero più grande è: {0}").format(num_1,num_2)
    print(numeroMaggiore)
    c=num_1-num_2
    differenza=("La differenza tra {0} e {1} = {2}").format(num_1,num_2,c)
    print(differenza)
elif(num_2>num_1):
    numeroMaggiore=("Tra {0} e {1}, il numero più grande è: {0}").format(num_2,num_1)
    print(numeroMaggiore)
    c=num_2-num_1
    differenza=("La differenza tra {0} e {1} = {2}").format(num_2,num_1,c)
    print(differenza)
else:
    c=num_1-num_2
    uguaglianza=("{0} e {1} sono uguali, infatti la loro differenza è: {2}").format(num_1,num_2,c)
    print(uguaglianza)
    
print(nextEx)