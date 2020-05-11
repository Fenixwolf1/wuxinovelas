import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wuxi.settings')
django.setup()


from bs4 import BeautifulSoup
from urllib.request import urlopen,Request
from novelas.models import Novelas,Generos

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
base_url ="https://novelfull.com/index.php/genre/Sci-fi?page=1"

req = Request(url=base_url, headers=headers) 
page = urlopen(req)
content = page.read()
page.close()

# Parsing the chapter
parsed_content = BeautifulSoup(content,'html.parser')

genres_divs = parsed_content.find_all("div", class_="col-xs-6")

for genre in genres_divs:
    genero = Generos(genre = genre.a.text) 
    genero.save()
