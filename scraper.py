import requests
import bs4
from flask import request
from parsel import Selector
import enlighten
import json
import os
import logging
import time
import typer
import requests_html

app = typer.Typer()

logging.basicConfig(level=logging.DEBUG)
manager = enlighten.get_manager()

FOLDER = 'KMZ'

os.makedirs(FOLDER,exist_ok=True)

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
session = requests_html.HTMLSession()
#params = {}
# session.headers.update({'User-Agent': user_agent})
BASE_URL = 'https://gadm.org/download_country_v3.html'
r = session.get(BASE_URL)

@app.command(help='Get the info of all site')
def get_all():

    letter_pages = []
    soup = bs4.BeautifulSoup(r.html.html, 'lxml')
    print('page')
    x = soup.body.find('select', attrs={'id:countrySelect'})
    
if __name__ == "__main__":
    app()

