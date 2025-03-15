# Read file into a Pandas dataframe
from pandas import DataFrame, read_csv

print("Programma di calcolo e visualizzazione matrice di correlazione lineare")

#Leggiamo il file csv e stampiamo le prime 10 righe
"""
a = input("Inserisci path completo file CSV: ")
header_si_no = input("La prima riga è l'header(Si/No)?")
separator = input("Inserisci il separatore:")

#file remoto
#f = 'https://archive.ics.uci.edu/ml/machine-learning-databases/abalone/abalone.data'

#inizializzo la lista delle etichette che leggo dal CSV se ci sono oppure le inserisce l'utente
labels = [];
f = a;
if(header_si_no.lower()=='si'):
    df = read_csv(f, sep=separator)

if(header_si_no.lower()=='no') :
    df = read_csv(f, header=None, sep=separator)

df=df[0:10]
print(df)
"""


#Leggiamo il file csv e stampiamo le prime 10 righe e il vettore delle etichette
"""
a = input("Inserisci path completo file CSV: ")
header_si_no = input("La prima riga è l'header(Si/No)?")
separator = input("Inserisci il separatore:")

#inizializzo la lista delle etichette che leggo dal CSV se ci sono oppure le inserisce l'utente
labels = [];
f = a;
header_flag_ok = 0;
if(header_si_no.lower()=='si'):
    df = read_csv(f, sep=separator)
    labels = df.columns.tolist();
    header_flag_ok = 1;

if(header_si_no.lower()=='no') :
    df = read_csv(f, header=None, sep=separator)
    header_flag_ok = 1;
    iCounter = 0;
    num_cols = len(df.columns)
    while iCounter < num_cols:
        sStringToPrint = "Inserisci label " + str(iCounter + 1);
        labels.append(input(sStringToPrint))
        iCounter = iCounter + 1;

if(header_flag_ok!=1):
    print("header nel file non letto correttamente");
    sys.exit(0);
    
df=df[0:10]
print(df)
print(labels)
"""

#Creare e visualizzare un grafico in cui sull’asse delle X c’è la variabile 
#Sex e sull’asse delle Y c’è la variabile Rings.
"""
import matplotlib
import numpy as np
import matplotlib.pyplot as plt

#funzione che mostra l'ambiente grafico di mathplot
def crea_grafico_semplice(vX, vY):
    
    #crea una finestra per un grafico
    fig = plt.figure()
    
    #crea una griglia 1x1 e metti il piano cartesiano nella posizione 1 della griglia
    fig.add_subplot(111)
    
    plt.scatter(vX, vY)
    plt.show()

a = input("Inserisci path completo file CSV: ")
header_si_no = input("La prima riga è l'header(Si/No)?")
separator = input("Inserisci il separatore:")

#inizializzo la lista delle etichette che leggo dal CSV se ci sono oppure le inserisce l'utente
labels = [];
f = a;
header_flag_ok = 0;
if(header_si_no.lower()=='si'):
    df = read_csv(f, sep=separator)
    labels = df.columns.tolist();
    header_flag_ok = 1;

if(header_si_no.lower()=='no') :
    df = read_csv(f, header=None, sep=separator)
    header_flag_ok = 1;
    iCounter = 0;
    num_cols = len(df.columns)
    while iCounter < num_cols:
        sStringToPrint = "Inserisci label " + str(iCounter + 1);
        labels.append(input(sStringToPrint))
        iCounter = iCounter + 1;

if(header_flag_ok!=1):
    print("header nel file non letto correttamente");
    sys.exit(0);
    
df=df[0:10]
print(df)
print(labels)

numpy_array = np.array(df)
x = numpy_array[:,0]
y = numpy_array[:,8]
crea_grafico_semplice(x,y)
"""




#Creare 4 grafici sulla stessa finestra
"""
import matplotlib
import numpy as np
import matplotlib.pyplot as plt



#funzione che mostra l'ambiente grafico di mathplot
def crea_grafico_semplice(vX, vY, pos, fig):
    
    
    #crea una griglia 1x1 e metti il piano cartesiano nella posizione 1 della griglia
    fig.add_subplot(pos)
    
    plt.scatter(vX, vY)
    

a = input("Inserisci path completo file CSV: ")
header_si_no = input("La prima riga è l'header(Si/No)?")
separator = input("Inserisci il separatore:")

#inizializzo la lista delle etichette che leggo dal CSV se ci sono oppure le inserisce l'utente
labels = [];
f = a;
header_flag_ok = 0;
if(header_si_no.lower()=='si'):
    df = read_csv(f, sep=separator)
    labels = df.columns.tolist();
    header_flag_ok = 1;

if(header_si_no.lower()=='no') :
    df = read_csv(f, header=None, sep=separator)
    header_flag_ok = 1;
    iCounter = 0;
    num_cols = len(df.columns)
    while iCounter < num_cols:
        sStringToPrint = "Inserisci label " + str(iCounter + 1);
        labels.append(input(sStringToPrint))
        iCounter = iCounter + 1;

if(header_flag_ok!=1):
    print("header nel file non letto correttamente");
    sys.exit(0);
    
df=df[0:10]
print(df)
print(labels)

fig = plt.figure()
numpy_array = np.array(df)
x = numpy_array[:,0]
y = numpy_array[:,8]
crea_grafico_semplice(x,y,221,fig)

x = numpy_array[:,0]
y = numpy_array[:,1]
crea_grafico_semplice(x,y,222, fig)

x = numpy_array[:,0]
y = numpy_array[:,2]
crea_grafico_semplice(x,y,223, fig)

x = numpy_array[:,0]
y = numpy_array[:,3]
crea_grafico_semplice(x,y,224, fig)
plt.show()
"""














