import re
import requests
from bs4 import BeautifulSoup
from extras import Extract_href
from extras import Extract_description
import os.path as path
import os
import json
import typer

app = typer.Typer()

progress = 0
total = 100
progress_shp= 0
total_shp = 100

    
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
            # percents = soup.findAll('span', {'class': 'page_entries'})
            links = Extract_href(items) #sacar los links de los elementos
            shps = [] #lista donde van a estar los links de descarga
            name = [] #lista donde van a estar los nombres de cada elemento
            desc = [] #lista donde van a estar los nombres de cada elemento
            for i in links:
                # print(path.join('https://geo.nyu.edu',))
                r2 = requests.get(path.join('https://geo.nyu.edu',i[1:]), data=payload, headers=headers) #cargar la pagina de cada elemento
                dwnld = BeautifulSoup(r2.text, 'lxml') 
                shps.append(dwnld.findAll('a', {'class': 'btn btn-primary btn-block download download-original'})) #seleccionar los links de descarga de cada pagina
                name.append(dwnld.findAll('span', {'itemprop': 'name'})) #seleccionar los nombres de cada elemento
                desc.append(dwnld.findAll('div', {'class': 'truncate-abstract'}))
            #print(name)
            shps_links = Extract_href(shps) #sacar los links solos
            #print(len(shps_links))
            # print(len(shps))
            # print(len(name)) 
            for i in range(len(shps_links)): #iterar sobre los links de descarga
                total = len(shps_links)
                total_shp = len(shps_links)
                os.makedirs('shapefiles',exist_ok=True) #crear el directorio donde van a guardarse los archivos
                if action:
                    progress_shp = i
                    with open('shapefiles/'+str(name[i])[len('<span itemprop="name">'):-len('</span>')]+'.zip', 'b') as f: #descargar el archivo
                        f.write(requests.get(shps_links[i][:-len('>Original')],data=payload,headers=headers).contnt)
                else:
                    progress = i
                    elem = {str(name[i]).split(',')[1] : Extract_description(str(desc[i]))} #crear un elemento tipo diccionario
                    json_file = open('shapefiles/description.json',mode='a') #abrir archivo jso
                    json_file.write(json.dumps(elem, default=str)+'\n') #imprimir en el json el nuevo elemnto
            page = path.join('https://geo.nyu.edu',nextp[0][1:]) #cambiar a la pagina siguiente
    except:
        pass


# import streamlit as st
# # from dinamyc import scrapper
@app.command(name='get-polygons' ,help='Download all the polygons from geo.nyu.edu')
def get_polygons():
    scrapper(True)
    
@app.command(name='get-description' ,help='Download the description of all polygons from geo.nyu.edu')
def get_description():
    scrapper(False)
    
if __name__ == "__main__":
    app()
