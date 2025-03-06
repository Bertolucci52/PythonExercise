nextEx="---------------------------------------------------------------------------"
print("Esercitazione Python - Programma 4")
sParola=input("Inserisci una parola: ")
print("Hai inserito,",sParola)

lunghezza=len(sParola)                                                              #funzione len(lunghezza della stringa)
print("La parola è composta da ",lunghezza," caratteri")
if(lunghezza>=4):
    print("La quarta lettera è: ",sParola[3])
else:
    print(sParola,"ha meno di 4 caratteri")
    
# inizializzo parametri
    
iIndice=0

vocaleA=0
vocaleE=0
vocaleI=0
vocaleO=0
vocaleU=0

# per incrementare ho utilizzato la scrittura += 1 che è equivalente a variabile = variabile +1

while iIndice<lunghezza:

    if(sParola[iIndice]=='a'):
        vocaleA+=1
    elif(sParola[iIndice]=='e'):        
        vocaleE+=1
    elif(sParola[iIndice]=='i'):
        vocaleI+=1
    elif(sParola[iIndice]=='o'):
        vocaleO+=1
    elif(sParola[iIndice]=='u'):
        vocaleU+=1
                
    iIndice+=1

riepilogo=("A: {0} - E: {1} - I:{2} - O:{3} - U:{4}").format(vocaleA,vocaleE,vocaleI,vocaleO,vocaleU)
print("Nella parola",sParola,"sono state trovate le seguenti vocali",riepilogo)
