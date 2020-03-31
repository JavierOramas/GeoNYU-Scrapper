import zipfile
import os
from os import path
import json
import pygeoj
import unicodedata

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
                if f.endswith('.zip'):
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

def convert_to_geojson(directory:str, mode:bool, maxnum:int = 100):
    os.makedirs('geojsons', exist_ok=True) #crear carpeta destino de los json
    
    for cp,dir,files in os.walk(directory): #recorrer todo el directorio de los shapefiles
       for f in files:                      #recorrer todos los .zip 
            # try:
                if f.endswith('.zip'):
                    zf = zipfile.ZipFile(path.join(directory,str(f)),'r') #cargar los .zip
                    os.makedirs('decompress', exist_ok=True)         #crear la carpeta de trabajo
                    filename = ''                                     
                    for i in zf.namelist():                        #recorrer todo el .zip
                        zf.extract(i, path='decompress', pwd=None)   #extraer los archivos en la carpeta de trabajo
                        if i[-3:] == 'shp':                          #si el archivo es el .shp
                            filename = i                             #guardar el nombre
                    
                    outputfi = f[:-3]+'json'                          #fichero .geojson de salida
                    outputfo = path.join('geojsons',outputfi)      #direccion del fichero de salida
                    inputf = path.join('decompress',filename)    
                    
                    os.system('ogr2ogr -f "GeoJSON" '+outputfo+' '+inputf) #convertir con ogr2ogr de shp a geojson
                    if mode:
                        split_polygons(pygeoj.load('geojsons/'+outputfi),maxnum,outputfi[:-4]+'splitted.json')
                    else:
                        count_points(pygeoj.load('geojsons/'+outputfi))
                    os.system('rm -rf decompress')                   #eliminar la carpeta de trabajo         
            # except:
            #   pass
    
    os.system('rm -rf geojsons/')                

def split_polygons(json_file, maxnum,addr):
    a = []
    index = 0
    f = json_file
    fi = open('upload/'+addr, 'w')
    f.features = []
    dic = {}
    dic['poligonos'] = []
    for i in json_file:
        index = index+1
        coordinates = i.geometry.coordinates[0]
        last_idx = 0
        new_list = []
        
        while not len(coordinates)-last_idx < maxnum:
            new_list.insert(-1, coordinates[last_idx:min(last_idx+maxnum, len(coordinates))])
            last_idx = last_idx+maxnum+1
        new_list.append(coordinates[last_idx:])
        for j in new_list:
            dictio = dict(i.properties)
            dictio = clean_dict(dictio)
            dictio['index'] = index
            dictio['geometry'] = j
            dic['poligonos'].append(dictio)
    fi.write(json.dumps(dic, default=str)+'\n')
    fi.close()

def clean_dict(dictio):
    dictio.pop('ID_0', None)
    dictio.pop('ISO', None)
    dictio.pop('HASC_1',None)
    dictio.pop('CCN_1', None)
    dictio.pop('CCA_1', None) 
    dictio.pop('NL_NAME_1', None)
    dictio.pop('HASC_2',None)
    dictio.pop('CCN_2', None)
    dictio.pop('CCA_2', None) 
    dictio.pop('NL_NAME_2', None)
    dictio.pop('HASC_3',None)
    dictio.pop('CCN_3', None)
    dictio.pop('CCA_3', None) 
    dictio.pop('NL_NAME_3', None)
    dictio.pop('HASC_4',None)
    dictio.pop('CCN_4', None)
    dictio.pop('CCA_4', None) 
    dictio.pop('NL_NAME_4', None)
    dictio.pop('HASC_5',None)
    dictio.pop('CCN_5', None)
    dictio.pop('CCA_5', None) 
    dictio.pop('NL_NAME_5', None)
    dictio.pop('HASC_6',None)
    dictio.pop('CCN_6', None)
    dictio.pop('CCA_6', None) 
    dictio.pop('NL_NAME_6', None)
    return dictio
            
        
def count_points(json_file):
    a = []
    for i in json_file:
        coordinates = i.geometry.coordinates[0]
        a.append([i.properties['NAME_0'] ,len(coordinates)])
    a.sort()
    print(a[0][0])
    print([i[1] for i in a])