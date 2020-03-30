import zipfile
import os
from os import path
import json
import pygeoj

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

def convert_to_geojson(directory:str, mode:bool):
    os.makedirs('geojsons', exist_ok=True) #crear carpeta destino de los KML
    
    for cp,dir,files in os.walk(directory): #recorrer todo el directorio de los shapefiles
       for f in files:                      #recorrer todos los .zip 
            # try:
            zf = zipfile.ZipFile(path.join(directory,str(f).replace(' ', '\ ')),'r') #cargar los .zip
            os.makedirs('decompress', exist_ok=True)         #crear la carpeta de trabajo
            filename = ''                                     
            for i in zf.namelist():                        #recorrer todo el .zip
                zf.extract(i, path='decompress', pwd=None)   #extraer los archivos en la carpeta de trabajo
                if i[-3:] == 'shp':                          #si el archivo es el .shp
                    filename = i                             #guardar el nombre
            
            outputfi = f[:-3]+'json'                          #fichero .geojson de salida
            outputfo = path.join('geojsons',outputfi)      #direccion del fichero de salida
            inputf = path.join('decompress',filename)    
            
            os.system('ogr2ogr -f "GeoJSON" '+outputfo+' '+inputf) #convertir con ogr2ogr de shp a kml
            os.system('cp '+outputfo+' geojsons/'+outputfi)       #copiarlo a la carpeta KML
            if mode:
                split_polygons(pygeoj.load('geojsons/'+outputfi),10)
            else:
                count_points(pygeoj.load('geojsons/'+outputfi))
            #os.system('rm -rf decompress')                   #eliminar la carpeta de trabajo         
            # except:
            #   pass

def split_polygons(json_file, maxnum):
    a = []
    for i in json_file:
        coordinates = i.geometry.coordinates[0]
        a.append([i.properties['NAME_0'] ,len(coordinates)])
        # last_idx = 0
        # new_list = []
        # while len(coordinates)-last_idx > maxnum:
        #     new_list.insert(-1, coordinates[last_idx:last_idx+maxnum])
        #     last_idx = last_idx+maxnum+1
        # i.geometry.coordinates[0] = [new_list]
        # print(len(i.geometry.coordinates))
    # json_file.save('geojsons/test2.json')
    a.sort()
    print(a[0][0])
    print([i[1] for i in a])
    
def count_points(json_file):
    a = []
    for i in json_file:
        coordinates = i.geometry.coordinates[0]
        a.append([i.properties['NAME_0'] ,len(coordinates)])
        # last_idx = 0
        # new_list = []
        # while len(coordinates)-last_idx > maxnum:
        #     new_list.insert(-1, coordinates[last_idx:last_idx+maxnum])
        #     last_idx = last_idx+maxnum+1
        # i.geometry.coordinates[0] = [new_list]
        # print(len(i.geometry.coordinates))
    # json_file.save('geojsons/test2.json')
    a.sort()
    print(a[0][0])
    print([i[1] for i in a])