myList=[]

print("Elenco Iniziale: ", myList)

iIndice=0

while len(myList)<10:
    if iIndice== 0:
        myList.append("Cane")
        iIndice +=1
    elif iIndice==1:
        myList.append("Gatto")
        iIndice+=1
    elif iIndice==2:
        myList.append("Leone")
        iIndice+=1
    elif iIndice==3:
        myList.append("Aquila")
        iIndice+=1
    elif iIndice==4:
        myList.append("Mucca")
        iIndice+=1
    elif iIndice==5:
        myList.append("Toro")
        iIndice+=1
    elif iIndice==6:
        myList.append("Michele")
        iIndice+=1
    elif iIndice==7:
        myList.append("Cane")
        iIndice+=1
    elif iIndice==8:
        myList.append("Giovanni")
        iIndice+=1
    elif iIndice==9:
        myList.append("Cane")
        iIndice+=1

iIndice +=1

print("Elenco Aggiornato: ", myList)

listaDistinct = set(myList)

print("Elenco Lista senza duplicati: ", listaDistinct)

        