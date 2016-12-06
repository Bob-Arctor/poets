from bs4 import BeautifulSoup
from urllib.request import urlopen
import os

BASE_URL = 'http://versos.ru/allautors/'
authors = ['pushkin','tutchev','bunin','block','esenin','lermontov','gumilev']
ext = '.txt'
poems_path = 'poems'

for auth in authors:
    poet_url = BASE_URL + auth + '.html'
    html = urlopen(poet_url).read()
    soup = BeautifulSoup(html, "html.parser")
    file_counter = 1
    for ultag in soup.find_all('ul', {'class': 'vers_list1'}):
        for litag in ultag.find_all('li'):
            for link in litag.find_all('a'):
                poem_url = link.get('href')
                html = urlopen(poem_url).read()
                soup_poem = BeautifulSoup(html, "html.parser")
                ptag = soup_poem.find("p", {'class': 'vers'})
                f = open(os.path.join(poems_path, auth + str(file_counter) + ext), 'w')
                f.write(ptag.get_text().strip())
                f.close()
                f = open(os.path.join(poems_path, auth + str(file_counter) + ext), 'r+')
                lines = f.readlines()
                f.writelines(lines[:-2])
                f.close()
                file_counter += 1
                   
    
    