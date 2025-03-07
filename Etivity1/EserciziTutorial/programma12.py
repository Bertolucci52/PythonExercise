
# """ ... """ --> genera una stringa multilinea
data = """
0.000000    -2.6881
3.336670    -4.3010
6.673340    -5.3763
1.001001    -6.9892
1.334668    -1.1290
1.668335    -1.4516
2.002002    -2.0430
2.335669    -2.5268
2.669336    -3.1182
3.003003    -3.8709
3.336670    -4.6236
3.670337    -5.4300
4.004004    -6.2365
4.337671    -7.1505
4.671338    -8.0107
5.005005    -8.9246
5.338672    -9.8924
5.672339    -1.0806
6.006006    -1.1774
6.339673    -1.2741
6.673340    -1.3709
7.007007    -1.4677
7.340674    -1.5752
7.674341    -1.6720
8.008008    -1.7688
8.341675    -1.8655
8.675342    -1.9731
9.009009    -2.0752
9.342676    -2.1827
9.676343    -2.2849
""".split('\n')             # spezza in righe così da creare una lista

print(len(data))
print(data)

# prendo i valori dalla lista DATA ---> e li riporto in due nuove liste T e Y ---> prima di riportarli con append li converto

tlist = []
ylist = []
for s in data:                  # Scansiona ogni riga della lista "data"
    if s:                       # Evita righe vuote
        t, y = s.split()        # Divide la riga nei due numeri (come stringhe)
        t = float(t)            # Converte "t" in float (numero decimale)
        y = float(y) / 100.0    # Converte "y" in float e lo trasforma in metri
        tlist.append(t)         # Aggiunge il valore di t alla lista tlist
        ylist.append(y)         # Aggiunge il valore di y alla lista ylist


import matplotlib.pyplot as plt
plt.title('y-position vs. time for falling cupcake paper')
plt.xlabel('t (s)')
plt.ylabel('y (m)')
plt.plot(tlist,ylist,'m.')
plt.show()