#Stampare a schermo la MATRICE DI CORRELAZIONE
"""
import matplotlib
import numpy as np
import matplotlib.pyplot as plt

#funzione che mostra l'ambiente grafico di mathplot
def crea_grafico_semplice(vX, vY):
    
    #crea una finestra per un grafico
    fig = plt.figure()
    
    #crea una griglia 1x1 e metti il piano cartesiano nella posizione 1 della griglia
    fig.add_subplot(111)
    
    plt.scatter(vX, vY)
    plt.show()

a = input("Inserisci path completo file CSV: ")
header_si_no = input("La prima riga è l'header(Si/No)?")
separator = input("Inserisci il separatore:")

#inizializzo la lista delle etichette che leggo dal CSV se ci sono oppure le inserisce l'utente
labels = [];
f = a;
header_flag_ok = 0;
if(header_si_no.lower()=='si'):
    df = read_csv(f, sep=separator)
    labels = df.columns.tolist();
    header_flag_ok = 1;

if(header_si_no.lower()=='no') :
    df = read_csv(f, header=None, sep=separator)
    header_flag_ok = 1;
    iCounter = 0;
    num_cols = len(df.columns)
    while iCounter < num_cols:
        sStringToPrint = "Inserisci label " + str(iCounter + 1);
        labels.append(input(sStringToPrint))
        iCounter = iCounter + 1;

if(header_flag_ok!=1):
    print("header nel file non letto correttamente");
    sys.exit(0);
    
df=df[0:10]
print(labels)
print(df)

print(df.corr())
"""









#Visualizzare la matrice di correlazione con una mappa termica

import matplotlib
import numpy as np
import matplotlib.pyplot as plt

#funzione che mostra l'ambiente grafico di mathplot
def crea_grafico_semplice(vX, vY):
    
    #crea una finestra per un grafico
    fig = plt.figure()
    
    #crea una griglia 1x1 e metti il piano cartesiano nella posizione 1 della griglia
    fig.add_subplot(111)
    
    plt.scatter(vX, vY)
    plt.show()
    

def correlation_matrix(df, labels):
    from matplotlib import pyplot as plt
    from matplotlib import cm as cm
    
    #crea una finestra per un grafico
    fig = plt.figure()
    
    #crea una griglia 1x1 e metti il piano cartesiano nella posizione 1 della griglia
    ax1 = fig.add_subplot(111)   
    
    #rappresentiamo la matrice di correlazione con una colorMap
    cmap = cm.get_cmap('jet', 30)   
    cax = ax1.imshow(df.corr(), cmap=cmap)
    
    #creiamo sul piano cartesiano una griglia
    ax1.grid(True)
    
    plt.title('Matrice di correlazione')   
    
    #aggiungiamo al piano cartesiano le labalels su entram gli assi
    ax1.set_xticklabels(labels,fontsize=6)
    ax1.set_yticklabels(labels,fontsize=6)
    
    # Add colorbar, make sure to specify tick locations to match desired ticklabels
    fig.colorbar(cax, ticks=[.75,.8,.85,.90,.95,1])
    
    plt.show()



a = input("Inserisci path completo file CSV: ")
header_si_no = input("La prima riga è l'header(Si/No)?")
separator = input("Inserisci il separatore:")

#inizializzo la lista delle etichette che leggo dal CSV se ci sono oppure le inserisce l'utente
labels = [];
f = a;
header_flag_ok = 0;
if(header_si_no.lower()=='si'):
    df = read_csv(f, sep=separator)
    labels = df.columns.tolist();
    header_flag_ok = 1;

if(header_si_no.lower()=='no') :
    df = read_csv(f, header=None, sep=separator)
    header_flag_ok = 1;
    iCounter = 0;
    num_cols = len(df.columns)
    while iCounter < num_cols:
        sStringToPrint = "Inserisci label " + str(iCounter + 1);
        labels.append(input(sStringToPrint))
        iCounter = iCounter + 1;

if(header_flag_ok!=1):
    print("header nel file non letto correttamente");
    sys.exit(0);
    
df=df[0:10]
print(labels)
print(df)

print(df.corr())
correlation_matrix(df,labels)



