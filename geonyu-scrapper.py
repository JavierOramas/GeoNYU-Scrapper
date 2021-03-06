
import requests
from bs4 import BeautifulSoup
from extras import Extract_href
from extras import Extract_description
from extras import Remove_extra
from extras import convert_to_json
import os.path as path
import os
import json
import typer
from pyexcel_ods import save_data
from collections import OrderedDict
import urllib.request
import string

app = typer.Typer()

elems = []

page ='https://geo.nyu.edu/?per_page=100&q=%22-level+administrative+division%22+%22polygon%22+%22public%22+%22stanford%22' #pagina inicial

def scrapper(action,page):
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'}

    payload = {
        'query':'test'
    }
    cont = 0
    while(True):
        cont = cont+1
    
        print("Processing page "+str(cont))
        r = requests.get(page,data = payload ,headers = headers)
        soup = BeautifulSoup(r.text,'lxml') #cargar pagina principal
        items = soup.findAll('h3', {'class':'index_title col-sm-9s cosl-lg-10 text-span'}) #tomar los elementos devueltos (poligonos)
        nextp = Extract_href(soup.findAll('a', {'rel':'next'}))
        links = Extract_href(items) #sacar los links de los elementos
        shps = [] #lista donde van a estar los links de descarga
        names = [] #lista donde van a estar los nombres de cada elemento
        desc = [] #lista donde van a estar los nombres de cada elemento
        for i in links:
            r2 = requests.get(path.join('https://geo.nyu.edu',i[1:]), data=payload, headers=headers) #cargar la pagina de cada elemento
            dwnld = BeautifulSoup(r2.text, 'lxml') 
            shps.append(dwnld.findAll('a', {'class': 'btn btn-primary btn-block download download-original'})) #seleccionar los links de descarga de cada pagina
            names.append(dwnld.findAll('span', {'itemprop': 'name'})) #seleccionar los nombres de cada elemento
            desc.append(dwnld.findAll('div', {'class': 'truncate-abstract'}))
        shps_links = Extract_href(shps) #sacar los links solos
        for i in range(len(shps_links)): #iterar sobre los links de descarga
            sleep(2)
            os.makedirs('shapefiles',exist_ok=True) #crear el directorio donde van a guardarse los archivos
            if action:
                #with open('shapefiles/'+str(name[i])[len('<span itemprop="name"> '):-len(' </span>')]+'.zip', 'w+b') as f: #descargar el archivo
                url = str(shps_links[i][:-len('>Original')])
                name = str(names[i])[len('<span itemprop="name"> '):-len(' </span>')]+'.zip'
                name = name.translate({ord(c): None for c in string.whitespace})
                urllib.request.urlretrieve(url,'shapefiles/'+name)
            else:
                elems.append(Remove_extra(str(name[i]).split(',')[1], Extract_description(str(desc[i]))))
        if len(nextp[0][1:]) < 3:
            data = {}
            data['Sheet1'] = elems
            save_data('descriptions.ods', data)
            return
        
        page = path.join('https://geo.nyu.edu',nextp[0][1:]) #cambiar a la pagina siguiente
        print(nextp[0][:])
        if len(nextp[0][1:]) <= 1:
            break



from colorama import Fore
from time import sleep

@app.command(name='get-custom' ,help='Download all the polygons result from search and splits all polygons in 100 points polygons')
def get_custom(country:str):
    page ='https://geo.nyu.edu/?utf8=✓&q=' #pagina inicial
    page = page+"+%22"+country+"%22"
    scrapper(True,page)
    convert_to_json('shapefiles/',True)
    os.system('rm -rf shapefiles')
    print(Fore.GREEN+"Done!")

@app.command(name='get-polygons' ,help='Download all the polygons from geo.nyu.edu and splits all polygons in 100 points polygons\
    \n Args: maxnum = maximum number of points per polygon (default 100)')
def get_polygons(maxnum:int = 1000):
    page ='https://geo.nyu.edu/?per_page=100&q=%22-level+administrative+division%22+%22polygon%22+%22public%22+%22stanford%22' #pagina inicial
    # page ='https://geo.nyu.edu/?page=73&per_page=10&q=%22-level+administrative+division%22+%22polygon%22+%22public%22+%22stanford%22' #pagina inicial
    scrapper(True,page)
    os.makedirs('upload', exist_ok=True)
    convert_to_json('shapefiles/',True,maxnum)
    os.system('rm -rf shapefiles')
    print(Fore.GREEN+"Done!")
    
@app.command(name='get-description' ,help='Download the description of all polygons from geo.nyu.edu')
def get_description():
    page ='https://geo.nyu.edu/?per_page=100&q=%22-level+administrative+division%22+%22polygon%22+%22public%22+%22stanford%22' #pagina inicial
    scrapper(False)
    print(Fore.GREEN+"Done!")
    

@app.command(name='convert' ,help='Converts all shapefiles in shapefile folder to json, output on upload folder\
    \n Args: maxnum = maximum number of points per polygon (default 100)')
def convert_polygons(maxnum:int = 1000):
    os.makedirs('upload', exist_ok=True)
    convert_to_json('shapefiles/',True,maxnum)
    print(Fore.GREEN+"Done!")
    
if __name__ == "__main__":
    app()
