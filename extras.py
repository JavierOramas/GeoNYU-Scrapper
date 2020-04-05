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
        #    try:
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
        #    except:
        #       pass

def convert_to_json(directory:str, mode:bool, maxnum:int = 100):
    import shapefile
    os.makedirs('geojsons', exist_ok=True) #crear carpeta destino de los json
    
    for cp,dir,files in os.walk(directory): #recorrer todo el directorio de los shapefiles
       for f in files:                      #recorrer todos los .zip 
            # try:
                if f.endswith('.zip'):
                    zf = zipfile.ZipFile(path.join(directory,str(f)),'r') #cargar los .zip
                    os.makedirs('decompress', exist_ok=True)         #crear la carpeta de trabajo
                               
                    for i in zf.namelist():                        #recorrer todo el .zip
                        zf.extract(i, path='decompress', pwd=None)   #extraer los archivos en la carpeta de trabajo
                        if i.endswith('.shp'):                          #si el archivo es el .shp
                            filename = i                             #guardar el nombre
                    
                    outputfi = f[:-3]+'.json'                          #fichero .geojson de salida
                    outputfo = path.join('geojsons',outputfi)      #direccion del fichero de salida
                    inputf = path.join('decompress',filename)
                    
                    reader = shapefile.Reader(inputf)
                    #reader.schema = 'iso19139'
                    fields = reader.fields[1:]
                    field_names = [field[0] for field in fields]
                    buffer = []
                    for sr in reader.shapeRecords():
                        atr = dict(zip(field_names, sr.record))
                        geom = sr.shape.__geo_interface__
                        buffer.append(dict(type="Feature", \
                            geometry=geom, properties=atr)) 
                    
                    # write the GeoJSON file
                    from json import dumps
                    geojson = open(outputfo, "w")
                    geojson.write(dumps({"type": "FeatureCollection",\
                        "features": buffer}, indent=2) + "\n")
                    geojson.close()


                    index = 0
                    fi = open('upload/'+outputfi, 'w')
                    f.features = []
                    dic = {}
                    dic['poligonos'] = []
                    count = 0

                    for i in pygeoj.load('geojsons/'+outputfi):
                        
                        index = index+1
                        
                        if i.geometry.type == 'MultiPolygon':
                            for j in i.geometry.coordinates:
                                count = count + process_multipolygon(i,j,maxnum,dic,count,index,'MultiPolygon')
                        else:
                            dic['type'] = 'Polygon'
                            count = count + process_polygon(i,maxnum,dic,count,index,'Polygon')
                        
                        dic['total'] = count
                        fi.write(json.dumps(dic, default=str)+'\n')
                    fi.close()
    
def process_multipolygon(i,j,maxnum,dic,index,type_of_geometry):
    last_idx = 0
    new_list = []
    index_2 = 0
    for coordinates in j:
        while last_idx <= len(coordinates):
            new_list.append(coordinates[last_idx:min(len(coordinates),last_idx+maxnum)])
            last_idx = last_idx+maxnum
            
        for k in new_list:
            index_2 = index_2+1
            dictio = dict(i.properties)
            dictio = clean_dict(dictio)
            dictio['type'] = type_of_geometry
            dictio['index'] = index
            dictio['index_2'] = index_2
            dictio['geometry'] = k
            dic['poligonos'].append(dictio)
    
    return len(new_list)

def process_polygon(i,maxnum,dic,index,type_of_geometry):
    last_idx = 0
    new_list = []

    for coordinates in i.coordinates:
        index = index+1
        while last_idx < len(coordinates):
            new_list.append(coordinates[last_idx:min(len(coordinates),last_idx+maxnum)])
            last_idx = last_idx+maxnum
    
        for j in new_list:
            dictio = dict(i.properties)
            dictio = clean_dict(dictio)
            dictio['type'] = type_of_geometry
            dictio['index'] = index
            dictio['geometry'] = j
            dic['poligonos'].append(dictio)
            
    return len(new_list)

def clean_dict(dic):
    keys_needed = ['ID_0', 'ID_1', 'ID_2','ID_3','ID_4','ID_5','ID_6','NAME_0','NAME_1','NAME_2','NAME_3','NAME_4','NAME_5','NAME_6', 'geometry']
    
    if 'NAME_ENGLI' in dic.keys():
        dic["NAME_0"] = dic["NAME_ENGLI"]
    
    for i in dic.keys():
        if not i in keys_needed:
            dic.popitem(i)
    
    return dic        
    
def count_points(json_file):
    a = []
    for i in json_file:
        coordinates = i.geometry.coordinates[0]
        a.append([i.properties['NAME_0'] ,len(coordinates)])
    a.sort()
    print(a[0][0])
    print([i[1] for i in a])