import re
import requests
from bs4 import BeautifulSoup
from href_extract import Extract_href
import os.path as path
import os

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'}

payload = {
    'query':'test'
}

r = requests.get('https://geo.nyu.edu/?per_page=10&q=%22-level+administrative+division%22+%22polygon%22+%22public%22+%22stanford%22',data = payload ,headers = headers)

soup = BeautifulSoup(r.text,'lxml')
items = soup.findAll('h3', {'class':'index_title col-sm-9s cosl-lg-10 text-span'})


links = Extract_href(items)
shps = []
name = []
for i in links:
    # print(path.join('https://geo.nyu.edu',))
    r2 = requests.get(path.join('https://geo.nyu.edu',i[1:]), data=payload, headers=headers)
    dwnld = BeautifulSoup(r2.text, 'lxml')
    shps.append(dwnld.findAll('a', {'class': 'btn btn-primary btn-block download download-original'}))
    name.append(dwnld.findAll('span', {'itemprop': 'name'}))
#print(name)
shps_links = Extract_href(shps)
# print(len(shps_links))
# print(len(shps))
# print(len(name))      

# for i in range(len(shps_links)):
#     os.makedirs('shapefiles',exist_ok=True)
#     print(str(name[i])[len('<span itemprop="name"> '):-len(' </span>')])
#     with open('shapefiles/'+str(name[i])[len('<span itemprop="name">'):-len('</span>')]+'.zip', 'wb') as f:
#         f.write(requests.get(shps_links[i][:-len('>Original')],data=payload,headers=headers).content)

