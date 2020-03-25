import re
import requests
from bs4 import BeautifulSoup
from extras import Extract_href
from extras import Extract_description
from extras import Remove_extra
import os.path as path
import os
import json
import typer
from pyexcel_ods import save_data
from collections import OrderedDict

app = typer.Typer()

elems = []

def scrapper(action):
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'}

    payload = {
        'query':'test'
    }
    page ='https://geo.nyu.edu/?per_page=100&q=%22-level+administrative+division%22+%22polygon%22+%22public%22+%22stanford%22' #pagina inicial
    cont = 0
    try:
        while(True):
            cont = cont+1
            print("Processing page "+str(cont))
            r = requests.get(page,data = payload ,headers = headers)
            soup = BeautifulSoup(r.text,'lxml') #cargar pagina principal
            items = soup.findAll('h3', {'class':'index_title col-sm-9s cosl-lg-10 text-span'}) #tomar los elementos devueltos (poligonos)
            nextp = Extract_href(soup.findAll('a', {'rel':'next'}))
            links = Extract_href(items) #sacar los links de los elementos
            shps = [] #lista donde van a estar los links de descarga
            name = [] #lista donde van a estar los nombres de cada elemento
            desc = [] #lista donde van a estar los nombres de cada elemento
            for i in links:
                r2 = requests.get(path.join('https://geo.nyu.edu',i[1:]), data=payload, headers=headers) #cargar la pagina de cada elemento
                dwnld = BeautifulSoup(r2.text, 'lxml') 
                shps.append(dwnld.findAll('a', {'class': 'btn btn-primary btn-block download download-original'})) #seleccionar los links de descarga de cada pagina
                name.append(dwnld.findAll('span', {'itemprop': 'name'})) #seleccionar los nombres de cada elemento
                desc.append(dwnld.findAll('div', {'class': 'truncate-abstract'}))
            shps_links = Extract_href(shps) #sacar los links solos
            for i in range(len(shps_links)): #iterar sobre los links de descarga
                os.makedirs('shapefiles',exist_ok=True) #crear el directorio donde van a guardarse los archivos
                if action:
                    with open('shapefiles/'+str(name[i])[len('<span itemprop="name">'):-len('</span>')]+'.zip', 'b') as f: #descargar el archivo
                        f.write(requests.get(shps_links[i][:-len('>Original')],data=payload,headers=headers).contnt)
                else:
                    elems.append(Remove_extra(str(name[i]).split(',')[1], Extract_description(str(desc[i]))))
            if len(nextp[0][1:]) < 3:
                data = {}
                data['Sheet1'] = elems
                print(elems)
                print(data['Sheet1'])
                save_data('descriptions.ods', data)
                return
            page = path.join('https://geo.nyu.edu',nextp[0][1:]) #cambiar a la pagina siguiente
    except:
        pass


from colorama import Fore

@app.command(name='get-polygons' ,help='Download all the polygons from geo.nyu.edu')
def get_polygons():
    scrapper(True)
    print(Fore.GREEN+"Done!")
    
@app.command(name='get-description' ,help='Download the description of all polygons from geo.nyu.edu')
def get_description():
    scrapper(False)
    print(Fore.GREEN+"Done!")

if __name__ == "__main__":
    app()
