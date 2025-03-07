from time import localtime                                  #importa la funzione localtime() dal modulo time di Python

# Insieme Chiave - Valore

mia_Agenda={8:'Sleeping',
            9:'Breakfast',
            12:'pranzo dallo zozzone',
            17:'Working',
            18:'Dinner',
            20:'Tennis',
            22:'Gaming'
            }

print(mia_Agenda)
# Richiava il valore di mia_Agenda in funzione della chiave [22]
print(mia_Agenda[22])
time_now = localtime()
print(time_now)
hour=time_now.tm_hour
minuti=time_now.tm_min
s="Sone le {0}:{1}".format(hour,minuti)
print(s)

for activity_time in sorted(mia_Agenda.keys()):         # Scansiona le ore dell'agenda in ordine crescente
    if hour < activity_time:                            # Se l'ora attuale è minore dell'ora dell'attività
        print(mia_Agenda[activity_time])                # Stampa la prossima attività
        break                                           # Esce dal ciclo dopo aver trovato la prima attività successiva ed evita che vengano stampate tutte le attività rimanenti
else:
    print('Nulla da segnalare - Niente annotato in agenda')                         # Se non trova attività future, stampa questo messaggio
