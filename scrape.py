from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import re
import pandas as pd
from selenium import webdriver
from urllib.parse import urlsplit
import requests

class Scraper:

    def __init__(self):
        self.EXP_DIR = "results.xlsx"
        self.names = []
        self.locations = []
        self.types = []
        self.links = []
        self.schoolinfo = pd.DataFrame()

    def read_wikipedia(self):
        url = 'https://de.wikipedia.org/wiki/Liste_bestehender_M%C3%A4dchenschulen_im_deutschsprachigen_Raum'
        html = urlopen(url)
        soup = BeautifulSoup(html, 'html.parser')
        
        #print(soup.table.prettify())

        # all tables on the wiki page
        tables = soup.find_all('table')
        
        for table in tables:
            trows = table.find_all('tr')
            for row in trows:
                tcells = row.find_all('td')

                # if the row has at least one cell
                if len(tcells) > 1:
                    self.process_cells(tcells)
        
        df_schoolinfo = pd.DataFrame(list(zip(self.names, self.links, self.types, self.locations)), columns= ['name', 'link', 'schooltype', 'location'])
        self.schoolinfo = df_schoolinfo

    def process_cells(self, cells):

        # eventuelle source-annotationen abschneiden
        # example: Gymnasium [1] -> Gymnasium
        clean_name = re.split(r' \[', cells[0].text)[0]
        self.names.append(clean_name)

        # find links to the school website
        a = cells[0].find('a', href=True)
        if a is None:
            self.links.append('')
        else:
            # no wiki-links!
            wikilink_regex = re.compile('/wiki/|/w/')

            link = str(a['href'])

            if wikilink_regex.search(link) is None:
                self.links.append(a['href'])
            else: self.links.append('')

        location = cells[1]
        self.locations.append(location.text.strip())

        schooltype = cells[2]
        self.types.append(schooltype.text.strip())

    def find_missing_links(self):
        count_schools = int(self.schoolinfo.shape[0])

        for i in range(0, count_schools):
            school = self.schoolinfo.iloc[i]
            link = school['link']
            name = school['name']
            
            if link == '':
                new_link = self.perform_search(name)
                if new_link is not None:
                    self.schoolinfo.iloc[i]['link'] = new_link

    def perform_search(self, search_term):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(chrome_options=options)

        url = f"https://www.google.de/search?q={search_term}"
        driver.get(url)
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')

        div = soup.find('div', {'class': 'g'}) # we want the first result
        a = div.find('a')
        href = a['href']
        print(href)
        return href

    def get_email2(self, url):

        mail = 'empty'
        if url == None:
            pass
        elif url == '':
            pass
        else:
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            driver = webdriver.Chrome(chrome_options=options)

            driver.get(url)
            html = driver.page_source
            soup = BeautifulSoup(html, 'lxml')
            print(soup)

            # mail = soup.find(re.compile(".+@.+"))
            mail = soup.find_all(re.compile(".+@.+"))
        return mail

    def get_email(self, url):
        parts = urlsplit(url)
        base_url = "{0.scheme}://{0.netloc}".format(parts)
        if '/' in parts.path:
            path = url[:url.rfind('/')+1]
        else:
            path = url

        try:
            response = requests.get(url)
            new_email = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.de", response.text, re.I))
            return new_email
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
            # ignore pages with errors and continue with next url
            return ''


        #soup = BeautifulSoup(response.text, 'lxml')

        # for anchor in soup.find_all("a"):
        #     if "href" in anchor.attrs:
        #         link = anchor.attrs["href"]
        #     else:
        #         link = ''

        #         if link.startswith('/'):
        #             link = base_url + link
                
        #         elif not link.startswith('http'):
        #             link = path + link

        #         if not link.endswith(".gz"):
        #         if not link in unscraped and not link in scraped:
        #             unscraped.append(link)

if __name__=='__main__':
    scraper = Scraper()
    # scraper.read_wikipedia()
    # scraper.find_missing_links()
    
    # scraper.schoolinfo.to_excel(scraper.EXP_DIR)

    scraper.schoolinfo = pd.read_excel("results_fest.xlsx", index_col=0)
    
    emails = []
    for i in range(0, int(scraper.schoolinfo.shape[0])):
        school = scraper.schoolinfo.iloc[i]
        url = school['link']

        mail = scraper.get_email(url)
        print(mail)
        emails.append(str(mail))
    series = pd.Series(emails)
    print(series)  
    scraper.schoolinfo =  pd.concat([scraper.schoolinfo, series], axis=1)
    print(scraper.schoolinfo.columns)
    scraper.schoolinfo.to_excel(scraper.EXP_DIR)