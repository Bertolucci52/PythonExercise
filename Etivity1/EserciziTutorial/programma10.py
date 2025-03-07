def mcm(x, y):                              # funzione per trovare minimo comune multiplo (x,y) sono i parametri che la funzione riceve come input dall'utente
    mx = x                                  # mx assume il valore di x
    my = y                                  # my assume il valore di y
    while mx != my:                         # finché mx e my non saranno uguali (il minimo comune multiplo appunto) eseguo un ciclo alternato
        if mx<my:                           # l'alternanza è definita dal rapporto tra mx e my, se mx è più piccolo:
            mx = mx+x                       # aggiungo al valore di mx una quantità di x (o viceversa) ---> finché non viene rispentata la condizione per ottenere mcm
        else:
            my = my+y
    return(mx)

def mcd(x, y):
    while y != 0:                           # il calcolo andrà avanti finché y è diverso da ZERO
        x, y = y, x % y                     # Sostituisco x con y e y con il resto % restituisce il resto tra due numeri (48 % 18 ---> restituirà 12 <--- 18x3=36  48-36= 12)
    return x                                # valore prima che sia zero        


print("Ciao a tutti - PROGRAMMA10")

iPos = 0                                                                            # inizializzo i tentativi (contatore) per eseguire l'operazione
while iPos < 3:
    sStringaRicevuta = input("Inserisci un valore per a: ")
    try:
        a = float(sStringaRicevuta)
        print("Hai inserito ",a)
        iPos = 100                                                                  # se il valore inserito è un numero, converte la stringa in numero, porta il contatore a 100 (valore scelto per proseguire)
    except:
        print("Attenzione, hai inserito un valore sbagliato ",sStringaRicevuta)     
        iPos = iPos + 1                                                             # in caso di errore (testo anziché numero) aumento il contatore di 1 fino ad un max di 3 (def. riga 14)

if(iPos!=100):                                                                      # ho 3 possibilità, iPos appena diventa 4 sarà diverso da 100 (pass) e chiude il programma
    exit(0)

b = int(input("Inserisci un valore per b: "))
m = mcm(a,b)                                                                        # richiamo la funzione definita all'inizio passandogli i parametri a,b che saranno interpretato come x,y
MCD = mcd(a,b)
print("mcm(", a, ",", b,") = ", m)
print("MCD(", a, ",", b,") = ", MCD)