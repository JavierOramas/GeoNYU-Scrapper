## Contributing [![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/dwyl/esta/issues)
[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2FJavierOramas%2FGeoNYU-Scrapper&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23D10000&title=hits&edge_flat=false)](https://hits.seeyoufarm.com)

GeoNYU-Scrapper


Herramienta de web scrapping para descargar todos los poligonos de https://geo.nyu.edu que contengan informacion administrativa

Para instalar todos los paquetes necesarios ejecutar pip install -r requirements.txt

intrucciones:
* python geonyu-scrapper.py get-description - retorna el archivo description.ods (país,nivel,tipo de datos)
* python geonyu-scrapper.py get-polygons [MAXNUM (cantidad máxima de puntos por trozo)] - descarga todos los poligonos picados en 'trozos' de 100 puntos como .json en la carpeta upload 
* python geonyu-scrapper.py get-custom ['word(s)']- descarga todos los resultados de la busqueda picados en 'trozos' de 100 puntos como .json en la carpeta upload 
* python geonyu-scrapper.py convert (OPTIONAL) [MAXNUM (cantidad máxima de puntos por trozo)]- convierte todos los archivos shapefile (en .zip) de la carpeta shapefile a .json (en la carpeta upload, picados en 'trozos' de 100 puntos)
