# ho definito una funzione "prima_procedura()" che è chiamata ad eseguire una print solo dopo essere stata invocata (riga 7 "prima_procedura()")
def prima_procedura():
    print("Ciao, sono la prima procedura")
    return
# inizio del programma
print("Qui inizia lesecuzione del programma.")
prima_procedura()
print("Fine del programma.")