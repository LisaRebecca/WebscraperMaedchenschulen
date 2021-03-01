import urllib.request
import time
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from urllib.request import urlopen, Request
import re
import urllib.parse

def main():
    # read wikipedia
    df1 = read_wikipedia()

    # visit the sites
    # search for the emails
    #visit_sites(df1)

    # write to excel
    df1.to_excel("output.xlsx")

def read_wikipedia():

    url = 'https://de.wikipedia.org/wiki/Liste_bestehender_M%C3%A4dchenschulen_im_deutschsprachigen_Raum'
    html = urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')

    tables = soup.find_all('table')

    names = []
    locations = []
    types = []
    links = []

    wikilink = re.compile('/wiki/|/w/')
    #source_annotation = re.compile(r'\[ [0-9]* \]')

    # alle tabellen auf der wiki-seite
    for table in tables:
        tr = table.find_all('tr')

        for row in tr:
            tds = row.find_all('td')

            if len(tds) > 1:
                name = tds[0]

                # eventuelle source-annotationen abschneiden
                names.append(re.split(r' \[', name.text)[0])

                a = tds[0].find('a', href=True)

                if a is None:
                    links.append('')
                else:
                    # wir wollen keine wiki-links!
                    if wikilink.search(str(a['href'])) is None:
                        #print(name.text, a['href'])
                        links.append(a['href'])
                    else: links.append('')

                location = tds[1]
                locations.append(location.text.strip())

                schooltype = tds[2]
                types.append(schooltype.text.strip())

    #df1 = pd.DataFrame(locations, columns = ['location'])
    df1 = pd.DataFrame(list(zip(names, links, types, locations)), columns= ['name', 'link', 'schooltype', 'location'])
    print(df1.iloc[15])
    
    #for i in range(1, df1.shape[0]):
    for i in range(1, 5):
        if df1.iloc[i]['link'] == '':
            search_term = df1.iloc[i][0]
            search_term = urllib.parse.quote_plus(search_term)
            print('empty link ', search_term)
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
            for r in soup.find_all('div'):
                try:
                    print(r.find('a', href = True))
                    print(r.find('div', attrs={'class':'vvjwJb'}).get_text())
                    print(r.find('div', attrs={'class':'s3v9rd'}).get_text())
                except:
                    continue
            print('---------')
    print('Anzahl der gefundenen Schulen: ', df1.shape[0])
    return df1

def visit_sites(df1):
    #df1 = pd.read_excel('output.xlsx', index_col=0)
    #print(df1.head(30))

    emails = ['no mail']*len(df1)
    for i in range(0, len(df1)):
        link = str(df1.iloc[i]['link'])

        if not (link == 'nan'):
            # print('no nan')
            if not (len(link)>0):
                # print('i continued')
                continue
            print('url:', link)
            try:
                html = urlopen(link)
                soup = BeautifulSoup(html, 'html.parser')

                if not soup.title is None:
                    print('page title:', soup.title.text)
                    text = soup.prettify()
                else:
                    print('page title: none')
                # impressum als link
                # 'at'
                email = re.findall(r'\w+@\S+.de', str(text))
                if(len(email)>0):
                    print('found emails:', email)
                    print()
                else:
                    print('found emails: none')
                    print()
            except:
                print('fehler bei url')
                print()
        emails[i] = email
    df1['emails'] = emails

if __name__ == "__main__": main()
