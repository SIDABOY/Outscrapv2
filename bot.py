import requests
import tabula
import pandas as pd
import pdfkit
import os
response = requests.get("https://outlettecnologico.cl/listaPrecios.pdf")
file = open("metadata.pdf", "wb")
file.write(response.content)
file.close()

tabula.convert_into('metadata.pdf', "nuevo.csv", output_format="csv", pages='all')
nuevo=pd.read_csv('nuevo.csv',header=[0],encoding ="ISO-8859-1") 

tabula.convert_into('listaPrecios.pdf', "antiguo.csv", output_format="csv", pages='all')
antiguo=pd.read_csv('antiguo.csv',header=[0],encoding ="ISO-8859-1")

result = nuevo[~(nuevo.SKU.isin(antiguo.SKU))]
print(len(result))
result.to_html("test.html")
#PDF
pdfkit.from_file('test.html', 'Lista.pdf')
if len(result) == 0:
    os.remove("metadata.pdf")
else:
    os.remove("listaPrecios.pdf")
    os.rename("metadata.pdf", "listaPrecios.pdf")    
    os.remove("nuevo.csv")
    os.remove("antiguo.csv")