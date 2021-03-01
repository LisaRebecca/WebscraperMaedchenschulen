import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from urllib.request import urlopen

url = 'https://de.wikipedia.org/wiki/Liste_bestehender_M%C3%A4dchenschulen_im_deutschsprachigen_Raum'
html = urlopen(url) 
soup = BeautifulSoup(html, 'html.parser')

# deutschland = soup.find('h2')
tables = soup.find_all('table')

names = []
locations = []
types = []
coordinates = []
links = []

for table in tables:
    rows = table.find_all('tr')
    
    for row in rows:
        cells = row.find_all('td')


        if len(cells) > 1:
            # link = row.find_all('a')
            # if len(link)>0:
            #     links.append(link)
            # else: 
            links.append("a")

            name = cells[0]
            names.append(name.text)

            
            location = cells[1]
            locations.append(location.text.strip())
            
            schooltype = cells[2]
            types.append(schooltype.text.strip())
            
df1 = pd.DataFrame(locations, index= names, columns = ['location'])
df1['schooltype'] = types
df1['link'] = links
#df1['coordinates'] = coordinates

df1.to_excel("output.xlsx")
print('Anzahl der gefundenen Schulen: ', df1.shape[0])
print(df1.head(5))