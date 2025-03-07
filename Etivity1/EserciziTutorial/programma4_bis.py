print("Esercitazione Python - Programma 4 Bis")
sParola=input("Inserisci una parola: ")
sCerca=input("Inserisci il carattere da cercare: ")

if(len(sCerca)>1):
    print("Errore - Cercare un carattere per volta")
    sCerca=""
    sCerca=input("Inserisci il carattere da cercare: ")
    
elif(len(sCerca)<0):
    print("Errore - Cercare almeno un carattere")
    sCerca=""
    sCerca=input("Inserisci il carattere da cercare: ")
    
iIndice=0
iCarattereTrovato=0

while iIndice<len(sParola):
    
    if(sParola[iIndice]==sCerca):
        iCarattereTrovato +=1
    
    iIndice +=1

if(iCarattereTrovato>0):
        
    riepilogo=("Nella parola che hai scelto: {0}, il carattere da cercare {1} è comparso {2} volte!").format(sParola,sCerca,iCarattereTrovato)
    print(riepilogo)
        
elif(iCarattereTrovato==0):
    riepilogo=("Nella parola che hai scelto: {0}, il carattere da cercare {1} non è presente!").format(sParola,sCerca)
    print(riepilogo)