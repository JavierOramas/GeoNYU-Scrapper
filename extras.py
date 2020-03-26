import zipfile
import os
from os import path

def Extract_href(elements):
    new_list = []
    for item in elements:
        temp_list = str(item).split(" ")
        for i in temp_list:
            if i[:4] == 'href':
                new_list.append(i[6:-1])
    return new_list

def Extract_description(item):
    li = item.split('.')
    resp = ''
    for i in li:
        if i[:len(' Level')] == ' Level':
            resp = i
    
    return resp

def Remove_extra(country,cad):
    elem = cad.split('divisions include')
    
    if len(elem) < 2:
        dat = [country,"",""]
    else:
        dat = [country[1:],elem[0][1:-1],elem[1][1:]]

    #print(dat)
    return dat

def convert_to_kml(directory:str):
    os.makedirs('KML', exist_ok=True) #crear carpeta destino de los KML
    
    for cp,dir,files in os.walk(directory): #recorrer todo el directorio de los shapefiles
       for f in files:                      #recorrer todos los .zip 
           try:
                zf = zipfile.ZipFile(path.join(directory,f),'r') #cargar los .zip
                os.makedirs('decompress', exist_ok=True)         #crear la carpeta de trabajo
                filename = ''                                     
                for i in zf.namelist():                          #recorrer todo el .zip
                    zf.extract(i, path='decompress', pwd=None)   #extraer los archivos en la carpeta de trabajo
                    if i[-3:] == 'shp':                          #si el archivo es el .shp
                        filename = i                             #guardar el nombre

                outputfi = f[:-3]+'kml'                          #fichero .kml de salida
                outputfo = path.join('decompress',outputfi)      #direccion del fichero de salida
                inputf = path.join('decompress',filename)        #direccion del fichero .shp de entrada

                os.system('ogr2ogr -f KML '+outputfo+' '+inputf) #convertir con ogr2ogr de shp a kml
                os.system('cp '+outputfo+' KML/'+outputfi)       #copiarlo a la carpeta KML
                os.system('rm -rf decompress')                   #eliminar la carpeta de trabajo
           except:
              pass
                