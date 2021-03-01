import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from urllib.request import urlopen

url = 'https://en.wikipedia.org/wiki/Epidemiology_of_depression'
html = urlopen(url) 
soup = BeautifulSoup(html, 'html.parser')
tables = soup.find_all('table')

#convert number as string to integer
#re.sub() returns the substring that match the regrex
import re
def process_num(num):
    return float(re.sub(r'[^\w\s.]','',num))

num1 = re.sub(r'[^\w\s.]','','1,156.30')
num1

ranks = []
rates = []
countries = []
links = []

for table in tables:
    rows = table.find_all('tr')
    
    for row in rows:
        cells = row.find_all('td')
        
        if len(cells) > 1:
            rank = cells[0]
            ranks.append(int(rank.text))
            
            country = cells[1]
            countries.append(country.text.strip())
            
            rate = cells[2]
            rates.append(process_num(rate.text.strip()))
            
            link = cells[1].find('a').get('href')
            links.append('https://en.wikipedia.org/'+ link)
            
df1 = pd.DataFrame(ranks, index= countries, columns = ['Rank'])
df1['DALY rate'] = rates

print(df1.head(10))