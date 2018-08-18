# --------------------------------------------------------------
# ---------     INSTALACIÓN DE PAQUETES Y MÓDULOS     ----------

from selenium import webdriver
from time import sleep
import requests
import colorsys
import json
import os
import PyPDF2
from pybtex.database.input import bibtex

# --------------------------------------------------------------




# --------------------------------------------------------------

class color:
    BOLD = '\033[1m'
    END = '\033[0m'

# --------------------------------------------------------------




# --------------------------------------------------------------
# ------------------     CONSEGUIR TOKEN     -------------------

email = input('\nIntroduzca su dirección email de Mendeley: ')
password = input('Introduzca su contraseña de Mendeley: ')

chrome_path = 'C:\\Users\\Mireya\\Desktop\\chromedriver.exe'
driver = webdriver.Chrome(chrome_path)

url = 'https://mendeley-show-me-access-tokens.herokuapp.com/'
driver.get(url)
driver.find_element_by_xpath("//*[@id='login']/a").click()
sleep(1)

driver.find_element_by_id('username').send_keys(email)
driver.find_element_by_id('password').send_keys(password)
driver.find_element_by_xpath('//*[@id="login"]/div[2]/button').click()
sleep(1)

access_token=driver.find_element_by_xpath('//*[@id="oauth"]/dl/dd[1]')
sleep(1)

# --------------------------------------------------------------
# --------------------------------------------------------------



# --------------------------------------------------------------
# ---------------     MENÚ DE OPCIONES     ---------------------

while True:
    task = input('\n¿Qué desea hacer? (Introduzca un número)'
         '\n\t1. Ver el listado de referencias y documentos '
         'con posibilidad de borrar alguna/o'
         '\n\t2. Subir un documento'
         '\n\t3. Salir\nRespuesta: ')

    if task.isnumeric() == False:
        task = input('\n¿Qué desea hacer? (Introduzca un número)'
             '\n\t1. Ver el listado de referencias y documentos '
             'con posibilidad de borrar alguna/o'
             '\n\t2. Subir un documento'
             '\n\t3. Salir\nRespuesta: ')

    if task.isnumeric() == True:
        task = int(task)
        if task > 3 or task < 1:
            task = input('\n¿Qué desea hacer? (Introduzca un número)'
                 '\n\t1. Ver el listado de referencias y documentos '
                 'con posibilidad de borrar alguna/o'
                 '\n\t2. Subir un documento'
                 '\n\t3. Salir\nRespuesta: ')



        if task == 3:
            break
# --------------------------------------------------------------



# --------------------------------------------------------------
# ------------------      LEER/BORRAR      ---------------------

# - - - - - - -       LEER lista de arc/ref      - - - - - - - -

        if task == 1:
            url = "https://api.mendeley.com/documents"
            headers = {
                'Authorization': "Bearer " + access_token.text,
            }
            list = requests.request("GET", url, headers=headers)

            print(color.BOLD+'\nListado de publicaciones: '+color.END)
            parsed = json.loads(list.text)
            print(json.dumps(parsed, indent = 4, sort_keys=True))


# - - - - - -       BORRAR una entrada       - - - - - - - - -

            delete = input('\nSi desea borrar alguna publicación '
                    'introduzca el título del mismo'
                    '\nSi no desea eliminar nada escriba: no'
                    '\nRespuesta: ')
            if delete == 'no':
                pass
            else:
                select_id = delete
                div1 = list.text.split(select_id)[1]
                div2 = div1.split('id":"')[1]
                id = div2.partition('",')[0]
                print('ID: ', id)

                url = "https://api.mendeley.com/documents/"+id
                headers = {
                    'Authorization': "Bearer " + access_token.text,
                }
                deleted=requests.request("DELETE",url,headers=headers)

                print(deleted)

# --------------------------------------------------------------
# --------------------------------------------------------------



# --------------------------------------------------------------
# ------------      SUBIR el archivo a Mendeley     ------------

# - - - - - -    PEDIR NOMBRE CARPETA Y ARCHIVO      - - - - - -

        if task == 2:
            folder = input('\nIntroduzca el nombre de la carpeta en'
                           ' la que se encuentra el archivo: ')
            os.chdir(folder)
            file_name = input('Introduzca el nombre del archivo '
                              'con su extensión: ')
            ext = file_name[-3::]

# - - - - - - - -   Distinguir según extensión     - - - - - - -

            if ext == 'txt':
                f = open(file_name, "r")
                f.close()
            if ext == 'pdf':
                pdfFileObj = open(file_name, 'rb')
                pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
                pageObj = pdfReader.getPage(0)
                pdfFileObj.close()
            if ext == 'bib':
                parser = bibtex.Parser()
                bibdata = parser.parse_file(file_name)
                for bib_id in bibdata.entries:
                    entries = bibdata.entries[bib_id]

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

            url = "https://api.mendeley.com/documents"
            headers = {
                'Content-Disposition': "attachment; filename=" +file_name,
                'Accept': "application/vnd.mendeley-document.1+json",
                'Authorization': 'Bearer ' + access_token.text,
                'Content-Type': 'text/plain',
                'Content-Length': '11509',
                }
            files={'file': open(file_name,'rb')}
            postfile = requests.post(url, headers=headers, files=files)

            print(color.BOLD+'\nSe ha subido este archivo: '+color.END)
            print(postfile.text)

# --------------------------------------------------------------
# --------------------------------------------------------------

driver.close()
exit()