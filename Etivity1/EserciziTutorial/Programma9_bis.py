def somma():
    a=int(input("Inserisci un numero: "))
    b=int(input("Inserisci un secondo numero: "))
    c=a+b
    s="{0}+{1}={2}".format(a,b,c)
    print("Operatore Somma: ", s)

def differenza():
    a=int(input("Inserisci un numero: "))
    b=int(input("Inserisci un secondo numero: "))
    c=a-b
    s="{0}-{1}={2}".format(a,b,c)
    print("Operatore Differenza: ", s)

def moltiplicazione():
    a=int(input("Inserisci un numero: "))
    b=int(input("Inserisci un secondo numero: "))
    c=a*b
    s="{0}x{1}={2}".format(a,b,c)
    print("Operatore Moltiplicatore: ", s)

def divisione():
    a=int(input("Inserisci un numero: "))
    b=int(input("Inserisci un secondo numero: "))
    if b==0:
        print("Il denominatore non può essere uguale a zero")
        exit()
    c=a/b
    s="{0}/{1}={2}".format(a,b,c)
    print("Operatore Divisione: ", s)

def media():
    numeri = list(map(int, input("Inserisci i numeri separati da spazio: ").split()))
    risultato = sum(numeri) / len(numeri)
    print("Operatore Media: ", risultato)

print("Python - Calcolatrice")

# Dizionario per gestire gli operatori e le funzioni corrispondenti
operatori = {
    '+': somma,
    '-': differenza,
    '*': moltiplicazione,
    '/': divisione,
    'media': media
}


# Loop per permettere più operazioni senza dover riavviare
while True:
    question = input("Scegli l'operazione da eseguire (+ - * / media) o 'exit' per uscire: ")

    if question == "exit":
        print("Fine Programma")
        break

    if question in operatori:
        operatori[question]()  # Chiama la funzione corrispondente
    else:
        print("Operatore non valido, riprova!")



