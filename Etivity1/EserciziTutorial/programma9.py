def prima_procedura():
    seconda_procedura()
    print("Ciao, sono la prima procedura")
    return

def seconda_procedura():
    print("Ciao, sono la seconda procedura")
    return


print("Qui inizia lesecuzione del programma.")
prima_procedura()
print("Fine del programma.")