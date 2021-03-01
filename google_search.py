import urllib.request
import time
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from urllib.request import urlopen, Request
import re
import urllib.parse

search_term = 'Megalodon Hai'
#search_term = df1.iloc[i][0]
search_term = urllib.parse.quote_plus(search_term)
print('empty link: ', search_term)
req = Request(f"https://www.google.de/search?q={search_term}", headers={'User-Agent': 'Mozilla/5.0'})
html = urlopen(req)
soup = BeautifulSoup(html, 'html.parser')
# div mit class = g
# result = soup.find("div", {"class": "g"})
# # darin a tag finden
# if result is not None:
#     print(result)
#     google_link = result.find('a', href=True)
#     df1[[i, 'link']] == google_link['href']
#     print(google_link)
# print('------------------------------')
for div1 in soup.find_all("div", {"class": "g"}):
    
    try:
        print(div1.find('h2'))
        div2 = div1.find('div')
        div3 = div2.find('div')
        print(div3.find('a', href = True))
        #print(r.find('div', attrs={'class':'s3v9rd'}).get_text())
    except:
        continue
print('---------')