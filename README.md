GeoNYU-Scrapper
===============

Herramienta de web scrapping para descargar todos los poligonos de https://geo.nyu.edu que contengan informacion administrativa

Para instalar todos los paquetes necesarios ejecutar pip install -r requirements.txt

es necesario instalar gdal en el sistema:
* sudo apt-get install gdal (ubuntu)
* sudo pacman -S gdal (Arch)


intrucciones:
* python geonyu-scrapper.py get-description - retorna el archivo description.ods (país,nivel,tipo de datos)
* python geonyu-scrapper.py get-polygons [MAXNUM (cantidad máxima de puntos por trozo)] - descarga todos los poligonos picados en 'trozos' de 100 puntos como .json en la carpeta upload 
* python geonyu-scrapper.py get-country ['word(s)']- descarga todos los poligonos resultado de la busqueda del país picados en 'trozos' de 100 puntos como .json en la carpeta upload 
* python geonyu-scrapper.py convert (OPTIONAL) [MAXNUM (cantidad máxima de puntos por trozo)]- convierte todos los archivos shapefile (en .zip) de la carpeta shapefile a .json (en la carpeta upload, picados en 'trozos' de 100 puntos)
* python geonyu-scrapper.py count devuelve la cantidad de puntos que tiene cada poligono de los ficheros en la carpeta shapefile
