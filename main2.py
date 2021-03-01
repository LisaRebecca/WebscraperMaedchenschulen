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

deutschland = soup.find_all('h2')

for d in deutschland:
    print(d.text)
    print(d.next_sibling)