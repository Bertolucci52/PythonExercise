#concatenazione di testi --> il risultato di c sarà testo input a (5) + testo input b (3)= 53
print("Python: concatenazione testuale")
a = input("inserisci un numero: ")
b = input("inserisci un numero: ")
c = a+b
print("la variabile c è uguale a: ",c)
s = "La somma di {0} + {1} vale {2}".format(a,b,c)
print(s)

#per lavorare con dei numeri devo definire l'input come integer

print("Python - Somma integer")
x = int(input("Immetti un numero: "))
y = int(input("Immetti un secondo numero: "))
z = x + y
somma = ("Effettuo somma tra {0} e {1} = {2}").format(x,y,z)
print(somma)