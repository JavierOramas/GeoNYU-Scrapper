Herramienta de web scrapping para descargar todos los poligonos de https://geo.nyu.edu que contengan informacion administrativa

Para instalar todos los paquetes necesarios ejecutar pip install -r requirements.txt

intrucciones:
python geonyu-scrapper.py get-description - retorna el archivo description.json (país:nivel,tipo de datos)
python geonyu-scrapper.py get-polygons - descarga todos los poligonos como .zip en la carpeta shapefiles 
