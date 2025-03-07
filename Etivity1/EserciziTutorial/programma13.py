import PyPDF2                                               # libreria per manipolare i PDF
import re                                                   # modulo per esegure ricerche con espressioni regolari

pattern = input("Immetti il testo da cercare: ")
fileName = input("Immetti il percorso e il nome del file: ")

object = PyPDF2.PdfFileReader(fileName)                     # accedo al PDF
numPages = object.getNumPages()                             # conto le pagine del pdf

for i in range(0, numPages):                                # analizzo per i =(0,numPages) ---> da 0 a n.pagine contante in precedenza
    pageObj = object.getPage(i)                             # accedo alla pagina i-esima
    text = pageObj.extractText()                            # estraggo (leggo) il testo della pagina
   
    for match in re.finditer(pattern, text):                # cerco il pattern nel testo della pagina i-esima che sto analizzando
        print(f'Page no: {i} | Match: {match}')             # se lo trovo stampo la pagina i-esima e l'oggetto match
